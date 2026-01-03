# cmd-ai

A small CLI that converts natural-language tasks into OS/shell-specific commands.

## Run (dev)

```powershell
python -m cmd_ai
```

## Examples

```powershell
# Windows PowerShell
python -m cmd_ai "list files" --os Windows --shell PowerShell

# Windows CMD
python -m cmd_ai "list files" --os Windows --shell CMD

# Linux Bash
python -m cmd_ai "list files" --os Linux --shell Bash
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
