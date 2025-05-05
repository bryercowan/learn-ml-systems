import os
import pytest
import re
from pathlib import Path
from utils import (
    run_command,
    check_file_exists,
    check_container_running,
    read_file_content
)

class TestModuleA:
    """Tests for Optional Module A: DDIA 7-12 Bank-grade Ledger"""
    
    def test_compose_file(self):
        """Test if ledger compose file exists"""
        assert check_file_exists("stacks/ledger.yml"), "Ledger compose file not found"
    
    def test_ledger_api(self):
        """Test if ledger API exists"""
        assert check_file_exists("src/ledger_api") or check_file_exists("crates/ledger_api"), "Ledger API source not found"
    
    def test_simulation_script(self):
        """Test if simulation script exists"""
        assert check_file_exists("simulate_transfers.py"), "Transfer simulation script not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/A-ledger.md"), "Architecture report not found"
        
        # Check if report is substantive
        content = read_file_content("notes/A-ledger.md")
        word_count = len(re.findall(r'\b\w+\b', content))
        assert word_count >= 400, f"Architecture report too short: {word_count} words (should be ~500)"


class TestModuleB:
    """Tests for Optional Module B: PMPP 1 & 7-23 GPU Workbench"""
    
    def test_workbench_directory(self):
        """Test if GPU workbench directory exists"""
        assert check_directory_exists("gpu-workbench"), "GPU workbench directory not found"
    
    def test_bootstrap_script(self):
        """Test if bootstrap script exists"""
        assert check_file_exists("gpu-workbench/bootstrap.sh"), "Bootstrap script not found"
    
    def test_benchmark_script(self):
        """Test if benchmark script exists"""
        assert check_file_exists("gpu-workbench/run_all_bench.sh"), "Benchmark script not found"
    
    def test_results_file(self):
        """Test if results are generated"""
        assert check_file_exists("gpu-workbench/results.md"), "Benchmark results file not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/B-workbench.md"), "Workbench optimizations summary not found"

    def check_directory_exists(self, path):
        """Helper to check if directory exists"""
        return os.path.isdir(path)


class TestModuleC:
    """Tests for Optional Module C: ml-eng Extras Project 'Prod-Ready MLOps'"""
    
    def test_workflow_file(self):
        """Test if CD workflow exists"""
        assert check_file_exists(".github/workflows/cd.yml"), "CD workflow file not found"
    
    def test_deployment_script(self):
        """Test if blue-green deployment script exists"""
        assert check_file_exists("infra/deploy_blue_green.sh"), "Blue-green deployment script not found"
    
    def test_feast_configs(self):
        """Test if Feast feature store configs exist"""
        assert check_file_exists("feature_store.yaml") or check_file_exists("feast.yaml"), "Feast configuration not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/C-mlops.md"), "MLOps lessons summary not found"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])