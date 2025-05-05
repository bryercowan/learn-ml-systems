import os
import pytest
import re
import requests
from pathlib import Path
from utils import (
    run_command,
    check_file_exists,
    check_container_running,
    check_port_open,
    check_api_endpoint,
    read_file_content
)

class TestModule4A:
    """Tests for Module 4-A: Data Plane Ready"""
    
    def test_compose_file(self):
        """Test if data plane compose file exists"""
        assert check_file_exists("stacks/dataplane.yml"), "Data plane compose file not found"
    
    def test_services_running(self):
        """Test if required services are running"""
        # Check if Kafka is running
        assert check_container_running("kafka"), "Kafka container not running"
        
        # Check if ClickHouse is running
        assert check_container_running("clickhouse"), "ClickHouse container not running"
    
    def test_streaming_component(self):
        """Test if streaming component exists"""
        assert check_file_exists("stream_to_ch"), "Stream to ClickHouse binary not found"
        
        # Alternative: check for Rust source code
        if not check_file_exists("stream_to_ch"):
            assert check_file_exists("src/stream_to_ch") or check_file_exists("crates/stream_to_ch"), "Stream to ClickHouse source code not found"
    
    def test_snapshot_script(self):
        """Test if snapshot script exists"""
        assert check_file_exists("snapshot.py"), "Snapshot script not found"
    
    def test_snapshot_output(self):
        """Test if snapshot directory exists"""
        assert check_directory_exists("snapshots"), "Snapshots directory not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/4-A.md"), "Debrief notes file not found"
        
        # Check if debrief discusses retention
        content = read_file_content("notes/4-A.md")
        assert re.search(r'retention', content.lower()), "Debrief doesn't discuss retention strategy"

    def check_directory_exists(self, path):
        """Helper to check if directory exists"""
        return os.path.isdir(path)


class TestModule4B:
    """Tests for Module 4-B: Training Pipeline"""
    
    def test_prefect_flow(self):
        """Test if Prefect flow file exists"""
        assert check_file_exists("flows/capstone.py"), "Prefect flow file not found"
    
    def test_flow_content(self):
        """Test if flow file contains expected content"""
        if not check_file_exists("flows/capstone.py"):
            pytest.skip("Flow file not found")
            
        content = read_file_content("flows/capstone.py")
        assert "prefect" in content.lower(), "Flow file doesn't import prefect"
        assert re.search(r'flow|task', content.lower()), "Flow file doesn't define flow or tasks"
    
    def test_wandb_integration(self):
        """Test if flow integrates with W&B"""
        if not check_file_exists("flows/capstone.py"):
            pytest.skip("Flow file not found")
            
        content = read_file_content("flows/capstone.py")
        assert "wandb" in content.lower(), "Flow doesn't integrate with W&B"
    
    def test_custom_kernels(self):
        """Test if custom CUDA kernels are defined"""
        # This could be checking for .cu files or Python modules wrapping custom kernels
        kernel_files_exist = False
        
        for ext in [".cu", ".cuh", ".cpp", ".h"]:
            stdout, _, _ = run_command(f"find . -name '*kernel*{ext}' -o -name '*cuda*{ext}'")
            if stdout.strip():
                kernel_files_exist = True
                break
                
        assert kernel_files_exist, "No custom kernel files found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/4-B.md"), "Debrief notes file not found"
        
        # Check if debrief contains throughput analysis
        content = read_file_content("notes/4-B.md")
        assert re.search(r'throughput|baseline|performance', content.lower()), "Debrief doesn't analyze throughput"


class TestModule4C:
    """Tests for Module 4-C: Model Serving"""
    
    def test_dockerfile(self):
        """Test if serving Dockerfile exists"""
        assert check_file_exists("serve.Dockerfile"), "Serving Dockerfile not found"
    
    def test_api_code(self):
        """Test if API code exists"""
        # Look for FastAPI code
        api_file_exists = False
        for file in ["app.py", "api.py", "server.py", "main.py"]:
            if check_file_exists(file):
                content = read_file_content(file)
                if "fastapi" in content.lower():
                    api_file_exists = True
                    break
                
        assert api_file_exists, "FastAPI code not found"
    
    def test_grpc_client(self):
        """Test if gRPC client exists"""
        assert check_file_exists("grpc_client.py"), "gRPC client not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/4-C.md"), "Debrief notes file not found"
        
        # Check if debrief records memory and latency
        content = read_file_content("notes/4-C.md")
        assert re.search(r'memory|footprint', content.lower()), "Debrief doesn't record memory footprint"
        assert re.search(r'latency|response time', content.lower()), "Debrief doesn't record latency"


class TestModule4D:
    """Tests for Module 4-D: Observability & CI"""
    
    def test_github_workflow(self):
        """Test if GitHub workflow exists"""
        assert check_file_exists(".github/workflows/ci.yml"), "GitHub workflow file not found"
    
    def test_monitoring_compose(self):
        """Test if monitoring compose file exists"""
        assert check_file_exists("stacks/monitor_capstone.yml"), "Monitoring compose file not found"
    
    def test_test_files(self):
        """Test if test files exist"""
        # Check for pytest files
        test_files_exist = False
        stdout, _, _ = run_command("find . -name 'test_*.py'")
        if stdout.strip():
            test_files_exist = True
            
        assert test_files_exist, "No test files found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/4-D.md"), "Debrief notes file not found"
        
        # Check if debrief contains alert rule rationale
        content = read_file_content("notes/4-D.md")
        assert re.search(r'alert|rule', content.lower()), "Debrief doesn't contain alert rule rationale"


class TestModule4E:
    """Tests for Module 4-E: Storytelling Launch"""
    
    def test_blog_post(self):
        """Test if blog post exists"""
        assert check_file_exists("docs/blog.md"), "Blog post not found"
    
    def test_screencast_link(self):
        """Test if README contains screencast link"""
        content = read_file_content("README.md")
        assert re.search(r'screencast|video|demo', content.lower()), "README doesn't link to screencast"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/4-E.md"), "Debrief notes file not found"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])