import threading

import customtkinter as ctk

from cmd_ai.llm import CommandGenerator

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatBubble(ctk.CTkFrame):
    def __init__(self, master, text, is_user=False, **kwargs):
        super().__init__(master, **kwargs)
        self.is_user = is_user
        
        # Colors
        bg_color = "#1f538d" if is_user else "#2b2b2b"
        text_color = "white"
        
        self.configure(fg_color="transparent")
        
        # Bubble Container
        self.bubble = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=15)
        
        if is_user:
            self.bubble.pack(side="right", padx=10, pady=5, anchor="e")
        else:
            self.bubble.pack(side="left", padx=10, pady=5, anchor="w")
            
        # Text
        self.label = ctk.CTkLabel(
            self.bubble, 
            text=text, 
            text_color=text_color, 
            wraplength=400, 
            justify="left" if not is_user else "right",
            font=("Roboto", 14)
        )
        self.label.pack(side="left", padx=15, pady=10)

        # Copy Button (Only for AI responses)
        if not is_user and text and not text.startswith("Welcome") and not text.startswith("error"):
            self.copy_btn = ctk.CTkButton(
                self.bubble, 
                text="📋", 
                width=30, 
                height=30, 
                fg_color="transparent", 
                hover_color="#404040",
                command=lambda: self.copy_to_clipboard(text)
            )
            self.copy_btn.pack(side="right", padx=(0, 10))

    def copy_to_clipboard(self, text):
        # Native Tkinter Clipboard access
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.master.update() # Required to finalize clipboard on some systems
        
        self.copy_btn.configure(text="✅")
        self.after(2000, lambda: self.copy_btn.configure(text="📋"))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ShellSage")
        self.geometry("900x600")
        
        # Initialize Logic
        self.current_flag = "windows-cli"
        self.generator = None
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) # Row 1 (Chat) expands
        
        self.create_sidebar()
        self.create_status_area() # Row 0
        self.create_chat_area()   # Row 1
        self.create_input_area()  # Row 2

        # Welcome Message
        self.add_message("System", "ShellSage v1.0\nReady to transpile commands.", is_user=False)
        
        # Start Thread AFTER logic is ready
        self.init_model_thread()

    def init_model_thread(self):
        threading.Thread(target=self.load_model, daemon=True).start()

    def update_status(self, color):
        self.status_canvas.itemconfig(self.status_indicator, fill=color)

    def load_model(self):
        try:
            self.after(0, lambda: self.update_status("orange"))
            self.generator = CommandGenerator()
            # Success -> Green
            self.after(0, lambda: self.update_status("#00ff00")) 
        except Exception as e:
            # Failure -> Red
            self.after(0, lambda: self.update_status("#ff0000"))
            err_msg = str(e)
            self.after(0, lambda: self.add_message("System", f"error, cant load brain of app: {err_msg}", is_user=False))

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew") # Spans 3 rows
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ShellSage", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Target Shell:", anchor="w")
        self.mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        self.mode_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["windows-cli", "windows-ps", "linux", "macos", "git", "docker", "kubectl", "aws", "sql"],
                                                                         command=self.change_mode)
        self.mode_option.grid(row=2, column=0, padx=20, pady=10)
        self.mode_option.set("windows-cli")

    def create_status_area(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.header_frame.grid(row=0, column=1, sticky="e", padx=20, pady=(10,0))
        
        self.status_label = ctk.CTkLabel(self.header_frame, text="Model Status:", font=("Arial", 12))
        self.status_label.pack(side="right", padx=5)
        
        self.status_canvas = ctk.CTkCanvas(self.header_frame, width=14, height=14, bg="#2b2b2b", highlightthickness=0)
        self.status_canvas.pack(side="right")
        self.status_indicator = self.status_canvas.create_oval(2, 2, 13, 13, fill="gray", outline="")

    def create_chat_area(self):
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=(10, 20))

    def create_input_area(self):
        self.entry = ctk.CTkEntry(self, placeholder_text="Type your command request here...")
        self.entry.grid(row=2, column=1, sticky="ewe", padx=(20, 20), pady=(0, 20))
        self.entry.bind("<Return>", self.send_message_event)
        
        self.send_button = ctk.CTkButton(self, text="Generate", command=self.send_message_event)
        self.send_button.grid(row=2, column=2, padx=(0, 20), pady=(0, 20))

    def change_mode(self, new_mode):
        self.current_flag = new_mode

    def send_message_event(self, event=None):
        text = self.entry.get()
        if not text:
            return
            
        self.entry.delete(0, "end")
        self.add_message("User", text, is_user=True)
        
        if not self.generator:
            self.add_message("System", "⚠️ Model is still loading, please wait...", is_user=False)
            return

        # Disable input while generating
        self.entry.configure(state="disabled")
        
        # Run generation in thread
        threading.Thread(target=self.generate_response, args=(text,), daemon=True).start()

    def generate_response(self, text):
        try:
            response = self.generator.generate(text, self.current_flag)
            self.after(0, lambda: self.display_response(response))
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self.add_message("System", f"Error: {err_msg}", is_user=False))
            self.after(0, lambda: self.entry.configure(state="normal"))

    def display_response(self, text):
        self.add_message("AI", text, is_user=False)
        self.entry.configure(state="normal")

    def add_message(self, sender, text, is_user):
        bubble = ChatBubble(self.chat_frame, text=text, is_user=is_user)
        bubble.pack(fill="x", pady=5)
        
        # Auto scroll to bottom
        self.after(10, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
