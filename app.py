from flask import Flask, request, jsonify
import subprocess
import uuid
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Python Sandbox Service!"})

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')

    # Blacklist check to prevent dangerous code execution
    forbidden_keywords = [
        # Module imports
        'import os', 'import sys', 'import subprocess', 'import shutil',
        'import socket', 'import multiprocessing', 'import threading', 'import asyncio',
        'import logging', 'import pathlib', 'import pickle', 'import base64',
        'import ctypes', 'import pwd', 'import grp',

        # Dangerous built-in functions
        '__import__', 'eval(', 'exec(', 'compile(', 'execfile(', 'input(',
        'globals(', 'locals(', 'vars(', 'delattr(', 'setattr(', 'getattr(',
        'open(', 'file(',

        # OS command execution
        'os.system', 'os.popen', 'os.exec', 'os.fork', 'os.spawn',
        'os.remove', 'os.unlink', 'os.rmdir', 'os.makedirs',
        'os.chmod', 'os.chown', 'os.rename', 'os.kill', 'os.abort',

        # Subprocess and shell execution
        'subprocess.Popen', 'subprocess.run', 'subprocess.call',
        'subprocess.check_output', 'subprocess.check_call',
        'shlex.split', 'shutil.rmtree', 'shutil.copy', 'shutil.move',

        # Network and socket access
        'socket.socket', 'socket.bind', 'socket.connect', 'socket.listen',
        'socket.accept', 'socket.recv', 'socket.send',
        'http.client', 'urllib',

        # Multi-threading / multi-processing
        'threading.Thread', 'multiprocessing.Process', 'multiprocessing.Pool',

        # Unsafe data deserialization
        'pickle.load', 'pickle.loads',
        'base64.b64decode', 'marshal.loads', 'marshal.load',

        # File operations
        'write(', 'read(', 'delete(', 'save(', 'chmod(', 'chown(', 'unlink(',

        # Reflection / introspection abuse
        'ctypes.', 'globals()', 'locals()',

        # GUI abuse
        'import turtle',
    ]

    if any(keyword in code for keyword in forbidden_keywords):
        return jsonify({"error": "Forbidden keyword in code"}), 403

    try:
        # Create a temporary file to store user code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Execute user code in a restricted environment
        result = subprocess.run(
            ['python3', temp_file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Delete temporary file
        subprocess.run(['rm', temp_file_path])

        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)