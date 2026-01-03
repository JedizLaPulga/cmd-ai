# cmd-ai

A small Tkinter GUI that converts natural-language tasks into OS/shell-specific commands.

## Run (dev)

```powershell
python -m cmd_ai
```

## Tests

```powershell
python -m pip install -e .
python -m pip install pytest ruff mypy
pytest
ruff check .
ruff format --check .
mypy .
```
