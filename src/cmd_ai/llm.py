from __future__ import annotations
import sys
import os
from llama_cpp import Llama

DEFAULT_MODEL_PATH = "./qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"

class CommandGenerator:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            from cmd_ai.downloader import download_model_interactive
            print(f"[!] Model file not found at: {self.model_path}")
            if download_model_interactive():
                print("[!] Model downloaded. Initializing...")
            else:
                raise RuntimeError("Model file missing. Cannot proceed.")

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
            "You strictly output ONLY the executable command. "
            "No markdown, no explanations, no headers. "
            "If the request is ambiguous, guess the most standard command."
        )
        
        if flag == "linux":
            return f"You are an expert Linux Bash assistant. {base_instruction}"
        elif flag == "windows-ps":
            return f"You are an expert Windows PowerShell assistant. {base_instruction}"
        elif flag == "windows-cli":
            return f"You are an expert Windows Command Prompt (cmd) assistant. {base_instruction}"
        elif flag == "macos":
            return f"You are an expert macOS Terminal (Zsh) assistant. Use 'open', 'pbcopy', 'brew' where applicable. {base_instruction}"
        elif flag == "git":
            return f"You are an expert Git CLI assistant. {base_instruction}"
        elif flag == "docker":
            return f"You are an expert Docker CLI assistant. {base_instruction}"
        elif flag == "kubectl":
            return f"You are an expert Kubernetes (kubectl) assistant. {base_instruction}"
        elif flag == "aws":
            return f"You are an expert AWS CLI assistant. {base_instruction}"
        elif flag == "sql":
            return f"You are an expert SQL assistant. Output standard ANSI SQL unless asked otherwise. {base_instruction}"
        else:
            return f"You are a helpful command line assistant. {base_instruction}"

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
