import sys
import os
from llama_cpp import Llama

# --- Configuration ---
MAX_INPUT_SIZE = 1024
DEFAULT_FLAG = "windows-cli"
VALID_FLAGS = {"windows-cli", "windows-ps", "linux"}

# Make sure this matches the EXACT name of the file you downloaded
MODEL_PATH = "./qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"

# --- 1. Load the "Brain" (The AI Model) ---
print(f"Loading AI Model from {MODEL_PATH}...")
try:
    # n_ctx=2048: The memory window. Sufficient for shell commands.
    # verbose=False: Hides the messy technical logs during startup.
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
    print("Model loaded successfully!")
except Exception as e:
    print(f"[CRITICAL ERROR] Could not load model: {e}")
    print(f"Make sure '{MODEL_PATH}' exists in this folder.")
    sys.exit(1)

def get_system_prompt(flag):
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
    else: # windows-cli
        return f"You are an expert Windows Command Prompt (cmd) assistant. {base_instruction}"

def generate_command(user_input, flag):
    """Sends the natural language to the LLM and gets code back."""
    
    system_role = get_system_prompt(flag)
    
    # Qwen/ChatML Prompt Format
    prompt = f"""<|im_start|>system
{system_role}<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""
    
    # Run Inference
    output = llm(
        prompt, 
        max_tokens=128, 
        stop=["<|im_end|>", "\n"], # Stop generating after the command
        temperature=0.1, # Low temp = precise code, no creativity
        echo=False
    )
    
    return output['choices'][0]['text'].strip()

def get_prompt_text(current_flag):
    return f"({current_flag}) >>> "

# --- 2. The REPL Loop (The Interface) ---
def start_repl():
    current_flag = DEFAULT_FLAG
    
    print("-" * 50)
    print(f"AI Shell Translator Ready.")
    print(f"Current Mode: {current_flag}")
    print("Commands:")
    print("  -change-flag=linux       : Switch to Linux")
    print("  -change-flag=windows-ps  : Switch to PowerShell")
    print("  -change-flag=windows-cli : Switch to CMD")
    print("  exit / quit              : Stop")
    print("-" * 50)

    while True:
        try:
            # Get Input
            user_input = input(get_prompt_text(current_flag))
            cleaned_input = user_input.strip()

            # Handle Empty Input
            if not cleaned_input:
                continue

            # Handle Exit
            if cleaned_input.lower() in ('exit', 'quit'):
                print("Exiting...")
                sys.exit(0)

            # Handle Flag Change
            if cleaned_input.startswith("-change-flag="):
                try:
                    _, new_flag = cleaned_input.split("=", 1)
                    new_flag = new_flag.lower().strip()
                    if new_flag in VALID_FLAGS:
                        current_flag = new_flag
                        print(f"[System] Switched to: {current_flag}")
                    else:
                        print(f"[Error] Invalid flag. Use: {', '.join(VALID_FLAGS)}")
                except ValueError:
                     print("[Error] Use format: -change-flag=value")
                continue

            # Safety Check
            if len(user_input) > MAX_INPUT_SIZE:
                print(f"[Error] Input too long.")
                continue

            # --- AI GENERATION STEP ---
            # 1. Show a loading indicator (optional but nice)
            print("... generating ...", end="\r") 
            
            # 2. Get prediction
            command = generate_command(cleaned_input, current_flag)
            
            # 3. Clear loading line and print result
            print(" " * 20, end="\r") # Clear the "... generating ..."
            print(f"[{current_flag} suggestion]: {command}")

        except KeyboardInterrupt:
            print("\n[!] Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    start_repl()