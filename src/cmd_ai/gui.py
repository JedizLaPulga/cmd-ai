from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from cmd_ai.knowledge_base import OSName, ShellName, suggest_command


class App(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)

        self.os_var = tk.StringVar(value="Windows")
        self.shell_var = tk.StringVar(value="PowerShell")
        self.query_var = tk.StringVar(value="")
        self.output_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="")

        self._build()
        self._wire_events()
        self._sync_shell_options()

    def _build(self) -> None:
        self.grid(column=0, row=0, sticky="nsew")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)

        title = ttk.Label(self, text="cmd-ai", font=("Segoe UI", 14, "bold"))
        title.grid(column=0, row=0, sticky="w", padx=12, pady=(12, 6))

        form = ttk.Frame(self)
        form.grid(column=0, row=1, sticky="ew", padx=12)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Request").grid(column=0, row=0, sticky="w", pady=4)
        query_entry = ttk.Entry(form, textvariable=self.query_var)
        query_entry.grid(column=1, row=0, sticky="ew", pady=4)
        query_entry.focus_set()

        ttk.Label(form, text="OS").grid(column=0, row=1, sticky="w", pady=4)
        os_combo = ttk.Combobox(form, textvariable=self.os_var, state="readonly")
        os_combo["values"] = ("Windows", "Linux")
        os_combo.grid(column=1, row=1, sticky="w", pady=4)

        ttk.Label(form, text="Shell").grid(column=0, row=2, sticky="w", pady=4)
        self.shell_combo = ttk.Combobox(form, textvariable=self.shell_var, state="readonly")
        self.shell_combo.grid(column=1, row=2, sticky="w", pady=4)

        buttons = ttk.Frame(self)
        buttons.grid(column=0, row=2, sticky="ew", padx=12, pady=(10, 0))

        self.generate_btn = ttk.Button(buttons, text="Generate", command=self.on_generate)
        self.generate_btn.grid(column=0, row=0, sticky="w")

        self.copy_btn = ttk.Button(buttons, text="Copy", command=self.on_copy)
        self.copy_btn.grid(column=1, row=0, sticky="w", padx=(8, 0))

        ttk.Label(self, text="Command").grid(column=0, row=3, sticky="w", padx=12, pady=(12, 4))

        output = ttk.Entry(self, textvariable=self.output_var, state="readonly")
        output.grid(column=0, row=4, sticky="ew", padx=12)

        status = ttk.Label(self, textvariable=self.status_var)
        status.grid(column=0, row=5, sticky="w", padx=12, pady=(8, 12))

    def _wire_events(self) -> None:
        self.os_var.trace_add("write", lambda *_: self._sync_shell_options())
        self.shell_var.trace_add("write", lambda *_: self.status_var.set(""))
        self.query_var.trace_add("write", lambda *_: self.status_var.set(""))

        self.master.bind("<Return>", lambda _e: self.on_generate())

    def _sync_shell_options(self) -> None:
        os_name: OSName = "Windows" if self.os_var.get() != "Linux" else "Linux"
        if os_name == "Windows":
            self.shell_combo["values"] = ("PowerShell", "CMD")
            if self.shell_var.get() not in ("PowerShell", "CMD"):
                self.shell_var.set("PowerShell")
        else:
            self.shell_combo["values"] = ("Bash",)
            self.shell_var.set("Bash")

    def on_generate(self) -> None:
        query = self.query_var.get().strip()
        if not query:
            self.output_var.set("")
            self.status_var.set("Enter a request.")
            return

        os_name: OSName = "Windows" if self.os_var.get() != "Linux" else "Linux"
        shell: ShellName = self.shell_var.get()  # type: ignore[assignment]

        cmd = suggest_command(query, os_name=os_name, shell=shell)
        if cmd is None:
            self.output_var.set("")
            self.status_var.set("No matching command found.")
            return

        self.output_var.set(cmd)
        self.status_var.set("Ready.")

    def on_copy(self) -> None:
        cmd = self.output_var.get().strip()
        if not cmd:
            self.status_var.set("Nothing to copy.")
            return

        self.clipboard_clear()
        self.clipboard_append(cmd)
        self.status_var.set("Copied.")


def run_app() -> None:
    root = tk.Tk()
    root.title("cmd-ai")
    root.geometry("720x240")

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    App(root)
    root.mainloop()
