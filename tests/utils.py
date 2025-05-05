import os
import subprocess
import json
import sys
import time
import socket
import requests
from pathlib import Path

def run_command(command, shell=True, timeout=60):
    """Run a command and return its output and return code"""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout} seconds", 1

def check_file_exists(filepath):
    """Check if a file exists and return True/False"""
    return os.path.exists(filepath)

def check_directory_exists(dirpath):
    """Check if a directory exists and return True/False"""
    return os.path.isdir(dirpath)

def check_container_running(container_name):
    """Check if a Docker container is running"""
    stdout, stderr, retcode = run_command(f"docker ps -q -f name={container_name}")
    return retcode == 0 and stdout.strip() != ""

def check_port_open(port, host="localhost", timeout=1):
    """Check if a port is open on host"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def check_api_endpoint(url, method="GET", expected_status=200, timeout=5, **kwargs):
    """Check if an API endpoint returns expected status code"""
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
        return response.status_code == expected_status, response
    except requests.RequestException:
        return False, None

def check_gpu_available():
    """Check if GPU is available via PyTorch"""
    try:
        stdout, stderr, retcode = run_command(
            "python -c 'import torch; print(torch.cuda.is_available())'")
        return retcode == 0 and "True" in stdout
    except Exception:
        return False

def read_file_content(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"