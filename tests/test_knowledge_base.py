from __future__ import annotations

from cmd_ai.knowledge_base import suggest_command


def test_list_files_windows_powershell() -> None:
    cmd = suggest_command("list files", os_name="Windows", shell="PowerShell")
    assert cmd == "Get-ChildItem"


def test_list_files_linux_bash() -> None:
    cmd = suggest_command("list files", os_name="Linux", shell="Bash")
    assert cmd == "ls -la"


def test_no_match() -> None:
    cmd = suggest_command("compose a sonnet about penguins", os_name="Linux", shell="Bash")
    assert cmd is None
