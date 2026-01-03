# 🐚 ShellSage
**Local Command Transpiler**

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20Mac-lightgrey?style=for-the-badge)
![AI Model](https://img.shields.io/badge/Model-Qwen2.5--Coder-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Turn natural language into executable shell commands—instantly, offline, and privately.**

ShellSage is a Python-based **Desktop Application** that uses a lightweight **Local Large Language Model (LLM)** to translate human requests (e.g., *"Create a new folder and enter it"*) into precise terminal commands for **Windows CMD**, **PowerShell**, or **Linux Bash**.

---

## ✨ Key Features

* **✨ Modern GUI:** A beautiful, dark-mode graphical interface built with `customtkinter`.
* **🧠 Context-Aware:** Supports **Windows, Linux, macOS**, plus specialized tools like **Git, Docker, Kubernetes, AWS, and SQL**.
* **🔒 100% Offline & Private:** Runs entirely on your machine using GGUF models. No API keys, no cloud costs, no data leaks.
* **⚡ High Performance:** Optimized for CPU inference using `llama.cpp`.
* **📋 One-Click Copy:** Native copy button allows for instant command extraction.
* **️ Easy to Use:** Select your target shell from the sidebar and start chatting.

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

### 3. Download the Model
**Important:** You must download the AI model (~1.0 GB) for the tool to work.

You can do this by running the application, which will offer to download it for you:
```bash
# Run the application
python -m cmd_ai
```

### 3. Usage
Simply launch the app and:
1. Select your target shell (CMD, PowerShell, or Linux) from the sidebar.
2. Type your request in natural language (e.g., "delete all logs older than 7 days").
3. View the generated command in the chat window.
