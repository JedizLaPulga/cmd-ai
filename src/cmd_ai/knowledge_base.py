from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Literal

OSName = Literal["Windows", "Linux"]
WindowsShell = Literal["PowerShell", "CMD"]
LinuxShell = Literal["Bash"]
ShellName = Literal["PowerShell", "CMD", "Bash"]


@dataclass(frozen=True)
class CommandEntry:
    """A single intent with per-OS/per-shell command variants."""

    intent: str
    keywords: tuple[str, ...]
    windows_powershell: str
    windows_cmd: str
    linux_bash: str


_KB: tuple[CommandEntry, ...] = (
    CommandEntry(
        intent="list_files",
        keywords=("list", "files", "directory", "folder", "ls", "dir"),
        windows_powershell="Get-ChildItem",
        windows_cmd="dir",
        linux_bash="ls -la",
    ),
    CommandEntry(
        intent="current_directory",
        keywords=("where am i", "current directory", "pwd", "path"),
        windows_powershell="Get-Location",
        windows_cmd="cd",
        linux_bash="pwd",
    ),
    CommandEntry(
        intent="make_directory",
        keywords=("make", "create", "mkdir", "folder", "directory"),
        windows_powershell='New-Item -ItemType Directory -Path "<name>"',
        windows_cmd='mkdir "<name>"',
        linux_bash='mkdir -p "<name>"',
    ),
    CommandEntry(
        intent="remove_file",
        keywords=("delete", "remove", "rm", "del", "file"),
        windows_powershell='Remove-Item -Path "<path>"',
        windows_cmd='del "<path>"',
        linux_bash='rm -f "<path>"',
    ),
    CommandEntry(
        intent="search_text",
        keywords=("search", "find", "grep", "text", "string"),
        windows_powershell='Select-String -Path "<files>" -Pattern "<text>"',
        windows_cmd='findstr /S /N /I "<text>" <files>',
        linux_bash='grep -RIn "<text>" <path>',
    ),
)


def _score(query: str, entry: CommandEntry) -> float:
    q = query.strip().lower()
    if not q:
        return 0.0

    keyword_hits = sum(1 for k in entry.keywords if k in q)
    keyword_score = min(1.0, keyword_hits / max(1, len(entry.keywords)))

    similarity = SequenceMatcher(None, q, entry.intent.replace("_", " ")).ratio()

    return (0.75 * keyword_score) + (0.25 * similarity)


def suggest_command(
    query: str,
    os_name: OSName,
    shell: ShellName,
    *,
    min_score: float = 0.15,
    knowledge_base: Iterable[CommandEntry] = _KB,
) -> str | None:
    """Return the best matching command for the query, or None if no match.

    This is intentionally deterministic and offline (no network / no LLM).
    """

    scored = [(entry, _score(query, entry)) for entry in knowledge_base]
    best_entry, best_score = max(scored, key=lambda t: t[1], default=(None, 0.0))

    if best_entry is None or best_score < min_score:
        return None

    if os_name == "Windows":
        if shell == "PowerShell":
            return best_entry.windows_powershell
        if shell == "CMD":
            return best_entry.windows_cmd
        return None

    if os_name == "Linux":
        if shell == "Bash":
            return best_entry.linux_bash
        return None

    return None
