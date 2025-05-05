import os
import pytest
import re
from pathlib import Path
from utils import (
    run_command,
    check_file_exists,
    check_gpu_available,
    read_file_content
)

class TestModule3_1:
    """Tests for Module 3-1: Vector Add"""
    
    def test_source_exists(self):
        """Test if vector add source code exists"""
        assert check_file_exists("vec_add.cu"), "Vector add CUDA source not found"
    
    def test_binary_exists(self):
        """Test if compiled binary exists"""
        assert check_file_exists("vec_add"), "Compiled vector add binary not found"
    
    def test_binary_execution(self):
        """Test if binary can execute (requires GPU)"""
        if not check_gpu_available():
            pytest.skip("GPU not available, skipping execution test")
            
        stdout, stderr, retcode = run_command("./vec_add 1000000", timeout=5)
        assert retcode == 0, f"Failed to run vector add binary: {stderr}"
    
    def test_benchmark_script(self):
        """Test if numpy benchmark script exists"""
        assert check_file_exists("bench_numpy.py"), "NumPy benchmark script not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/3-1.md"), "Debrief notes file not found"
        
        # Check if debrief explains memory-bound nature
        content = read_file_content("notes/3-1.md")
        assert re.search(r'memory.bound', content), "Debrief doesn't explain memory-bound characteristics"


class TestModule3_2:
    """Tests for Module 3-2: Tiled Mat-Mul"""
    
    def test_source_exists(self):
        """Test if matrix multiplication source code exists"""
        assert check_file_exists("matmul.cu"), "Matrix multiplication CUDA source not found"
    
    def test_binary_exists(self):
        """Test if compiled binary exists"""
        assert check_file_exists("matmul"), "Compiled matrix multiplication binary not found"
    
    def test_binary_execution(self):
        """Test if binary can execute (requires GPU)"""
        if not check_gpu_available():
            pytest.skip("GPU not available, skipping execution test")
            
        stdout, stderr, retcode = run_command("./matmul 512", timeout=10)
        assert retcode == 0, f"Failed to run matrix multiplication binary: {stderr}"
    
    def test_nsys_available(self):
        """Test if Nsight Systems is available"""
        stdout, stderr, retcode = run_command("which nsys")
        assert retcode == 0, "Nsight Systems (nsys) not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/3-2.md"), "Debrief notes file not found"
        
        # Check if debrief includes tile size justification
        content = read_file_content("notes/3-2.md")
        assert re.search(r'tile size', content.lower()), "Debrief doesn't justify tile size choice"


class TestModule3_3:
    """Tests for Module 3-3: Occupancy Tuner"""
    
    def test_tuner_script(self):
        """Test if block tuner script exists"""
        assert check_file_exists("tune_blocks.sh"), "Block tuner script not found"
    
    def test_results_file(self):
        """Test if results CSV exists"""
        assert check_file_exists("blocks.csv"), "Block timing results CSV not found"
    
    def test_plot_script(self):
        """Test if plotting script exists"""
        assert check_file_exists("plot_blocks.py"), "Block size plotting script not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/3-3.md"), "Debrief notes file not found"
        
        # Check if debrief discusses occupancy
        content = read_file_content("notes/3-3.md")
        assert re.search(r'occupancy', content.lower()), "Debrief doesn't discuss occupancy"
        assert re.search(r'ILP|instruction level', content.lower()), "Debrief doesn't discuss ILP trade-offs"


class TestModule3_4:
    """Tests for Module 3-4: Warp Shuffle Reduction"""
    
    def test_source_exists(self):
        """Test if shuffle reduction source exists"""
        assert check_file_exists("reduce_shfl.cu"), "Warp shuffle reduction CUDA source not found"
    
    def test_binary_exists(self):
        """Test if compiled binary exists"""
        assert check_file_exists("reduce_shfl"), "Compiled shuffle reduction binary not found"
    
    def test_binary_execution(self):
        """Test if binary can execute (requires GPU)"""
        if not check_gpu_available():
            pytest.skip("GPU not available, skipping execution test")
            
        stdout, stderr, retcode = run_command("./reduce_shfl 10000", timeout=5)
        assert retcode == 0, f"Failed to run shuffle reduction binary: {stderr}"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/3-4.md"), "Debrief notes file not found"
        
        # Check if debrief explains shuffle vs shared memory
        content = read_file_content("notes/3-4.md")
        assert re.search(r'shuffle|shared memory', content.lower()), "Debrief doesn't explain shuffle vs shared memory"


class TestModule3_5:
    """Tests for Module 3-5: Prefix-Sum Scan"""
    
    def test_source_exists(self):
        """Test if scan source code exists"""
        assert check_file_exists("scan.cu"), "Scan CUDA source not found"
    
    def test_binary_exists(self):
        """Test if compiled binary exists"""
        assert check_file_exists("scan"), "Compiled scan binary not found"
    
    def test_binary_execution(self):
        """Test if binary can execute (requires GPU)"""
        if not check_gpu_available():
            pytest.skip("GPU not available, skipping execution test")
            
        stdout, stderr, retcode = run_command("./scan 10000", timeout=5)
        assert retcode == 0, f"Failed to run scan binary: {stderr}"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/3-5.md"), "Debrief notes file not found"
        
        # Check if debrief mentions synchronization
        content = read_file_content("notes/3-5.md")
        assert re.search(r'sync|block|multi', content.lower()), "Debrief doesn't discuss multi-block synchronization"


class TestModule3_6:
    """Tests for Module 3-6: Ring All-Reduce"""
    
    def test_nccl_tests_repo(self):
        """Test if NCCL tests repo is cloned"""
        assert check_file_exists("nccl-tests"), "NCCL tests repository not found"
    
    def test_nccl_test_binary(self):
        """Test if all_reduce_perf binary is built"""
        assert check_file_exists("build/all_reduce_perf"), "NCCL all_reduce_perf binary not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/3-6.md"), "Debrief notes file not found"
        
        # Check if debrief compares topologies
        content = read_file_content("notes/3-6.md")
        assert re.search(r'ring|tree|topolog', content.lower()), "Debrief doesn't compare ring vs tree topology"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])