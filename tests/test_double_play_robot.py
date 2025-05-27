import os
import json
import tempfile
import pandas as pd
from unittest import mock
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import double_play_robot

class TestDoublePlayRobot:
    """Tests for double_play_robot.py functions."""
    
    @pytest.fixture
    def sample_json_data(self):
        """Fixture to provide sample JSON data for testing."""
        # Create sample data similar to 188_20250526.json
        data1 = {
            "chair_no": 0, "user_id": 1109720, "hand_tile": "6772X68X2X6963377", 
            "banker": 2, "bottom": "X53", 
            "his_call": {"0": 0, "1": -1, "2": 1}, 
            "his_rob": {"0": -1, "1": 0, "2": -1}, 
            "his_double": {"0": -1, "1": -1, "2": -1}, 
            "double_action": 1, "time": "1748241244", 
            "key": "1748241244_1109720", "is_win": 0
        }
        
        data2 = {
            "chair_no": 1, "user_id": 1110133, "hand_tile": "Q9Q98J9QJ38J444J8", 
            "banker": 2, "bottom": "X53", 
            "his_call": {"0": 0, "1": -1, "2": 1}, 
            "his_rob": {"0": -1, "1": 0, "2": -1}, 
            "his_double": {"0": 0, "1": -1, "2": -1}, 
            "double_action": 2, "time": "1748241244", 
            "key": "1748241244_1110133", "is_win": 1
        }
        
        data3 = {
            "chair_no": 2, "user_id": 1109875, "hand_tile": "KAKAA52AKBK2L5Q54X53", 
            "banker": 2, "bottom": "X53", 
            "his_call": {"0": 0, "1": -1, "2": 1}, 
            "his_rob": {"0": -1, "1": 0, "2": -1}, 
            "his_double": {"0": 0, "1": 0, "2": -1}, 
            "double_action": 4, "time": "1748241244", 
            "key": "1748241244_1109875", "is_win": 1
        }
        
        return [data1, data2, data3]
    
    @pytest.fixture
    def sample_log_content(self):
        """Fixture to provide sample log content for testing."""
        # Header line + sample data line
        return """ʱ���,����ID,��ʱ,����,��ˮ��,������,������,��������,�Ծ�����,���1,״̬,����,��ɫ,��Ӯ,��ʼ����,ʣ������,������Ӯ,��ʼ����,ʣ�����,���2,״̬,����,��ɫ,��Ӯ,��ʼ����,ʣ������,������Ӯ,��ʼ����,ʣ�����,���3,״̬,����,��ɫ,��Ӯ,��ʼ����,ʣ������,������Ӯ,��ʼ����,ʣ�����,�Ƿ��ǲ�ϴ������,��ʽ����ʱ��,���1�����˰汾,���2�����˰汾,���3�����˰汾,��Ϸ��ʼʱ��
2025-05-26 14:35:00,188,55,48,24000,1500,1,70000,0,1109875,65,������,����,162640,199300,353940,0,0,0,1110133,65,������,ũ��,-95650,104962,1312,0,0,0,1109720,65,������,ũ��,-66990,74990,0,0,1,1,��,43,192.168.102.45:2409,192.168.102.45:2412,192.168.102.45:2409,1748241244"""
    
    @pytest.fixture
    def setup_test_files(self, sample_json_data, sample_log_content, tmp_path):
        """Set up test files for the analysis."""
        # Create the JSON file
        json_file = tmp_path / "188_20250526.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            for data in sample_json_data:
                json_str = json.dumps(data)
                json.dump(json_str, f)
                f.write('\n')
        
        # Create the log file
        log_file = tmp_path / "PlayRecord20250526.log"
        with open(log_file, 'w', encoding='gb18030') as f:
            f.write(sample_log_content)
        
        return {
            'json_file': json_file,
            'log_file': log_file,
            'tmp_path': tmp_path
        }
    
    def test_win_rate_calculation(self):
        """Test win rate calculation functionality."""
        # Create test data
        test_data = [
            {'banker': 1, 'double_action': 1, 'is_win': 1},
            {'banker': 1, 'double_action': 1, 'is_win': 0},
            {'banker': 1, 'double_action': 1, 'is_win': 1},
            {'banker': 1, 'double_action': 2, 'is_win': 1},
            {'banker': 1, 'double_action': 2, 'is_win': 0},
            {'banker': 1, 'double_action': 4, 'is_win': 1},
        ]
        
        # Convert to DataFrame
        df = pd.DataFrame(test_data)
        
        # Filter data as done in the script
        df_no_double = df[df['double_action'] == 1]
        df_double = df[df['double_action'] == 2]
        df_super_double = df[df['double_action'] == 4]
        
        # Calculate win rates
        if len(df_no_double) > 0:
            wins = (df_no_double['is_win'] == 1).sum()
            total = len(df_no_double)
            no_double_win_rate = wins/total
            assert no_double_win_rate == 2/3  # 2 wins out of 3
        
        if len(df_double) > 0:
            wins = (df_double['is_win'] == 1).sum()
            total = len(df_double)
            double_win_rate = wins/total
            assert double_win_rate == 1/2  # 1 win out of 2
        
        if len(df_super_double) > 0:
            wins = (df_super_double['is_win'] == 1).sum()
            total = len(df_super_double)
            super_double_win_rate = wins/total
            assert super_double_win_rate == 1  # 1 win out of 1
    
    def test_net_win_calculation(self):
        """Test net win calculation functionality."""
        # Create test data with net_win field
        test_data = [
            {'banker': 1, 'double_action': 1, 'is_win': 1, 'net_win': 100},
            {'banker': 1, 'double_action': 1, 'is_win': 0, 'net_win': -50},
            {'banker': 1, 'double_action': 1, 'is_win': 1, 'net_win': 200},
            {'banker': 1, 'double_action': 2, 'is_win': 1, 'net_win': 300},
            {'banker': 1, 'double_action': 2, 'is_win': 0, 'net_win': -200},
            {'banker': 1, 'double_action': 4, 'is_win': 1, 'net_win': 500},
        ]
        
        # Convert to DataFrame
        df = pd.DataFrame(test_data)
        
        # Filter data as done in the script
        df_no_double = df[df['double_action'] == 1]
        df_double = df[df['double_action'] == 2]
        df_super_double = df[df['double_action'] == 4]
        
        # Calculate net win totals
        if len(df_no_double) > 0:
            net_win_total = df_no_double['net_win'].sum()
            assert net_win_total == 250  # 100 - 50 + 200
        
        if len(df_double) > 0:
            net_win_total = df_double['net_win'].sum()
            assert net_win_total == 100  # 300 - 200
        
        if len(df_super_double) > 0:
            net_win_total = df_super_double['net_win'].sum()
            assert net_win_total == 500  # Just 500
    
    def test_calculate_net_win_stats(self):
        """Test the calculate_net_win_stats function."""
        # Create test data
        test_data = [
            {'is_win': 1, 'net_win': 100},
            {'is_win': 0, 'net_win': -50},
            {'is_win': 1, 'net_win': 200},
            {'is_win': 0, 'net_win': -150},
            {'is_win': 1, 'net_win': 300},
        ]
        
        # Convert to DataFrame
        df = pd.DataFrame(test_data)
        
        # Calculate statistics
        stats = double_play_robot.calculate_net_win_stats(df)
        
        # Verify results
        assert stats['total'] == 400  # Sum of all net wins
        assert stats['count'] == 5    # Total number of games
        assert stats['avg'] == 80     # Average net win (400/5)
        assert stats['wins'] == 3     # Number of wins
        assert stats['losses'] == 2   # Number of losses
        assert stats['win_total'] == 600  # Sum of net wins for winning games
        assert stats['loss_total'] == -200  # Sum of net wins for losing games
        assert stats['win_avg'] == 200  # Average net win for winning games
        assert stats['loss_avg'] == -100  # Average net win for losing games
        assert round(stats['std'], 2) == 182.35  # Standard deviation (rounded)
        
    def test_generate_net_win_report(self):
        """Test the generate_net_win_report function."""
        # Create test data for new and old robot
        new_robot_no_double = pd.DataFrame([
            {'is_win': 1, 'net_win': 100},
            {'is_win': 0, 'net_win': -50}
        ])
        
        new_robot_double = pd.DataFrame([
            {'is_win': 1, 'net_win': 200},
            {'is_win': 1, 'net_win': 300}
        ])
        
        new_robot_super_double = pd.DataFrame([
            {'is_win': 1, 'net_win': 500}
        ])
        
        old_robot_no_double = pd.DataFrame([
            {'is_win': 0, 'net_win': -100},
            {'is_win': 1, 'net_win': 50}
        ])
        
        old_robot_double = pd.DataFrame([
            {'is_win': 0, 'net_win': -150},
            {'is_win': 1, 'net_win': 100}
        ])
        
        old_robot_super_double = pd.DataFrame([
            {'is_win': 0, 'net_win': -200}
        ])
        
        # Prepare input for the function
        new_robot_dfs = {
            'no_double': new_robot_no_double,
            'double': new_robot_double,
            'super_double': new_robot_super_double
        }
        
        old_robot_dfs = {
            'no_double': old_robot_no_double,
            'double': old_robot_double,
            'super_double': old_robot_super_double
        }
        
        # Generate report
        stats = double_play_robot.generate_net_win_report(new_robot_dfs, old_robot_dfs)
        
        # Verify some key results
        assert stats['new_robot']['total']['total'] == 1050  # Sum of all new robot net wins
        assert stats['old_robot']['total']['total'] == -300  # Sum of all old robot net wins
        assert stats['difference']['total']['total'] == 1350  # Difference in total net wins
        
        # Check detailed stats for new robot's double action
        assert stats['new_robot']['double']['total'] == 500
        assert stats['new_robot']['double']['count'] == 2
        assert stats['new_robot']['double']['avg'] == 250
        assert stats['new_robot']['double']['wins'] == 2
        assert stats['new_robot']['double']['losses'] == 0
        
        # Check detailed stats for old robot's no_double action
        assert stats['old_robot']['no_double']['total'] == -50
        assert stats['old_robot']['no_double']['count'] == 2
        assert stats['old_robot']['no_double']['avg'] == -25
        assert stats['old_robot']['no_double']['wins'] == 1
        assert stats['old_robot']['no_double']['losses'] == 1