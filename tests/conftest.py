#!/usr/bin/env python3
"""
ML Systems Journey Test Fixtures
-------------------------------
This file contains pytest fixtures for the ML Systems Journey tests.
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from utils import run_command, check_gpu_available, check_container_running

# Add the tests directory to path to ensure modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory as a Path object"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def is_in_container():
    """Check if tests are running inside a container"""
    return os.environ.get("IN_CONTAINER") == "1"


@pytest.fixture(scope="session")
def has_gpu(is_in_container):
    """Check if a GPU is available for testing"""
    if is_in_container:
        return check_gpu_available()
    else:
        # When not in container, check if we can access a GPU
        # This helps when deciding whether to skip GPU tests outside containers
        stdout, stderr, retcode = run_command(
            "nvidia-smi 2>/dev/null || (command -v docker >/dev/null && docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi)"
        )
        return retcode == 0


@pytest.fixture(scope="session")
def kafka_is_running():
    """Check if Kafka is running for data tests"""
    return check_container_running("kafka")


@pytest.fixture(scope="session")
def mongo_is_running():
    """Check if MongoDB is running for data tests"""
    return check_container_running("mongo")


@pytest.fixture(scope="session")
def clickhouse_is_running():
    """Check if ClickHouse is running for data tests"""
    return check_container_running("clickhouse")


@pytest.fixture(scope="function")
def temp_workspace():
    """Create a temporary workspace for tests that need to create files"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up temp directory after test
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def temp_data_file():
    """Create a temporary data file for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    yield temp_file.name
    # Clean up temp file after test
    os.unlink(temp_file.name)


@pytest.fixture(scope="module")
def setup_cuda_env(is_in_container, has_gpu):
    """Set up the CUDA environment for GPU tests"""
    if not has_gpu:
        pytest.skip("No GPU available for testing")
        
    if not is_in_container:
        # Check if we need a container for GPU tests
        cuda_available = check_gpu_available()
        if not cuda_available:
            pytest.skip("CUDA not available outside container, use make test-container")
    
    # Set environment variables for CUDA tests
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    
    # Return CUDA compute capability for the first GPU
    stdout, stderr, retcode = run_command(
        "nvidia-smi --query-gpu=compute_cap --format=csv,noheader"
    )
    compute_cap = stdout.strip() if retcode == 0 else "unknown"
    
    return {
        "compute_capability": compute_cap,
        "device_count": 1  # Simplifying to use just one GPU for tests
    }


@pytest.fixture(scope="function")
def compile_cuda_program(setup_cuda_env, temp_workspace):
    """
    Fixture to compile a CUDA program for testing
    
    Usage: 
    def test_my_cuda_code(compile_cuda_program):
        binary_path = compile_cuda_program("my_code.cu", "my_binary")
        # Now run tests with binary_path
    """
    def _compile(source_path, output_name):
        # Get absolute paths
        source_abs = Path(source_path).absolute()
        output_abs = Path(temp_workspace) / output_name
        
        # Compile the CUDA program
        stdout, stderr, retcode = run_command(
            f"nvcc -o {output_abs} {source_abs} -O3"
        )
        
        assert retcode == 0, f"Failed to compile CUDA program: {stderr}"
        return str(output_abs)
    
    return _compile