# 单元测试说明

本目录包含对 `double_dealdata.py` 和 `double_play_robot.py` 两个统计脚本的单元测试。

## 测试内容

### test_double_dealdata.py

测试 `double_dealdata.py` 的功能，主要包括：

1. `test_get_call_rob_data_parsing` - 测试日志文件解析功能是否正确，检查生成的JSON数据结构与内容是否符合预期
2. `test_win_loss_calculation` - 测试胜负结果计算是否正确，基于庄家（banker）和最后出牌（throw）数据

### test_double_play_robot.py

测试 `double_play_robot.py` 的功能，主要包括：

1. `test_win_rate_calculation` - 测试胜率计算功能是否正确
2. `test_net_win_calculation` - 测试净赢银统计功能是否正确

## 运行测试

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

## 测试数据

测试使用了模拟的日志文件和JSON数据，以测试代码在各种情况下的行为。测试数据尽量模拟真实数据结构，但为简化测试而减少了数据量。