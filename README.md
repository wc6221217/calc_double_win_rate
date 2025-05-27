# 斗地主双倍胜率计算工具 (calc_double_win_rate)

一个用于分析斗地主游戏日志数据并统计机器人胜率和净赢银数据的工具。

## 项目概述

本项目是一个斗地主游戏日志分析和双倍胜率统计工具，主要用于分析机器人在斗地主游戏中的表现。工具可以处理游戏日志文件，解析游戏数据，并生成详细的统计报告，包括：

- 机器人在不同加倍情况下的胜率
- 机器人的净赢银统计
- 新旧版本机器人性能对比
- 多维度统计分析（胜负局、平均净赢银等）

## 项目结构说明

- `double_dealdata.py`: 处理游戏日志文件，解析游戏数据并生成JSON格式的数据
  - 使用多进程处理大量日志文件
  - 解析游戏中的叫牌、抢地主、加倍等行为
  - 计算胜负结果
  - 生成结构化的JSON数据

- `double_play_robot.py`: 分析机器人胜率和净赢银统计
  - 计算不同加倍情况下的胜率
  - 计算净赢银统计数据
  - 对比新旧版本机器人性能
  - 生成统计报告和CSV导出

- `tests/`: 单元测试目录，包含对主要脚本的测试用例
  - `test_double_dealdata.py`: 测试日志解析和胜负计算功能
  - `test_double_play_robot.py`: 测试胜率和净赢银计算功能

## 安装和使用指南

### 环境要求

- Python 3.6+
- pandas 库

### 依赖包安装

```bash
pip install pandas
```

### 使用方法

1. **准备日志文件**：
   - 将斗地主游戏日志文件（`.log`格式）放置在 `logs` 目录下

2. **处理日志文件**：
   ```bash
   python double_dealdata.py
   ```
   该命令会处理 `logs` 目录下的日志文件，并在当前目录生成对应的JSON文件。

3. **分析胜率和净赢银**：
   ```bash
   python double_play_robot.py
   ```
   该命令会读取生成的JSON文件和 `PlayRecord*.log` 文件，计算并输出胜率和净赢银统计结果。

### 示例用法

```python
# 处理特定目录下的日志文件并将结果输出到指定目录
import os
from double_dealdata import get_call_rob_data

logs_dir = './my_logs'
output_dir = './results'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 处理单个日志文件
get_call_rob_data('188_20250526.log', 0, logs_dir, output_dir)

# 或者使用多进程处理多个日志文件
import multiprocessing as mp
log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]

pool = mp.Pool(4)  # 使用4个进程
for i, log_file in enumerate(log_files):
    pool.apply_async(get_call_rob_data, args=(log_file, i, logs_dir, output_dir))

pool.close()
pool.join()
```

## 数据格式说明

### 输入日志文件格式

输入的日志文件（`.log`）包含斗地主游戏过程中的详细记录，包括：
- 时间戳
- 座位号和用户ID
- 发牌信息
- 叫牌、抢地主行为
- 加倍行为（不加倍、加倍、超级加倍）
- 出牌记录

### 输出JSON数据结构

处理后的JSON数据包含以下字段：
- `chair_no`: 座位号
- `user_id`: 用户ID
- `hand_tile`: 手牌信息
- `banker`: 庄家（地主）座位号
- `bottom`: 底牌信息
- `his_call`: 各玩家的叫牌行为
- `his_rob`: 各玩家的抢地主行为
- `his_double`: 各玩家的加倍行为
- `double_action`: 加倍动作（1: 不加倍, 2: 加倍, 4: 超级加倍）
- `time`: 时间戳
- `key`: 唯一标识符
- `is_win`: 胜负结果（1: 胜, 0: 负）

### 统计报告格式

生成的统计报告包含以下信息：
- 不同加倍情况下的胜率统计
- 净赢银总计和平均值
- 胜负局数统计
- 胜负局净赢银统计
- 新旧版本机器人对比数据

统计结果可以导出为CSV格式，包含详细的统计数据。

## 测试说明

### 运行测试

在项目根目录运行以下命令：

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_double_dealdata.py
pytest tests/test_double_play_robot.py

# 运行特定测试函数
pytest tests/test_double_dealdata.py::TestDoubleDealData::test_get_call_rob_data_parsing
```

### 测试覆盖范围

测试覆盖了以下关键功能：
- 日志文件解析功能
- 胜负结果计算
- 胜率计算功能
- 净赢银统计功能

## 功能特性

- **多进程处理**：使用Python的multiprocessing模块高效处理大量日志文件
- **自动识别庄家和农民**：根据游戏日志自动识别角色
- **胜负结果计算**：基于最后出牌和庄家信息自动计算胜负
- **机器人AI识别**：区分新旧版本机器人并进行对比分析
- **净赢银统计**：详细计算不同情况下的净赢银数据
- **导出CSV报告**：支持将统计结果导出为CSV格式，方便进一步分析
- **多维度分析**：支持按加倍类型、胜负情况等多维度进行数据分析