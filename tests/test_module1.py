import os
import pytest
import json
import re
from pathlib import Path
from utils import (
    run_command,
    check_file_exists,
    check_container_running,
    read_file_content
)

class TestModule1_1:
    """Tests for Module 1-1: Reliability Queue Chaos"""
    
    def test_asciinema_recording(self):
        """Test if asciinema recording exists"""
        assert check_file_exists("demos/1-1.cast"), "Asciinema recording not found"
    
    def test_recording_content(self):
        """Test if recording shows proper recovery"""
        if not check_file_exists("demos/1-1.cast"):
            pytest.skip("Recording file not found")
            
        cast_content = read_file_content("demos/1-1.cast")
        # Check for expected patterns in recording
        assert "kafka" in cast_content.lower(), "Recording doesn't mention Kafka"
        
        # We'd ideally parse the JSON structure of the cast file
        # For simplicity, we're just checking for keywords
        assert "consumer" in cast_content.lower(), "Recording doesn't mention consumer"
        assert re.search(r'restart|recover', cast_content.lower()), "No evidence of recovery in recording"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/1-1.md"), "Debrief notes file not found"


class TestModule1_2:
    """Tests for Module 1-2: SQL vs Document Benchmark"""
    
    def test_dataset_exists(self):
        """Test if movies.csv exists"""
        assert check_file_exists("data/movies.csv"), "Movies dataset not found"
    
    def test_sqlite_db(self):
        """Test if SQLite database exists"""
        assert check_file_exists("movies.db"), "SQLite database not found"
    
    def test_mongo_container(self):
        """Test if MongoDB container is running"""
        assert check_container_running("mongo"), "MongoDB container is not running"
    
    def test_query_scripts(self):
        """Test if query scripts exist"""
        assert check_file_exists("scripts/query_sql.py"), "SQL query script not found"
        assert check_file_exists("scripts/query_mongo.py"), "MongoDB query script not found"
    
    def test_debrief_exists(self):
        """Test if debrief notes exist"""
        assert check_file_exists("notes/1-2.md"), "Debrief notes file not found"
        
        # Check if debrief contains comparison data
        content = read_file_content("notes/1-2.md")
        assert re.search(r'latenc(y|ies)|performance|timing', content.lower()), "Debrief doesn't contain performance comparison"


# Add similar test classes for modules 1-3 through 1-6
class TestModule1_3to6:
    """Placeholder for tests for Modules 1-3 through 1-6"""
    
    @pytest.mark.parametrize("module_num", [3, 4, 5, 6])
    def test_module_debriefs(self, module_num):
        """Test if debrief notes exist for each module"""
        assert check_file_exists(f"notes/1-{module_num}.md"), f"Debrief notes for Module 1-{module_num} not found"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])