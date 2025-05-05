#!/usr/bin/env python3
"""
ML Systems Journey CUDA Test Helpers
------------------------------------
This module provides helper functions for GPU/CUDA-specific testing.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

class CudaTestHelper:
    """Helper class for CUDA testing"""
    
    @staticmethod
    def get_gpu_info():
        """Get information about the available GPU"""
        try:
            # Use nvidia-smi to get GPU info
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,compute_cap,memory.total", "--format=csv,noheader"],
                capture_output=True, text=True, check=True
            )
            
            # Parse the output
            output = result.stdout.strip()
            if not output:
                return None
                
            # Parse the comma-separated values
            parts = [p.strip() for p in output.split(",")]
            
            return {
                "name": parts[0],
                "compute_capability": parts[1],
                "memory_total": parts[2]
            }
        except (subprocess.SubprocessError, IndexError):
            return None
    
    @staticmethod
    def get_cuda_version():
        """Get the CUDA version"""
        try:
            # Try nvcc first
            result = subprocess.run(
                ["nvcc", "--version"],
                capture_output=True, text=True, check=True
            )
            
            # Parse the version
            match = re.search(r'release\s+(\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
                
            # If that fails, try nvidia-smi
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                capture_output=True, text=True, check=True
            )
            
            return result.stdout.strip()
        except subprocess.SubprocessError:
            return "unknown"
    
    @staticmethod
    def compile_cuda_program(source_path, output_path, options=None):
        """
        Compile a CUDA program
        
        Args:
            source_path: Path to the source file
            output_path: Path for the compiled binary
            options: Additional compiler options
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        cmd = ["nvcc", "-o", str(output_path), str(source_path)]
        
        # Add optimization
        cmd.append("-O3")
        
        # Add any additional options
        if options:
            if isinstance(options, list):
                cmd.extend(options)
            else:
                cmd.append(options)
        
        # Run the compilation
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            return (
                result.returncode == 0,
                result.stdout,
                result.stderr
            )
        except Exception as e:
            return (False, "", str(e))
    
    @staticmethod
    def run_cuda_program(binary_path, arguments=None, timeout=30):
        """
        Run a compiled CUDA program
        
        Args:
            binary_path: Path to the compiled binary
            arguments: Command-line arguments to pass
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        cmd = [str(binary_path)]
        
        # Add any arguments
        if arguments:
            if isinstance(arguments, list):
                cmd.extend(arguments)
            else:
                cmd.append(arguments)
        
        # Run the program
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout
            )
            
            return (
                result.returncode == 0,
                result.stdout,
                result.stderr
            )
        except subprocess.TimeoutExpired:
            return (False, "", f"Timeout expired after {timeout} seconds")
        except Exception as e:
            return (False, "", str(e))
    
    @staticmethod
    def profile_cuda_program(binary_path, arguments=None, timeout=60):
        """
        Profile a CUDA program using Nsight Systems
        
        Args:
            binary_path: Path to the compiled binary
            arguments: Command-line arguments to pass
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (success, report_path, error_message)
        """
        # Create a temporary directory for the report
        report_dir = tempfile.mkdtemp()
        report_path = os.path.join(report_dir, "profile.qdrep")
        
        cmd = ["nsys", "profile", "-o", report_path]
        
        # Add the binary and its arguments
        cmd.append(str(binary_path))
        if arguments:
            if isinstance(arguments, list):
                cmd.extend(arguments)
            else:
                cmd.append(arguments)
        
        # Run the profiler
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return (True, report_path, "")
            else:
                return (False, "", result.stderr)
        except subprocess.TimeoutExpired:
            return (False, "", f"Profiling timeout expired after {timeout} seconds")
        except Exception as e:
            return (False, "", str(e))
    
    @staticmethod
    def calculate_theoretical_bandwidth(gpu_info=None):
        """
        Calculate theoretical memory bandwidth based on GPU info
        
        Returns:
            Bandwidth in GB/s
        """
        if not gpu_info:
            gpu_info = CudaTestHelper.get_gpu_info()
            
        # If we couldn't get GPU info, use a reasonable default
        if not gpu_info:
            return 400.0  # Default value, reasonable for recent GPUs
        
        # For accurate calculation, we would need memory clock and bus width
        # Since nvidia-smi doesn't provide this directly, we just return
        # a reasonable estimate based on the GPU name
        
        # Check for common GPU families and provide estimates
        name = gpu_info["name"].lower()
        
        if "a100" in name:
            return 1600.0  # ~1.6 TB/s
        elif "h100" in name:
            return 2000.0  # ~2 TB/s
        elif "v100" in name:
            return 900.0   # ~900 GB/s
        elif "40" in name or "30" in name:  # RTX 30xx or 40xx
            return 800.0   # Conservative estimate
        elif "20" in name:  # RTX 20xx
            return 500.0
        else:
            return 400.0  # Default fallback
    
    @staticmethod
    def verify_output(expected, actual, relative_tolerance=1e-5):
        """
        Verify numeric output from a CUDA program
        
        Args:
            expected: Expected output (string or number)
            actual: Actual output (string or number)
            relative_tolerance: Relative tolerance for floating-point comparison
            
        Returns:
            True if outputs match, False otherwise
        """
        # Convert to floats if possible
        try:
            expected_float = float(expected)
            actual_float = float(actual)
            
            # Calculate relative difference
            if expected_float == 0:
                return abs(actual_float) < relative_tolerance
            
            relative_diff = abs((expected_float - actual_float) / expected_float)
            return relative_diff <= relative_tolerance
        except (ValueError, TypeError):
            # If not numeric, do string comparison
            return str(expected).strip() == str(actual).strip()