import os
import json
import tempfile
import shutil
from unittest import mock
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import double_dealdata

class TestDoubleDealData:
    """Tests for double_dealdata.py functions."""
    
    @pytest.fixture
    def sample_log_content(self):
        """Fixture to provide sample log content for testing."""
        return """Version 1.0
Timestamp 1748241244
ChairNO 0 1109720
Deal 0 [6772X68X2X6963377]
ChairNO 1 1110133
Deal 1 [Q9Q98J9QJ38J444J8]
ChairNO 2 1109875
Deal 2 [AKAA52AKBK2L5Q54]
Call 0 0
Call 2 1
Rob 0 0
Rob 1 0
Bottom 2 [X5S5D3]
Double 0 0
Double 1 0
Double 2 2
Throw 2
Throw 0
Throw 2
Throw 1
Throw 2
Throw 0
Throw 2
Throw 1
Throw 2
Version 1.0
"""
    
    @pytest.fixture
    def mock_log_file(self, sample_log_content, tmp_path):
        """Create a mock log file for testing."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        log_file = log_dir / "188_20250526.record"
        log_file.write_text(sample_log_content, encoding='gb18030')
        return log_file
    
    def test_get_call_rob_data_parsing(self, mock_log_file, tmp_path):
        """Test that get_call_rob_data correctly parses log data."""
        # Setup
        test_file = os.path.basename(mock_log_file)
        output_file = tmp_path / f"{test_file[:-7]}.json"
        
        # Run the function in a context where it writes to our temp directory
        with mock.patch('os.getcwd', return_value=str(tmp_path)):
            with mock.patch('sys.stdout', mock.MagicMock()):  # Suppress print statements
                double_dealdata.get_call_rob_data(test_file, 0, 
                                             logs_dir=str(tmp_path / "logs"), 
                                             output_dir=str(tmp_path))
        
        # Check that output file was created
        assert output_file.exists()
        
        # Read the data and validate structure
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) > 0
            
            # Parse the first entry
            data = json.loads(json.loads(lines[0]))
            
            # Check required fields
            assert 'chair_no' in data
            assert 'user_id' in data
            assert 'hand_tile' in data
            assert 'banker' in data
            assert 'bottom' in data
            assert 'his_call' in data
            assert 'his_rob' in data
            assert 'his_double' in data
            assert 'double_action' in data
            assert 'time' in data
            assert 'key' in data
            assert 'is_win' in data
            
            # Check specific values
            assert data['time'] == '1748241244'
            assert data['bottom'] == 'XSD]'
            assert isinstance(data['double_action'], int)
            assert isinstance(data['is_win'], int)
    
    def test_win_loss_calculation(self, mock_log_file, tmp_path):
        """Test that win/loss is correctly calculated based on banker and last throw."""
        # Setup similar to previous test
        test_file = os.path.basename(mock_log_file)
        output_file = tmp_path / f"{test_file[:-7]}.json"
        
        # Run function
        with mock.patch('os.getcwd', return_value=str(tmp_path)):
            with mock.patch('sys.stdout', mock.MagicMock()):
                double_dealdata.get_call_rob_data(test_file, 0, 
                                             logs_dir=str(tmp_path / "logs"), 
                                             output_dir=str(tmp_path))
        
        # Validate win/loss calculation
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            data_list = [json.loads(json.loads(line)) for line in lines]
            
            # Find the banker
            banker_chair = None
            for data in data_list:
                if data['chair_no'] == data['banker']:
                    banker_chair = data['chair_no']
                    # Banker should have won (last throw was banker in our sample)
                    assert data['is_win'] == 1
                else:
                    # Non-bankers should have lost
                    assert data['is_win'] == 0
            
            # Make sure we found a banker
            assert banker_chair is not None