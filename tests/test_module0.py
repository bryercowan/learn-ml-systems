import os
import pytest
from pathlib import Path
from utils import (
    run_command,
    check_file_exists,
    check_directory_exists,
    check_container_running,
    check_gpu_available
)

class TestModule0A:
    """Tests for Module 0-A: Course Setup"""
    
    def test_readme_exists(self):
        """Test that README.md exists with project title"""
        assert check_file_exists("README.md"), "README.md file not found"
        
        # Check README content
        with open("README.md", "r") as f:
            content = f.read()
        assert "ML Systems Journey" in content, "README.md should contain project title"
    
    def test_remote_origin(self):
        """Test that remote origin is configured"""
        stdout, stderr, retcode = run_command("git remote -v")
        assert retcode == 0, f"Failed to run git remote command: {stderr}"
        assert "origin" in stdout, "No git remote 'origin' found"
    
    def test_git_push(self):
        """Test ability to push to remote (mocked)"""
        # We'll just check if origin exists since actual push would change repo
        stdout, stderr, retcode = run_command("git remote -v | grep origin")
        assert retcode == 0, "Remote origin not properly configured for git push"
    
    def test_cuda_available(self):
        """Test if CUDA is available in the container"""
        # This test is meant to be run inside the container
        if os.environ.get("IN_CONTAINER") != "1":
            pytest.skip("Not in container, skipping CUDA test")
            
        assert check_gpu_available(), "CUDA is not available in the container"


class TestModule0B:
    """Tests for Module 0-B: Kafka Hello-World"""
    
    def test_kafka_container(self):
        """Test if Kafka container is running"""
        assert check_container_running("kafka"), "Kafka container is not running"
    
    def test_docker_compose_file(self):
        """Test that docker-compose.yml exists"""
        assert check_file_exists("docker-compose.yml"), "docker-compose.yml not found"
    
    def test_kafka_producer(self):
        """Test if Python Kafka producer script can run"""
        script = """
from kafka import KafkaProducer
import json, uuid, random
p = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode()
)
msg = {"id": str(uuid.uuid4()), "v": random.random()}
p.send("test", msg)
p.flush()
print("Message sent successfully")
"""
        stdout, stderr, retcode = run_command(f"python -c '{script}'", timeout=10)
        assert retcode == 0, f"Failed to run Kafka producer: {stderr}"
        assert "Message sent successfully" in stdout, "Producer didn't send message"


class TestModuleM0:
    """Tests for Module 0 Project: DevBox Skeleton"""
    
    def test_devcontainer_exists(self):
        """Test that .devcontainer folder exists"""
        assert check_directory_exists(".devcontainer"), ".devcontainer folder not found"
    
    def test_make_test_dev(self):
        """Test running make test-dev command"""
        stdout, stderr, retcode = run_command("make test-dev")
        assert retcode == 0, f"make test-dev failed: {stderr}"
        assert "DevBox ready" in stdout or "DevBox ready" in stderr, "DevBox ready message not found"


if __name__ == "__main__":
    # Allow running this file directly for a specific module test
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--in-container":
        os.environ["IN_CONTAINER"] = "1"
        
    pytest.main(["-xvs", __file__])