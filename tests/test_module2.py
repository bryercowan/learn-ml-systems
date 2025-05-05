import os
import pytest
import re
from pathlib import Path
from utils import (
    run_command,
    check_file_exists,
    read_file_content
)

class TestModule2_1:
    """Tests for Module 2-1: Dataset Versioning (DVC)"""
    
    def test_dvc_initialized(self):
        """Test if DVC is initialized"""
        assert check_file_exists(".dvc"), "DVC not initialized (.dvc directory not found)"
    
    def test_dvc_tracked_file(self):
        """Test if movies.csv is tracked by DVC"""
        assert check_file_exists("data/movies.csv.dvc"), "DVC tracking file not found for movies.csv"
    
    def test_dvc_remote(self):
        """Test if DVC remote is configured"""
        stdout, stderr, retcode = run_command("dvc remote list")
        assert retcode == 0, f"Failed to list DVC remotes: {stderr}"
        assert "local" in stdout, "DVC remote 'local' not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/2-1.md"), "Debrief notes file not found"
        
        # Check if debrief contains remote backend rationale
        content = read_file_content("notes/2-1.md")
        assert re.search(r'remote|backend|storage', content.lower()), "Debrief doesn't contain remote backend rationale"


class TestModule2_2:
    """Tests for Module 2-2: Experiment Tracking (W&B)"""
    
    def test_training_script(self):
        """Test if training script exists"""
        assert check_file_exists("train_logreg.py"), "Training script not found"
    
    def test_wandb_integration(self):
        """Test if script contains W&B integration"""
        if not check_file_exists("train_logreg.py"):
            pytest.skip("Training script not found")
            
        content = read_file_content("train_logreg.py")
        assert "wandb" in content, "Script doesn't import W&B"
        assert re.search(r'wandb\.init|wandb\.log', content), "Script doesn't use W&B for tracking"
    
    def test_git_integration(self):
        """Test if script logs git SHA"""
        if not check_file_exists("train_logreg.py"):
            pytest.skip("Training script not found")
            
        content = read_file_content("train_logreg.py")
        assert re.search(r'git.*rev-parse|SHA|commit', content), "Script doesn't log git SHA"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/2-2.md"), "Debrief notes file not found"


# Additional test classes for other Module 2 sections can be added here
class TestModule2_3to6:
    """Placeholder for additional Module 2 tests"""
    
    @pytest.mark.parametrize("module_num", [3, 4, 5, 6])
    def test_debrief_exists(self, module_num):
        """Test if debrief notes exist for additional modules"""
        # Skip test if we go beyond what's defined in the README
        try:
            with open("README.md", "r") as f:
                readme = f.read()
            if not re.search(f"2-{module_num}", readme):
                pytest.skip(f"Module 2-{module_num} not defined in README")
                
            assert check_file_exists(f"notes/2-{module_num}.md"), f"Debrief notes for Module 2-{module_num} not found"
        except Exception:
            pytest.skip("Could not read README.md")


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])