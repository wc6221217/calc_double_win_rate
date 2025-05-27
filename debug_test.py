import os
import json
import tempfile
import shutil
from unittest import mock
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import double_dealdata

# Print the slicing result directly to debug
bottom_line = "Bottom 2 [X5S5D3]"
line_parts = bottom_line.split(' ')
print(f"Line parts: {line_parts}")
bottom_data = line_parts[2]
print(f"Bottom data: {bottom_data}")
print(f"Bottom data[1::2]: {bottom_data[1::2]}")

# Create a fixture for the sample log content
sample_log_content = """Version 1.0
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

# Create a temporary directory for the log file
tmp_dir = tempfile.mkdtemp()
log_dir = os.path.join(tmp_dir, "logs")
os.makedirs(log_dir)
log_file = os.path.join(log_dir, "188_20250526.record")

# Write the log content to the file
with open(log_file, 'w', encoding='gb18030') as f:
    f.write(sample_log_content)

# Process the log file
with mock.patch('sys.stdout', mock.MagicMock()):  # Suppress print statements
    double_dealdata.get_call_rob_data(os.path.basename(log_file), 0, 
                                 logs_dir=log_dir, 
                                 output_dir=tmp_dir)

# Check the output file
output_file = os.path.join(tmp_dir, "188_20250526.json")
print("\nOutput file content:")
with open(output_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        data = json.loads(json.loads(line))
        print(f"bottom: {data['bottom']}")
        
# Clean up
shutil.rmtree(tmp_dir)