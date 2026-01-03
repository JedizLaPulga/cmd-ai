# 🐚 ShellSage: AI Command Transpiler

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20Mac-lightgrey?style=for-the-badge)
![AI Model](https://img.shields.io/badge/Model-Qwen2.5--Coder-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Turn natural language into executable shell commands—instantly, offline, and privately.**

ShellSage is a Python-based REPL (Read-Eval-Print Loop) tool that uses a lightweight **Local Large Language Model (LLM)** to translate human requests (e.g., *"Create a new folder and enter it"*) into precise terminal commands for **Windows CMD**, **PowerShell**, or **Linux Bash**.

---

## ✨ Key Features

* **🔒 100% Offline & Private:** Runs entirely on your machine using GGUF models. No API keys, no cloud costs, no data leaks.
* **🧠 Context-Aware:** Intelligent switching between environments. It knows the difference between `ls -la` (Linux), `dir` (CMD), and `Get-ChildItem` (PowerShell).
* **🛡️ Safety First:**
    * **Dry-Run Default:** Commands are *suggested*, not executed. You are always in control.
    * **Memory Safe:** Implements strict input buffering (`1024` chars) to prevent memory exhaustion and DoS attempts.
* **⚡ High Performance:** Optimized for CPU inference using `llama.cpp`.
* **🔄 Hot-Swappable Context:** Switch OS flags instantly inside the prompt without restarting.

---

## 🚀 Installation

### 1. Prerequisites
* **Python 3.10** or higher.
* **(Windows Only)**: Visual Studio C++ Build Tools (required for compiling `llama-cpp-python`).

### 2. Clone & Setup
```bash
# Clone the repository
git clone [https://github.com/jedizlapulga/shellsage.git](https://github.com/jedizlapulga/shellsage.git)
cd shellsage

# Create a Virtual Environment (Recommended)
# Windows:
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt