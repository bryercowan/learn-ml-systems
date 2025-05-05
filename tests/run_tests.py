#!/usr/bin/env python3
"""
ML Systems Journey Test Runner
-----------------------------
This script runs all tests for the ML Systems Journey curriculum.
"""

import os
import sys
import time
import json
import argparse
import pytest
import subprocess
import datetime
from pathlib import Path
from termcolor import colored
from datetime import datetime

# Make sure the tests directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run tests for ML Systems Journey curriculum")
    parser.add_argument("--module", "-m", type=str, help="Specific module to test (e.g., 0, 1, 2, 3, 4, A, B, C)")
    parser.add_argument("--sub-module", "-s", type=str, help="Specific sub-module to test (e.g., 1, 2, A, B)")
    parser.add_argument("--container", "-c", action="store_true", help="Run tests inside container (for CUDA tests)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--all", "-a", action="store_true", help="Run all tests including optional modules")
    parser.add_argument("--list", "-l", action="store_true", help="List all available tests")
    parser.add_argument("--report", "-r", type=str, help="Generate a test report in the specified format (json, txt, html)")
    parser.add_argument("--output", "-o", type=str, help="Output file for the report (default: test_report.<format>)")
    parser.add_argument("--junit", "-j", action="store_true", help="Generate JUnit XML report (for CI integration)")
    return parser.parse_args()

def get_test_files(module=None):
    """Get all test files for a specific module or all modules"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    if module:
        # For numeric modules
        if module.isdigit():
            return [os.path.join(test_dir, f"test_module{module}.py")]
        # For optional modules (A, B, C)
        else:
            return [os.path.join(test_dir, "test_optional_modules.py")]
    
    # All core modules
    core_modules = [os.path.join(test_dir, f"test_module{i}.py") for i in range(5)]
    
    # Add optional modules if they exist
    optional_modules = [os.path.join(test_dir, "test_optional_modules.py")]
    
    return core_modules + optional_modules

def list_available_tests():
    """List all available tests"""
    print(colored("Available tests:", "cyan", attrs=["bold"]))
    print(colored("\nCore Modules:", "green", attrs=["bold"]))
    print(colored("  Module 0: Course Setup", "yellow"))
    print("    0-A: Course Setup")
    print("    0-B: Kafka Hello-World")
    print("    M0: DevBox Skeleton")
    
    print(colored("\n  Module 1: Data-Plumbing Fundamentals", "yellow"))
    print("    1-1: Reliability Queue Chaos")
    print("    1-2: SQL vs Document Benchmark")
    print("    1-3 through 1-6: Additional Data Lessons")
    
    print(colored("\n  Module 2: ML-Workflow Glue", "yellow"))
    print("    2-1: Dataset Versioning (DVC)")
    print("    2-2: Experiment Tracking (W&B)")
    print("    Additional sections as defined in README")
    
    print(colored("\n  Module 3: GPU-Performance Mindset", "yellow"))
    print("    3-1: Vector Add")
    print("    3-2: Tiled Mat-Mul")
    print("    3-3: Occupancy Tuner")
    print("    3-4: Warp Shuffle Reduction")
    print("    3-5: Prefix-Sum Scan")
    print("    3-6: Ring All-Reduce")
    
    print(colored("\n  Module 4: Capstone 'Vector-Aware Fine-Tuner'", "yellow"))
    print("    4-A: Data Plane Ready")
    print("    4-B: Training Pipeline")
    print("    4-C: Model Serving")
    print("    4-D: Observability & CI")
    print("    4-E: Storytelling Launch")
    
    print(colored("\nOptional Modules:", "green", attrs=["bold"]))
    print("  Module A: DDIA 7-12 Bank-grade Ledger")
    print("  Module B: PMPP 1 & 7-23 GPU Workbench")
    print("  Module C: ml-eng Extras Project 'Prod-Ready MLOps'")

class TestReporter:
    """Generate formatted test reports"""
    def __init__(self, report_format=None, output_path=None):
        self.report_format = report_format
        self.output_path = output_path or f"test_report.{report_format}"
        self.start_time = time.time()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "modules": {},
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 0
            }
        }
    
    def record_result(self, module, test_name, result, duration, message=None):
        """Record a test result"""
        if module not in self.results["modules"]:
            self.results["modules"][module] = {
                "tests": [],
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 0
            }
        
        self.results["modules"][module]["tests"].append({
            "name": test_name,
            "result": result,
            "duration": duration,
            "message": message
        })
        
        # Update module stats
        self.results["modules"][module][result] += 1
        self.results["modules"][module]["duration"] += duration
        
        # Update overall stats
        self.results["summary"]["total"] += 1
        self.results["summary"][result] += 1
    
    def finalize(self):
        """Finalize the report"""
        self.results["summary"]["duration"] = time.time() - self.start_time
        
        if not self.report_format:
            return
            
        if self.report_format == "json":
            self._generate_json_report()
        elif self.report_format == "txt":
            self._generate_text_report()
        elif self.report_format == "html":
            self._generate_html_report()
    
    def _generate_json_report(self):
        """Generate a JSON report"""
        with open(self.output_path, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\nJSON report saved to {self.output_path}")
    
    def _generate_text_report(self):
        """Generate a text report"""
        with open(self.output_path, "w") as f:
            f.write("ML Systems Journey Test Report\n")
            f.write("============================\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration: {self.results['summary']['duration']:.2f} seconds\n\n")
            
            f.write("Summary:\n")
            f.write(f"  Total Tests: {self.results['summary']['total']}\n")
            f.write(f"  Passed: {self.results['summary']['passed']}\n")
            f.write(f"  Failed: {self.results['summary']['failed']}\n")
            f.write(f"  Skipped: {self.results['summary']['skipped']}\n\n")
            
            f.write("Module Results:\n")
            for module, data in self.results["modules"].items():
                f.write(f"\nModule {module}:\n")
                f.write(f"  Tests: {len(data['tests'])}\n")
                f.write(f"  Passed: {data['passed']}\n")
                f.write(f"  Failed: {data['failed']}\n")
                f.write(f"  Skipped: {data['skipped']}\n")
                f.write(f"  Duration: {data['duration']:.2f} seconds\n\n")
                
                f.write("  Test Details:\n")
                for test in data["tests"]:
                    result_str = "PASS" if test["result"] == "passed" else "FAIL" if test["result"] == "failed" else "SKIP"
                    f.write(f"    {test['name']}: {result_str} ({test['duration']:.2f}s)\n")
                    if test["message"]:
                        f.write(f"      Message: {test['message']}\n")
        
        print(f"\nText report saved to {self.output_path}")
    
    def _generate_html_report(self):
        """Generate an HTML report"""
        template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ML Systems Journey Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        h1 { color: #333; }
        .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .module { margin-bottom: 30px; border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }
        .module-header { background-color: #eee; padding: 10px 15px; }
        .module-body { padding: 15px; }
        .test-item { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
        .test-name { font-weight: bold; }
        .pass { color: green; }
        .fail { color: red; }
        .skip { color: orange; }
        .message { margin-top: 5px; font-style: italic; color: #666; }
    </style>
</head>
<body>
    <h1>ML Systems Journey Test Report</h1>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Date: {date}</p>
        <p>Duration: {duration:.2f} seconds</p>
        <p>Total Tests: {total}</p>
        <p>Passed: <span class="pass">{passed}</span></p>
        <p>Failed: <span class="fail">{failed}</span></p>
        <p>Skipped: <span class="skip">{skipped}</span></p>
    </div>
    
    <h2>Module Results</h2>
    
    {module_results}
</body>
</html>
"""
        
        module_template = """
    <div class="module">
        <div class="module-header">
            <h3>Module {module}</h3>
            <p>Tests: {total} | Passed: <span class="pass">{passed}</span> | Failed: <span class="fail">{failed}</span> | Skipped: <span class="skip">{skipped}</span> | Duration: {duration:.2f}s</p>
        </div>
        <div class="module-body">
            {test_results}
        </div>
    </div>
"""
        
        test_template = """
            <div class="test-item">
                <div class="test-name">
                    {name}: <span class="{result_class}">{result_str}</span> ({duration:.2f}s)
                </div>
                {message_html}
            </div>
"""
        
        # Generate module results
        module_results = []
        for module, data in self.results["modules"].items():
            test_results = []
            for test in data["tests"]:
                result_str = "PASS" if test["result"] == "passed" else "FAIL" if test["result"] == "failed" else "SKIP"
                result_class = "pass" if test["result"] == "passed" else "fail" if test["result"] == "failed" else "skip"
                message_html = f'<div class="message">{test["message"]}</div>' if test["message"] else ""
                
                test_results.append(test_template.format(
                    name=test["name"],
                    result_str=result_str,
                    result_class=result_class,
                    duration=test["duration"],
                    message_html=message_html
                ))
            
            module_results.append(module_template.format(
                module=module,
                total=len(data["tests"]),
                passed=data["passed"],
                failed=data["failed"],
                skipped=data["skipped"],
                duration=data["duration"],
                test_results="".join(test_results)
            ))
        
        # Fill the template
        html = template.format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            duration=self.results["summary"]["duration"],
            total=self.results["summary"]["total"],
            passed=self.results["summary"]["passed"],
            failed=self.results["summary"]["failed"],
            skipped=self.results["summary"]["skipped"],
            module_results="".join(module_results)
        )
        
        with open(self.output_path, "w") as f:
            f.write(html)
        
        print(f"\nHTML report saved to {self.output_path}")


class CustomPytestPlugin:
    """Custom pytest plugin to capture test results for reporting"""
    def __init__(self, reporter=None):
        self.reporter = reporter
    
    def pytest_runtest_logreport(self, report):
        """Process test report"""
        if report.when == "call" or (report.when == "setup" and report.skipped):
            # Extract module and test names
            module_name = report.nodeid.split("::")[0].replace("test_module", "").replace("test_optional_modules.py", "")
            module_name = module_name.replace(".py", "")
            if "TestModule" in report.nodeid:
                # Extract from test class
                class_name = report.nodeid.split("::")[1]
                test_name = report.nodeid.split("::")[2]
                
                # Clean up module name based on class name
                if class_name.startswith("TestModule"):
                    if module_name.isdigit() or module_name == "":
                        # For core modules
                        module_cls = class_name.replace("TestModule", "")
                        module_name = module_cls.split("_")[0]
                    else:
                        # For optional modules
                        module_name = class_name.replace("TestModule", "")
            else:
                # Simple test function
                test_name = report.nodeid.split("::")[1]
            
            # Determine result and message
            if report.skipped:
                result = "skipped"
                message = report.longrepr[2] if report.longrepr else None
            elif report.failed:
                result = "failed"
                message = str(report.longrepr) if report.longrepr else None
            else:
                result = "passed"
                message = None
            
            # Record result if reporter exists
            if self.reporter:
                self.reporter.record_result(
                    module=module_name,
                    test_name=test_name,
                    result=result,
                    duration=report.duration,
                    message=message
                )

def run_tests(args):
    """Run the specified tests"""
    if args.list:
        list_available_tests()
        return 0
    
    # Initialize test reporter if reports requested
    reporter = None
    if args.report:
        reporter = TestReporter(report_format=args.report, output_path=args.output)
    
    # Initialize pytest plugin
    plugin = CustomPytestPlugin(reporter)
    
    # Prepare pytest arguments
    test_args = ["-v"] if args.verbose else []
    
    # Add JUnit XML report if requested
    if args.junit:
        junit_path = args.output or "junit_report.xml"
        test_args.extend(["--junitxml", junit_path])
    
    # Handle container mode for CUDA tests
    if args.container:
        os.environ["IN_CONTAINER"] = "1"
    
    # Handle specific module and sub-module
    if args.module:
        module = args.module
        
        # Get the appropriate test file
        test_files = get_test_files(module)
        
        # Add specific sub-module if provided
        if args.sub_module:
            sub_module = args.sub_module
            if module.isdigit():
                # For core modules
                test_args.extend(["-k", f"TestModule{module}_{sub_module}"])
            else:
                # For optional modules
                test_args.extend(["-k", f"TestModule{module}"])
    else:
        # Run all core modules by default, or all modules if --all specified
        test_files = get_test_files()
        if not args.all:
            # Exclude optional modules
            test_files = [f for f in test_files if "optional" not in f]
    
    # Add test files to pytest arguments
    test_args.extend(test_files)
    
    # Print test environment information
    print(colored("\nML Systems Journey Test Runner", "cyan", attrs=["bold"]))
    print(colored("--------------------------------", "cyan"))
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Running tests with Python {sys.version.split()[0]}")
    print(f"In container: {'Yes' if args.container else 'No'}")
    print(f"Modules: {args.module or 'All'}")
    if args.sub_module:
        print(f"Sub-module: {args.sub_module}")
    print(colored("--------------------------------\n", "cyan"))
    
    # Run the tests with our custom plugin
    result = pytest.main(test_args, plugins=[plugin])
    
    # Finalize reporting
    if reporter:
        reporter.finalize()
    
    # Print summary
    if reporter:
        total = reporter.results["summary"]["total"]
        passed = reporter.results["summary"]["passed"]
        failed = reporter.results["summary"]["failed"]
        skipped = reporter.results["summary"]["skipped"]
        duration = reporter.results["summary"]["duration"]
        
        print(colored("\nTest Summary:", "cyan", attrs=["bold"]))
        print(f"Total Tests: {total}")
        print(colored(f"Passed: {passed}", "green" if passed > 0 else "white"))
        print(colored(f"Failed: {failed}", "red" if failed > 0 else "white"))
        print(colored(f"Skipped: {skipped}", "yellow" if skipped > 0 else "white"))
        print(f"Duration: {duration:.2f} seconds")
    
    return result

if __name__ == "__main__":
    try:
        # Attempt to load termcolor for colored output
        # If not available, define a colored function that simply returns the text
        from termcolor import colored
    except ImportError:
        def colored(text, *args, **kwargs):
            return text
    
    args = parse_args()
    sys.exit(run_tests(args))