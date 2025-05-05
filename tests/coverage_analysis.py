#!/usr/bin/env python3
"""
ML Systems Journey Test Coverage Analysis
-----------------------------------------
This script analyzes test coverage for the ML Systems Journey curriculum.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict
import re

# Make sure the tests directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analyze test coverage for ML Systems Journey curriculum")
    parser.add_argument("--json", "-j", type=str, help="Path to JSON report from test run (if not provided, will run tests)")
    parser.add_argument("--output", "-o", type=str, default="coverage_report", help="Output directory for coverage reports")
    parser.add_argument("--format", "-f", type=str, choices=["text", "html", "json"], default="html", 
                       help="Output format (text, html, json)")
    parser.add_argument("--visualize", "-v", action="store_true", help="Generate visualization charts")
    return parser.parse_args()

def run_tests_with_coverage():
    """Run tests with coverage and return the test report"""
    from run_tests import run_tests
    
    # Create a TestReporter
    from run_tests import TestReporter
    reporter = TestReporter(report_format="json", output_path="temp_coverage_report.json")
    
    # Create arguments object with required properties
    class Args:
        pass
    
    args = Args()
    args.report = "json"
    args.output = "temp_coverage_report.json"
    args.verbose = False
    args.container = False
    args.all = True
    args.junit = False
    args.list = False
    args.module = None
    args.sub_module = None
    
    # Run tests
    run_tests(args)
    
    # Load the JSON report
    with open("temp_coverage_report.json", "r") as f:
        report = json.load(f)
    
    # Clean up
    os.remove("temp_coverage_report.json")
    
    return report

def analyze_readme_tasks():
    """Analyze the README to identify all tasks that should be tested"""
    tasks = defaultdict(list)
    
    # Check if README exists
    if not os.path.exists("README.md"):
        print("WARNING: README.md not found. Task analysis incomplete.")
        return tasks
    
    # Read README
    with open("README.md", "r") as f:
        content = f.read()
    
    # Extract module sections
    module_pattern = r"#+\s+Module\s+(\d+)[:\s-]+([^\n]+)"
    modules = re.finditer(module_pattern, content, re.IGNORECASE)
    
    current_module = None
    for line in content.split("\n"):
        # Check for module header
        module_match = re.search(r"#+\s+Module\s+(\d+)[:\s-]+([^\n]+)", line, re.IGNORECASE)
        if module_match:
            current_module = module_match.group(1)
            continue
            
        # Check for sub-module or task
        task_match = re.search(r"[*-]\s+(\d+[.-]\d+|\d+[.-][A-Z])\s+([^\n]+)", line)
        if task_match and current_module:
            task_id = task_match.group(1)
            task_name = task_match.group(2).strip()
            
            # Add to tasks
            tasks[current_module].append({
                "id": task_id,
                "name": task_name
            })
    
    return tasks

def analyze_test_coverage(test_report, tasks):
    """Analyze test coverage based on test report and expected tasks"""
    coverage = {
        "summary": {
            "total_tasks": 0,
            "covered_tasks": 0,
            "coverage_percent": 0
        },
        "modules": {}
    }
    
    # Count total expected tasks
    total_tasks = 0
    for module, module_tasks in tasks.items():
        total_tasks += len(module_tasks)
    
    coverage["summary"]["total_tasks"] = total_tasks
    
    # Analyze test report
    covered_tasks = 0
    for module_id, module_data in test_report["modules"].items():
        # Skip any non-numeric module IDs
        if not module_id.isdigit():
            continue
        
        # Initialize module coverage data
        if module_id not in coverage["modules"]:
            coverage["modules"][module_id] = {
                "total_tasks": len(tasks.get(module_id, [])),
                "covered_tasks": 0,
                "coverage_percent": 0,
                "tasks": []
            }
        
        # Count covered tasks for this module
        task_ids = set()
        for test in module_data["tests"]:
            # Extract task ID from test name if possible
            task_match = re.search(r"test_module\d+_(\d+)", test["name"])
            if task_match:
                task_id = task_match.group(1)
                task_ids.add(task_id)
        
        covered_module_tasks = len(task_ids)
        coverage["modules"][module_id]["covered_tasks"] = covered_module_tasks
        
        # Calculate coverage percentage
        total_module_tasks = coverage["modules"][module_id]["total_tasks"]
        if total_module_tasks > 0:
            coverage_percent = (covered_module_tasks / total_module_tasks) * 100
        else:
            coverage_percent = 0
            
        coverage["modules"][module_id]["coverage_percent"] = coverage_percent
        
        # Add to total covered tasks
        covered_tasks += covered_module_tasks
    
    # Calculate overall coverage percentage
    if total_tasks > 0:
        coverage_percent = (covered_tasks / total_tasks) * 100
    else:
        coverage_percent = 0
        
    coverage["summary"]["covered_tasks"] = covered_tasks
    coverage["summary"]["coverage_percent"] = coverage_percent
    
    return coverage

def generate_text_report(coverage, output_file):
    """Generate a text coverage report"""
    with open(output_file, "w") as f:
        f.write("ML Systems Journey Test Coverage Report\n")
        f.write("======================================\n\n")
        
        # Summary
        f.write("Summary:\n")
        f.write(f"  Total Tasks: {coverage['summary']['total_tasks']}\n")
        f.write(f"  Covered Tasks: {coverage['summary']['covered_tasks']}\n")
        f.write(f"  Coverage: {coverage['summary']['coverage_percent']:.1f}%\n\n")
        
        # Per-module coverage
        f.write("Module Coverage:\n")
        for module_id, module_data in sorted(coverage["modules"].items()):
            f.write(f"  Module {module_id}:\n")
            f.write(f"    Total Tasks: {module_data['total_tasks']}\n")
            f.write(f"    Covered Tasks: {module_data['covered_tasks']}\n")
            f.write(f"    Coverage: {module_data['coverage_percent']:.1f}%\n\n")

def generate_html_report(coverage, output_file):
    """Generate an HTML coverage report"""
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ML Systems Journey Test Coverage Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        h1, h2 { color: #333; }
        .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .module { margin-bottom: 20px; }
        .progress-container { width: 100%; background-color: #ddd; border-radius: 4px; margin: 10px 0; }
        .progress-bar { height: 20px; border-radius: 4px; text-align: center; color: white; line-height: 20px; }
        .high { background-color: #4CAF50; }
        .medium { background-color: #FFEB3B; color: #333; }
        .low { background-color: #F44336; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>ML Systems Journey Test Coverage Report</h1>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Tasks: {total_tasks}</p>
        <p>Covered Tasks: {covered_tasks}</p>
        <div class="progress-container">
            <div class="progress-bar {summary_class}" style="width: {coverage_percent}%">
                {coverage_percent:.1f}%
            </div>
        </div>
    </div>
    
    <h2>Module Coverage</h2>
    
    {module_coverage}
</body>
</html>
"""
    
    module_template = """
    <div class="module">
        <h3>Module {module_id}</h3>
        <p>Total Tasks: {total_tasks}</p>
        <p>Covered Tasks: {covered_tasks}</p>
        <div class="progress-container">
            <div class="progress-bar {coverage_class}" style="width: {coverage_percent}%">
                {coverage_percent:.1f}%
            </div>
        </div>
    </div>
"""
    
    # Generate module coverage HTML
    module_coverage_html = []
    for module_id, module_data in sorted(coverage["modules"].items()):
        # Determine coverage class
        coverage_percent = module_data["coverage_percent"]
        if coverage_percent >= 80:
            coverage_class = "high"
        elif coverage_percent >= 50:
            coverage_class = "medium"
        else:
            coverage_class = "low"
        
        module_coverage_html.append(module_template.format(
            module_id=module_id,
            total_tasks=module_data["total_tasks"],
            covered_tasks=module_data["covered_tasks"],
            coverage_percent=coverage_percent,
            coverage_class=coverage_class
        ))
    
    # Determine summary coverage class
    summary_percent = coverage["summary"]["coverage_percent"]
    if summary_percent >= 80:
        summary_class = "high"
    elif summary_percent >= 50:
        summary_class = "medium"
    else:
        summary_class = "low"
    
    # Generate complete HTML
    html = html_template.format(
        total_tasks=coverage["summary"]["total_tasks"],
        covered_tasks=coverage["summary"]["covered_tasks"],
        coverage_percent=summary_percent,
        summary_class=summary_class,
        module_coverage="".join(module_coverage_html)
    )
    
    with open(output_file, "w") as f:
        f.write(html)

def generate_visualizations(coverage, output_dir):
    """Generate coverage visualization charts"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Data for charts
    modules = []
    coverage_percents = []
    
    for module_id, module_data in sorted(coverage["modules"].items()):
        modules.append(f"Module {module_id}")
        coverage_percents.append(module_data["coverage_percent"])
    
    # Module coverage bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(modules, coverage_percents, color='skyblue')
    
    # Color bars based on coverage
    for i, bar in enumerate(bars):
        if coverage_percents[i] >= 80:
            bar.set_color('green')
        elif coverage_percents[i] >= 50:
            bar.set_color('yellow')
        else:
            bar.set_color('red')
    
    plt.axhline(y=80, color='green', linestyle='--', alpha=0.7, label='Target (80%)')
    plt.axhline(y=coverage["summary"]["coverage_percent"], color='black', linestyle='-', alpha=0.5, label='Average')
    
    plt.title('Test Coverage by Module')
    plt.xlabel('Module')
    plt.ylabel('Coverage (%)')
    plt.ylim(0, 105)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "module_coverage.png"))
    
    # Overall coverage pie chart
    plt.figure(figsize=(8, 8))
    covered = coverage["summary"]["covered_tasks"]
    uncovered = coverage["summary"]["total_tasks"] - covered
    
    labels = ['Covered', 'Uncovered']
    sizes = [covered, uncovered]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)  # explode 1st slice
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Overall Test Coverage')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "overall_coverage.png"))
    
    # Close all figures
    plt.close('all')

def main():
    """Main function"""
    args = parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Get test report
    if args.json and os.path.exists(args.json):
        with open(args.json, "r") as f:
            test_report = json.load(f)
    else:
        print("Running tests to generate coverage data...")
        test_report = run_tests_with_coverage()
    
    # Analyze README for tasks
    print("Analyzing curriculum tasks...")
    tasks = analyze_readme_tasks()
    
    # Analyze test coverage
    print("Analyzing test coverage...")
    coverage = analyze_test_coverage(test_report, tasks)
    
    # Generate reports
    output_base = os.path.join(args.output, "coverage")
    
    if args.format == "text":
        print("Generating text report...")
        generate_text_report(coverage, f"{output_base}.txt")
        print(f"Text report saved to {output_base}.txt")
        
    elif args.format == "html":
        print("Generating HTML report...")
        generate_html_report(coverage, f"{output_base}.html")
        print(f"HTML report saved to {output_base}.html")
        
    elif args.format == "json":
        print("Generating JSON report...")
        with open(f"{output_base}.json", "w") as f:
            json.dump(coverage, f, indent=2)
        print(f"JSON report saved to {output_base}.json")
    
    # Generate visualizations if requested
    if args.visualize:
        try:
            print("Generating visualizations...")
            generate_visualizations(coverage, args.output)
            print(f"Visualizations saved to {args.output}")
        except ImportError:
            print("WARNING: matplotlib not installed. Skipping visualizations.")
    
    # Print summary
    print("\nTest Coverage Summary:")
    print(f"  Total Tasks: {coverage['summary']['total_tasks']}")
    print(f"  Covered Tasks: {coverage['summary']['covered_tasks']}")
    print(f"  Coverage: {coverage['summary']['coverage_percent']:.1f}%")

if __name__ == "__main__":
    main()