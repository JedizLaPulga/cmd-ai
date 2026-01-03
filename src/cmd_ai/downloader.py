import os
import sys
import urllib.request
import time

MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
FILENAME = "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"

def get_model_path():
    """Returns the absolute path to the model file."""
    # Assuming the model is stored in the project root or a specific cache dir
    # For now, keeping it in the current working directory relative to execution context
    return os.path.abspath(FILENAME)

def check_model_exists():
    return os.path.exists(FILENAME)

def download_model_interactive():
    print(f"\n[!] Model file '{FILENAME}' is missing.")
    print(f"[!] This tool requires the Qwen 2.5 Coder GGUF model (~1.0 GB).")
    
    response = input("Would you like to download it now? [y/N]: ").strip().lower()
    if response not in ('y', 'yes'):
        print("Download aborted. The application cannot function without the model.")
        sys.exit(1)

    print(f"Downloading from: {MODEL_URL}")
    print("This may take a few minutes depending on your internet connection...")
    
    start_time = time.time()
    try:
        def reporthook(blocknum, blocksize, totalsize):
            readso_far = blocknum * blocksize
            if totalsize > 0:
                percent = readso_far * 1e2 / totalsize
                # Basic progress bar
                sys.stdout.write(f"\rDownloading: {percent:.1f}% ({int(readso_far/1024/1024)}MB / {int(totalsize/1024/1024)}MB)")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(MODEL_URL, FILENAME, reporthook)
        print("\n") # Newline after progress bar
        
        elapsed = time.time() - start_time
        print(f"Download complete! ({elapsed:.2f}s)")
        return True
        
    except KeyboardInterrupt:
        print("\n[!] Download canceled.")
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        sys.exit(1)
    except Exception as e:
        print(f"\n[Error] Download failed: {e}")
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        sys.exit(1)

if __name__ == "__main__":
    download_model_interactive()
