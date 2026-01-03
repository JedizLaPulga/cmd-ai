from __future__ import annotations

import os
import sys

from llama_cpp import Llama

DEFAULT_MODEL_PATH = "./qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"

class CommandGenerator:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        # robust path resolution
        candidates = [
            model_path,
            os.path.abspath(model_path),
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
            ),
            os.path.join(os.getcwd(), "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf")
        ]
        
        found_path = None
        for candidate in candidates:
            if os.path.exists(candidate):
                found_path = candidate
                break
        
        if found_path:
            self.model_path = found_path
        else:
            # Check if likely in a non-interactive environment (GUI)
            # If so, do NOT call interactive download which blocks.
            if sys.stdin and sys.stdin.isatty():
                from cmd_ai.downloader import download_model_interactive
                print(f"[!] Model file not found. Searched: {candidates}")
                if download_model_interactive():
                    print("[!] Model downloaded. Initializing...")
                    self.model_path = "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf" # Default download location
                else:
                    raise RuntimeError("Model download cancelled.")
            else:
                 msg = (
                     f"Model file missing. Please run 'python -m cmd_ai.downloader' "
                     f"to setup. (Searched: {candidates})"
                 )
                 raise RuntimeError(msg)

        print(f"Loading AI Model from {self.model_path}...")
        try:
            self.llm = Llama(model_path=self.model_path, n_ctx=2048, verbose=False)
            print("Model loaded successfully!")
        except Exception as e:
            # Re-raising or handling elegantly - for CLI we might want to exit or let main handle
            raise RuntimeError(f"Could not load model from '{self.model_path}': {e}") from e

    def get_system_prompt(self, flag: str) -> str:
        """Returns the persona instructions based on the user's flag."""
        base_instruction = (
            "You are a highly accurate command line assistant. "
            "Your ONLY task is to output the precise, executable shell command for the user's request.\n"
            "Rules:\n"
            "1. Output ONLY the command. No markdown, no comments, no explanations, no prologue.\n"
            "2. If multiple steps are needed, chain them with && or ; appropriate for the shell.\n"
            "3. If the request is ambiguous, generate the most standard, safe command.\n"
            "4. Do NOT use placeholders like <file> unless unavoidable. Try to infer or use '*'.\n"
        )
        
        examples = {
            "linux": (
                "User: list all files detailed\nAssistant: ls -la\n"
                "User: count lines in file.txt\nAssistant: wc -l file.txt"
            ),
            "windows-ps": (
                "User: list files\nAssistant: Get-ChildItem\n"
                "User: download file from url\nAssistant: Invoke-WebRequest -Uri 'url' -OutFile 'file'"
            ),
            "windows-cli": (
                "User: show files\nAssistant: dir\n"
                "User: delete folder\nAssistant: rmdir /s /q folder"
            ),
            "macos": (
                "User: copy file to clipboard\nAssistant: pbcopy < file.txt\n"
                "User: install git\nAssistant: brew install git"
            ),
            "git": (
                "User: undo last commit\nAssistant: git reset --soft HEAD~1\n"
                "User: push new branch\nAssistant: git push -u origin HEAD"
            ),
            "docker": (
                "User: run nginx\nAssistant: docker run -d -p 80:80 nginx\n"
                "User: clean system\nAssistant: docker system prune -f"
            ),
            "kubectl": (
                "User: get pods\nAssistant: kubectl get pods\n"
                "User: logs for service\nAssistant: kubectl logs -l app=service"
            ),
            "aws": (
                "User: list buckets\nAssistant: aws s3 ls\n"
                "User: describe instances\nAssistant: aws ec2 describe-instances"
            ),
            "sql": (
                "User: select all users\nAssistant: SELECT * FROM users;\n"
                "User: count orders\nAssistant: SELECT COUNT(*) FROM orders;"
            )
        }

        # Select prompt
        role = f"You are an expert {flag} assistant. "
        
        specific_examples = examples.get(flag, "")
        if specific_examples:
            full_prompt = f"{role}{base_instruction}\nExamples:\n{specific_examples}"
        else:
            full_prompt = f"{role}{base_instruction}"
            
        return full_prompt

    def generate(self, user_input: str, flag: str) -> str:
        """Sends the natural language to the LLM and gets code back."""
        
        system_role = self.get_system_prompt(flag)
        
        # Qwen/ChatML Prompt Format
        prompt = f"""<|im_start|>system
{system_role}<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""
        
        # Run Inference
        output = self.llm(
            prompt, 
            max_tokens=256, 
            stop=["<|im_end|>"], # Let it generate the full response (including newlines)
            temperature=0.1, 
            echo=False
        )
        
        raw_text = output['choices'][0]['text'].strip()
        
        # Clean Markdown Code Blocks if present
        if "```" in raw_text:
            lines = raw_text.split('\n')
            code_lines = []
            in_block = False
            for line in lines:
                if line.strip().startswith("```"):
                    in_block = not in_block
                    continue
                if in_block:
                    code_lines.append(line)
            
            if code_lines:
                return "\n".join(code_lines).strip()
            
            # Fallback if parsing failed but backticks exist (e.g. inline code)
            return raw_text.replace("`", "").strip()

        return raw_text
