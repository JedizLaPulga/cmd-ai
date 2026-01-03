import sys
from cmd_ai.gui import App

def main():
    try:
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()