import sys

# Configuration
MAX_INPUT_SIZE = 1024
# Default is set to Windows Command Line
DEFAULT_FLAG = "windows-cli"
VALID_FLAGS = {"windows-cli", "windows-ps", "linux"}

def get_prompt(current_flag):
    """Generates the prompt string based on the current flag."""
    return f"({current_flag}) >>> "

def safe_echo_repl():
    current_flag = DEFAULT_FLAG
    
    print(f"Starting Echo REPL. Default flag: {current_flag}")
    print("Commands:")
    print("  -change-flag=windows-cli : Switch to Windows CMD mode")
    print("  -change-flag=windows-ps  : Switch to Windows PowerShell mode")
    print("  -change-flag=linux       : Switch to Linux mode")
    print("  exit / quit              : Stop the program")
    print("-" * 50)

    while True:
        try:
            # 1. READ
            user_input = input(get_prompt(current_flag))

            # 2. EVAL
            cleaned_input = user_input.strip()

            # Check for exit commands
            if cleaned_input.lower() in ('exit', 'quit'):
                print("Exiting...")
                sys.exit(0)

            # Check for Flag Change Command
            if cleaned_input.startswith("-change-flag="):
                try:
                    # Extract value after '='
                    _, new_flag = cleaned_input.split("=", 1)
                    new_flag = new_flag.lower().strip()
                    
                    if new_flag in VALID_FLAGS:
                        current_flag = new_flag
                        print(f"[System] Flag switched to: {current_flag}")
                    else:
                        # Show available options on error
                        print(f"[Error] Invalid flag '{new_flag}'.")
                        print(f"Valid options: {', '.join(sorted(VALID_FLAGS))}")
                except ValueError:
                     print("[Error] Invalid format. Use -change-flag=value")
                
                # Skip echo for commands
                continue

            # Memory/Buffer Safety Check
            if len(user_input) > MAX_INPUT_SIZE:
                print(f"[Error] Input exceeds buffer limit of {MAX_INPUT_SIZE} chars.")
                continue

            # 3. PRINT
            print(f"[{current_flag} echo]: {user_input}")

        except KeyboardInterrupt:
            print("\n[!] Interrupted. Exiting.")
            sys.exit(0)
        except EOFError:
            print("\n[!] EOF. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"[Error] Unexpected: {e}")

if __name__ == "__main__":
    safe_echo_repl()