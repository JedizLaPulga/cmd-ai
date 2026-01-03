from __future__ import annotations

import tkinter as tk

import pytest

from cmd_ai.gui import App


@pytest.mark.skipif(
    condition=False,
    reason="Tkinter smoke test is lightweight; kept always-on by default.",
)
def test_app_can_instantiate() -> None:
    root = tk.Tk()
    root.withdraw()
    try:
        app = App(root)
        app.query_var.set("list files")
        app.on_generate()
        assert app.output_var.get()
    finally:
        root.destroy()
