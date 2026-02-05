# LearnPython-Sandbox
⚠️ **Security Notice:** This project is **intentionally not secure**.  
It exists for **educational purposes only** to demonstrate common mistakes and limitations in Python-based sandboxing and web security controls.


## Overview
LearnPython-Sandbox is a Flask-based web service that allows users to submit and execute Python code in a constrained environment.

The sandbox relies on:
- Python-level restrictions
- Keyword blacklisting
- Subprocess-based execution

This design is **deliberately limited** and is used to study:
- Why Python is unsafe as a sandbox language
- How blacklist-based filtering fails
- Common authentication, rate-limiting, and isolation pitfalls
- Real-world remote code execution (RCE) risks


## Features
- Flask REST API for code execution
- Temporary file-based execution using `subprocess`
- Basic keyword blacklist to block obvious dangerous operations
- Execution timeout to prevent infinite loops
- JSON-based request and response format
