# 斗地主双倍胜率计算器 (Double Win Rate Calculator)

一个用于分析斗地主游戏中机器人AI性能的统计工具，专门对比新旧版本机器人在不同加倍策略下的胜率和净赢银表现。

## 项目描述

本项目提供了完整的斗地主游戏数据分析解决方案，包括：
- 游戏日志解析和数据提取
- 机器人AI性能统计分析
- 新旧版本机器人对比
- 不同加倍策略效果评估
- 详细统计报告生成

## 功能特性

### 🎯 核心功能
- **游戏数据解析**: 解析斗地主游戏日志文件，提取关键游戏数据
- **胜率统计**: 计算不同加倍策略(不加倍/加倍/超级加倍)下的胜率
- **版本对比**: 对比新旧版本机器人的性能差异
- **净赢银分析**: 统计和分析净赢银数据，包括平均值、标准差等指标
- **数据导出**: 支持将统计结果导出为CSV格式

### 📊 支持的加倍策略
- **不加倍 (1倍)**: 基础游戏模式
- **加倍 (2倍)**: 双倍积分模式  
- **超级加倍 (4倍)**: 四倍积分模式

### 📈 统计指标
- 胜率百分比
- 净赢银总计和平均值
- 胜负局数统计
- 统计显著性分析

## 安装指南

### 系统要求
- Python 3.7 或更高版本
- 支持的操作系统: Windows, macOS, Linux

### 依赖安装

1. **克隆项目**
```bash
git clone https://github.com/wc6221217/calc_double_win_rate.git
cd calc_double_win_rate
```

2. **安装Python依赖**
```bash
pip install pandas
```

3. **验证安装**
```bash
python -m pytest tests/ -v
```

## 使用方法

### 数据准备

确保以下文件位于项目根目录：
- `PlayRecord20250526.log` - 游戏记录日志文件
- `188_20250526.json` - 游戏数据JSON文件
- `logs/` 目录 - 包含游戏记录文件

### 基本使用

#### 1. 游戏数据解析
```bash
python double_dealdata.py
```
此脚本会：
- 解析 `logs/` 目录中的游戏记录文件
- 提取游戏数据并生成JSON格式输出
- 计算胜负结果

#### 2. 机器人性能分析
```bash
python double_play_robot.py
```
此脚本会：
- 分析机器人胜率和净赢银表现
- 生成详细的统计报告
- 导出CSV格式的统计数据

### 示例输出

运行分析后，你会看到类似以下的统计结果：

```
=== 增强版净赢银统计报告 ===

机器人版本对比汇总：
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ 版本     │ 不加倍   │ 加倍     │ 超级加倍 │ 总计     │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│ 新版机器人│  81775   │  -44006  │ 24688819 │ 24726588 │
│ 旧版机器人│ 2254477  │ 1377379  │ 19885088 │ 23516944 │
│ 差值     │ -2172702 │ -1421385 │ 4803731  │ 1209644  │
└──────────┴──────────┴──────────┴──────────┴──────────┘

新版机器人超级加倍的胜率：75.12% (305/406)
旧版机器人超级加倍的胜率：85.97% (190/221)
```

### 输出文件

- `net_win_statistics.csv` - 详细统计数据的CSV导出文件
- `{日期}.json` - 解析后的游戏数据JSON文件

## 项目结构

```
calc_double_win_rate/
├── README.md                 # 项目文档
├── double_dealdata.py        # 游戏数据解析脚本
├── double_play_robot.py      # 机器人性能分析脚本
├── PlayRecord20250526.log    # 游戏记录日志文件
├── 188_20250526.json         # 游戏数据JSON文件
├── net_win_statistics.csv    # 统计结果输出
├── logs/                     # 游戏记录目录
│   └── 188_20250526.record
└── tests/                    # 单元测试
    ├── __init__.py
    ├── README.md
    ├── test_double_dealdata.py
    └── test_double_play_robot.py
```

## 测试

项目包含完整的单元测试套件：

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_double_dealdata.py
pytest tests/test_double_play_robot.py

# 运行特定测试函数
pytest tests/test_double_dealdata.py::TestDoubleDealData::test_get_call_rob_data_parsing
```

测试覆盖的功能：
- 日志文件解析功能
- 胜负结果计算
- 胜率统计计算
- 净赢银统计功能

## 贡献指南

我们欢迎社区贡献！请按照以下步骤参与项目：

### 开发环境设置

1. Fork 本项目
2. 创建功能分支: `git checkout -b feature/your-feature-name`
3. 安装开发依赖: `pip install pytest pandas`
4. 进行开发并添加测试

### 提交指南

1. **代码规范**: 请确保代码遵循PEP 8规范
2. **测试要求**: 新功能必须包含相应的单元测试
3. **提交信息**: 使用清晰、描述性的提交信息

```bash
# 示例提交流程
git add .
git commit -m "feat: 添加新的统计指标计算功能"
git push origin feature/your-feature-name
```

4. **Pull Request**: 创建PR并详细描述变更内容

### 报告问题

如果你发现问题或有功能建议，请：
1. 检查是否已有相关的Issue
2. 创建新Issue并提供详细信息：
   - 问题描述
   - 重现步骤
   - 期望行为
   - 系统环境信息

## 许可证信息

本项目采用 MIT 许可证。详细信息请查看 [LICENSE](LICENSE) 文件。

### MIT License

```
MIT License

Copyright (c) 2025 calc_double_win_rate

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 版本历史

- **v1.0.0** - 初始版本
  - 基础的游戏数据解析功能
  - 机器人性能统计分析
  - CSV数据导出功能

## 联系信息

- 项目维护者: [@wc6221217](https://github.com/wc6221217)
- 项目地址: [https://github.com/wc6221217/calc_double_win_rate](https://github.com/wc6221217/calc_double_win_rate)

---

**注意**: 本项目仅用于学术研究和技术分析，请遵循相关法律法规和平台使用条款。