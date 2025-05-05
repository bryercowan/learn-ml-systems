#!/usr/bin/env python3
"""
ML Systems Journey Test Structure Initializer
--------------------------------------------
This script creates the basic directory structure needed for tests.
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create the required directory structure for tests to run"""
    # Get the project root (assuming this script is in the tests directory)
    project_root = Path(__file__).parent.parent
    
    # Main directories
    directories = [
        "demos",
        "data",
        "scripts",
        "flows",
        "stacks",
        "docs",
        "snapshots",
        ".github/workflows",
        "infra",
        "gpu-workbench"
    ]
    
    # Create the directories
    for directory in directories:
        dir_path = project_root / directory
        if not dir_path.exists():
            print(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create empty notes directory with placeholder files for each module
    notes_dir = project_root / "notes"
    notes_dir.mkdir(exist_ok=True)
    
    # Create placeholder files for notes
    note_files = [
        # Module 0
        "00-A.md", "00-B.md", "M0-devbox.md",
        # Module 1
        "1-1.md", "1-2.md", "1-3.md", "1-4.md", "1-5.md", "1-6.md",
        # Module 2
        "2-1.md", "2-2.md",
        # Module 3
        "3-1.md", "3-2.md", "3-3.md", "3-4.md", "3-5.md", "3-6.md",
        # Module 4
        "4-A.md", "4-B.md", "4-C.md", "4-D.md", "4-E.md",
        # Optional modules
        "A-ledger.md", "B-workbench.md", "C-mlops.md"
    ]
    
    for note_file in note_files:
        note_path = notes_dir / note_file
        if not note_path.exists():
            print(f"Creating placeholder note: {note_path}")
            with open(note_path, 'w') as f:
                f.write(f"# Notes for {note_file.replace('.md', '')}\n\nPlace your notes here.\n")
    
    print("\nDirectory structure created successfully!")
    print("\nNext steps:")
    print("1. Install test dependencies: make setup-tests")
    print("2. Run tests for a specific module: make test-module-0")
    print("3. For more options, run: make list-tests")

if __name__ == "__main__":
    create_directory_structure()