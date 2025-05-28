# 统计斗地主不洗牌 加倍功能  人机对局机器人和真人之间的对比
# In[1]
import pandas as pd
# jqr_uid = pd.read_csv(r'E:\code\Server_Train\DDZ\ddz_analysis\robot_num\data\22042robotuid.csv')['uid'].to_list()
# In[1]
import json, os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# files_ls = os.listdir(r".\\calc_double_win_rate\\double_data")
data_ls = []
roomid = '188'

double_data_old_roobt_ls = []
double_data_robot_ls = []

robot_version_data = {}
new_jqr_uid = []
old_jqr_uid = []
# 存储净赢银数据的字典
net_win_data = {}

# Define file paths
log_file_path = r'.\\PlayRecord20250526.log'
# Check if the file exists, if not, try the current directory
if not os.path.exists(log_file_path):
    alt_log_file_path = 'PlayRecord20250526.log'
    if os.path.exists(alt_log_file_path):
        log_file_path = alt_log_file_path
    else:
        print(f"Error: The required log file 'PlayRecord20250526.log' was not found.")
        print("Please make sure the file exists either in the 'calc_double_win_rate' directory or in the current directory.")
        exit(1)

with open(log_file_path, "r", encoding='gb18030', errors='ignore') as res_file:
    next(res_file)
    for line in res_file:
        if len(line.strip()) == 0:
            continue
            
        fields = line.strip().split(',')

        role1 = fields[12]
        role2 = fields[22]
        role3 = fields[32]
        uid1 = fields[9]
        uid2 = fields[19]
        uid3 = fields[29]
        ai1 = fields[41]
        ai2 = fields[42]
        ai3 = fields[43]
        timestamp = fields[44]


        deposit1 = int(fields[13])
        deposit2 = int(fields[23])
        deposit3 = int(fields[33])

        
        #过滤掉有玩家参与的局
        if len(ai1)==0 or len(ai2)==0 or len(ai3)==0:
            continue
        #过滤掉全部是相同机器人版本的局
        if ai1 == ai2 and ai2 == ai3:
            continue
        #过滤掉没有胜负关系的局
        if int(deposit1)==0:
            continue

        # print(deposit1, deposit2, deposit3)
        if ai1 == '192.168.102.45:2412':
            new_jqr_uid.append(timestamp+'_'+uid1)
            # 存储净赢银数据
            net_win_data[timestamp+'_'+uid1] = deposit1
        if ai2 == '192.168.102.45:2412':
            new_jqr_uid.append(timestamp+'_'+uid2)
            # 存储净赢银数据
            net_win_data[timestamp+'_'+uid2] = deposit2
        if ai3 == '192.168.102.45:2412':
            new_jqr_uid.append(timestamp+'_'+uid3)
            # 存储净赢银数据
            net_win_data[timestamp+'_'+uid3] = deposit3
        if ai1 == '192.168.102.45:2409':
            old_jqr_uid.append(timestamp+'_'+uid1)
            # 存储净赢银数据
            net_win_data[timestamp+'_'+uid1] = deposit1
        if ai2 == '192.168.102.45:2409':
            old_jqr_uid.append(timestamp+'_'+uid2)
            # 存储净赢银数据
            net_win_data[timestamp+'_'+uid2] = deposit2
        if ai3 == '192.168.102.45:2409':
            old_jqr_uid.append(timestamp+'_'+uid3)
            # 存储净赢银数据
            net_win_data[timestamp+'_'+uid3] = deposit3

# Define file paths
json_file_path = r'.\\188_20250526.json'
# Check if the file exists, if not, try the current directory
if not os.path.exists(json_file_path):
    alt_json_file_path = '188_20250526.json'
    if os.path.exists(alt_json_file_path):
        json_file_path = alt_json_file_path
    else:
        print(f"Error: The required JSON file '188_20250526.json' was not found.")
        print("Please make sure the file exists either in the 'calc_double_win_rate' directory or in the current directory.")
        exit(1)

with open(json_file_path, "r", encoding='gb18030', errors='ignore') as f:
    f = f.readlines()
    duiju_ls = []
    for i, line in enumerate(f):
        data = json.loads(json.loads(line))

        if len(data.get('hand_tile')) == 20:
            data['banker'] = 1
        else:
            data['banker'] = 0
        time_uid_key = str(data.get('time'))+'_'+str(data.get('user_id'))
        # 添加净赢银数据
        if time_uid_key in net_win_data:
            data['net_win'] = net_win_data[time_uid_key]
        else:
            data['net_win'] = 0
            
        if time_uid_key in new_jqr_uid:
            double_data_robot_ls.append(data)
        else:
            double_data_old_roobt_ls.append(data)


double_old_robot_df = pd.DataFrame(double_data_old_roobt_ls)
double_robot_df = pd.DataFrame(double_data_robot_ls)
# In[1]
double_old_robot_df_dz = double_old_robot_df[double_old_robot_df['banker']==1]
double_old_robot_df_nm = double_old_robot_df[double_old_robot_df['banker']==0]

double_robot_df_dz = double_robot_df[double_robot_df['banker']==1]
double_robot_df_nm = double_robot_df[double_robot_df['banker']==0]
# In[1]
double_old_robot_df_dz_lose = double_old_robot_df_dz[double_old_robot_df_dz['is_win'] == 0]
double_old_robot_df_dz_win = double_old_robot_df_dz[double_old_robot_df_dz['is_win'] == 1]

double_old_robot_df_nm_lose = double_old_robot_df_nm[double_old_robot_df_nm['is_win'] == 0]
double_old_robot_df_nm_win = double_old_robot_df_nm[double_old_robot_df_nm['is_win'] == 1]
# In[1]
double_robot_df_dz_lose = double_robot_df_dz[double_robot_df_dz['is_win'] == 0]
double_robot_df_dz_win = double_robot_df_dz[double_robot_df_dz['is_win'] == 1]

double_robot_df_nm_lose = double_robot_df_nm[double_robot_df_nm['is_win'] == 0]
double_robot_df_nm_win = double_robot_df_nm[double_robot_df_nm['is_win'] == 1]

double_robot_df_dz_no_double = double_robot_df_dz[double_robot_df_dz['double_action'] == 1]
double_robot_df_dz_double = double_robot_df_dz[double_robot_df_dz['double_action'] == 2]
double_robot_df_dz_super_double = double_robot_df_dz[double_robot_df_dz['double_action'] == 4]

double_old_robot_df_dz_no_double = double_old_robot_df_dz[double_old_robot_df_dz['double_action'] == 1]

double_old_robot_df_dz_double = double_old_robot_df_dz[double_old_robot_df_dz['double_action'] == 2]
double_old_robot_df_dz_super_double = double_old_robot_df_dz[double_old_robot_df_dz['double_action'] == 4]
#统计新版机器人和旧版机器人在不加倍、加倍和超级加倍情况下的胜率

#统计新版机器人不加倍、加倍和超级加倍情况下的胜率
if len(double_robot_df_dz_no_double) > 0:
    wins = (double_robot_df_dz_no_double['is_win'] == 1).sum()
    total = len(double_robot_df_dz_no_double)
    print("新版机器人不加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("新版机器人不加倍的胜率：无数据")

if len(double_robot_df_dz_double) > 0:
    wins = (double_robot_df_dz_double['is_win'] == 1).sum()
    total = len(double_robot_df_dz_double)
    print("新版机器人加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("新版机器人加倍的胜率：无数据")

if len(double_robot_df_dz_super_double) > 0:
    wins = (double_robot_df_dz_super_double['is_win'] == 1).sum()
    total = len(double_robot_df_dz_super_double)
    print("新版机器人超级加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("新版机器人超级加倍的胜率：无数据")

#统计旧版机器人不加倍、加倍和超级加倍情况下的胜率
if len(double_old_robot_df_dz_no_double) > 0:
    wins = (double_old_robot_df_dz_no_double['is_win'] == 1).sum()
    total = len(double_old_robot_df_dz_no_double)
    print("旧版机器人不加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("旧版机器人不加倍的胜率：无数据")

if len(double_old_robot_df_dz_double) > 0:
    wins = (double_old_robot_df_dz_double['is_win'] == 1).sum()
    total = len(double_old_robot_df_dz_double)
    print("旧版机器人加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("旧版机器人加倍的胜率：无数据")

if len(double_old_robot_df_dz_super_double) > 0:
    wins = (double_old_robot_df_dz_super_double['is_win'] == 1).sum()
    total = len(double_old_robot_df_dz_super_double)
    print("旧版机器人超级加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))


#统计新版和旧版机器人在不同加倍动作下的净赢银
#其中机器人的加倍动作在188_20250526.json中double_action标签中
#其中净赢银数据在PlayRecord20250526.log中每一行用逗号分割后的第14、24、34行

def calculate_net_win_stats(dataframe, is_win_column='is_win', net_win_column='net_win'):
    """
    计算详细的净赢银统计数据
    
    Args:
        dataframe (pandas.DataFrame): 包含游戏数据的DataFrame
        is_win_column (str): 表示胜负的列名
        net_win_column (str): 表示净赢银的列名
        
    Returns:
        dict: 包含以下统计数据的字典:
            - total: 净赢银总计
            - count: 局数
            - avg: 平均净赢银
            - wins: 胜局数
            - losses: 负局数
            - win_total: 胜局净赢银总计
            - loss_total: 负局净赢银总计
            - win_avg: 胜局平均净赢银
            - loss_avg: 负局平均净赢银
            - std: 标准差
            - cv: 变异系数
    """
    stats = {}
    
    if len(dataframe) == 0:
        stats = {
            'total': 0, 'count': 0, 'avg': 0, 
            'wins': 0, 'losses': 0, 
            'win_total': 0, 'loss_total': 0, 
            'win_avg': 0, 'loss_avg': 0,
            'std': 0, 'cv': 0
        }
        return stats
    
    # 基础统计
    win_df = dataframe[dataframe[is_win_column] == 1]
    loss_df = dataframe[dataframe[is_win_column] == 0]
    
    total = dataframe[net_win_column].sum()
    count = len(dataframe)
    avg = total / count if count > 0 else 0
    
    wins = len(win_df)
    losses = len(loss_df)
    
    win_total = win_df[net_win_column].sum() if wins > 0 else 0
    loss_total = loss_df[net_win_column].sum() if losses > 0 else 0
    
    win_avg = win_total / wins if wins > 0 else 0
    loss_avg = loss_total / losses if losses > 0 else 0
    
    # 高级统计
    std = dataframe[net_win_column].std() if count > 0 else 0
    cv = (std / abs(avg)) if avg != 0 else 0
    
    stats = {
        'total': total, 'count': count, 'avg': avg, 
        'wins': wins, 'losses': losses, 
        'win_total': win_total, 'loss_total': loss_total, 
        'win_avg': win_avg, 'loss_avg': loss_avg,
        'std': std, 'cv': cv
    }
    
    return stats

def generate_net_win_report(new_robot_dfs, old_robot_dfs, output_csv=None):
    """
    生成净赢银详细统计报告
    
    Args:
        new_robot_dfs (dict): 新版机器人数据，包含 'no_double', 'double', 'super_double' 三个DataFrame
        old_robot_dfs (dict): 旧版机器人数据，包含 'no_double', 'double', 'super_double' 三个DataFrame
        output_csv (str, optional): 如果提供，则将统计结果导出到CSV文件
        
    Returns:
        dict: 统计结果的字典
    """
    # 创建统计数据结构
    net_win_stats = {
        'new_robot': {
            'no_double': calculate_net_win_stats(new_robot_dfs['no_double']),
            'double': calculate_net_win_stats(new_robot_dfs['double']),
            'super_double': calculate_net_win_stats(new_robot_dfs['super_double'])
        },
        'old_robot': {
            'no_double': calculate_net_win_stats(old_robot_dfs['no_double']),
            'double': calculate_net_win_stats(old_robot_dfs['double']),
            'super_double': calculate_net_win_stats(old_robot_dfs['super_double'])
        }
    }
    
    # 计算总计
    for robot_type in ['new_robot', 'old_robot']:
        total_count = sum(net_win_stats[robot_type][action]['count'] for action in ['no_double', 'double', 'super_double'])
        total_net_win = sum(net_win_stats[robot_type][action]['total'] for action in ['no_double', 'double', 'super_double'])
        total_wins = sum(net_win_stats[robot_type][action]['wins'] for action in ['no_double', 'double', 'super_double'])
        total_losses = sum(net_win_stats[robot_type][action]['losses'] for action in ['no_double', 'double', 'super_double'])
        total_win_net = sum(net_win_stats[robot_type][action]['win_total'] for action in ['no_double', 'double', 'super_double'])
        total_loss_net = sum(net_win_stats[robot_type][action]['loss_total'] for action in ['no_double', 'double', 'super_double'])
        
        net_win_stats[robot_type]['total'] = {
            'total': total_net_win,
            'count': total_count,
            'avg': total_net_win / total_count if total_count > 0 else 0,
            'wins': total_wins,
            'losses': total_losses,
            'win_total': total_win_net,
            'loss_total': total_loss_net,
            'win_avg': total_win_net / total_wins if total_wins > 0 else 0,
            'loss_avg': total_loss_net / total_losses if total_losses > 0 else 0,
            'std': 0,  # 这里不计算合并后的标准差
            'cv': 0    # 这里不计算合并后的变异系数
        }
    
    # 计算版本差异
    net_win_stats['difference'] = {}
    for action in ['no_double', 'double', 'super_double', 'total']:
        new_stats = net_win_stats['new_robot'][action]
        old_stats = net_win_stats['old_robot'][action]
        
        net_win_stats['difference'][action] = {
            'total': new_stats['total'] - old_stats['total'],
            'avg': new_stats['avg'] - old_stats['avg'],
            'win_rate': (new_stats['wins'] / new_stats['count'] if new_stats['count'] > 0 else 0) - 
                       (old_stats['wins'] / old_stats['count'] if old_stats['count'] > 0 else 0),
            'win_avg': new_stats['win_avg'] - old_stats['win_avg'],
            'loss_avg': new_stats['loss_avg'] - old_stats['loss_avg']
        }
    
    # 如果需要，导出CSV
    if output_csv:
        export_stats_to_csv(net_win_stats, output_csv)
    
    return net_win_stats

def analyze_and_visualize(new_robot_dfs, old_robot_dfs, output_dir=None):
    """
    进行全面分析并生成可视化结果
    
    Args:
        new_robot_dfs (dict): 新版机器人数据，包含 'no_double', 'double', 'super_double' 三个DataFrame
        old_robot_dfs (dict): 旧版机器人数据，包含 'no_double', 'double', 'super_double' 三个DataFrame
        output_dir (str, optional): 输出目录，如果提供则将所有结果保存到该目录
        
    Returns:
        dict: 包含统计结果和图表的字典
    """
    # 如果提供了输出目录，确保它存在
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 计算统计数据
    stats = generate_net_win_report(new_robot_dfs, old_robot_dfs)
    
    # 准备结果容器
    result = {
        'statistics': stats,
        'visualizations': {}
    }
    
    # 创建并保存可视化图表
    if output_dir:
        # 净赢银对比图
        net_win_fig = visualize_net_win_comparison(
            stats, 
            os.path.join(output_dir, 'net_win_comparison.png')
        )
        result['visualizations']['net_win'] = net_win_fig
        
        # 胜率对比图
        win_rate_fig = visualize_win_rate_comparison(
            stats, 
            os.path.join(output_dir, 'win_rate_comparison.png')
        )
        result['visualizations']['win_rate'] = win_rate_fig
        
        # 导出CSV和JSON
        export_stats_to_csv(stats, os.path.join(output_dir, 'net_win_statistics.csv'))
        export_stats_to_json(stats, os.path.join(output_dir, 'net_win_statistics.json'))
    else:
        # 不保存文件，只生成图表对象
        result['visualizations']['net_win'] = visualize_net_win_comparison(stats)
        result['visualizations']['win_rate'] = visualize_win_rate_comparison(stats)
    
    # 打印详细报告
    print_enhanced_net_win_report(stats)
    
    return result

def export_stats_to_csv(stats, output_file):
    """
    将统计数据导出到CSV文件
    
    Args:
        stats (dict): 统计数据
        output_file (str): 输出文件路径
    """
    import pandas as pd
    import os
    
    # 创建数据框
    rows = []
    
    # 添加新旧机器人数据
    for robot_type in ['new_robot', 'old_robot']:
        for action in ['no_double', 'double', 'super_double', 'total']:
            if action in stats[robot_type]:
                s = stats[robot_type][action]
                win_rate = s['wins'] / s['count'] if s['count'] > 0 else 0
                rows.append({
                    '机器人版本': '新版' if robot_type == 'new_robot' else '旧版',
                    '加倍动作': '不加倍' if action == 'no_double' else 
                              '加倍' if action == 'double' else 
                              '超级加倍' if action == 'super_double' else '总计',
                    '局数': s['count'],
                    '净赢银总计': s['total'],
                    '平均净赢银': s['avg'],
                    '胜率': win_rate,
                    '胜局数': s['wins'],
                    '负局数': s['losses'],
                    '胜局净赢银': s['win_total'],
                    '负局净赢银': s['loss_total'],
                    '胜局平均净赢银': s['win_avg'],
                    '负局平均净赢银': s['loss_avg'],
                    '标准差': s['std'],
                    '变异系数': s['cv']
                })
    
    # 添加差异数据
    for action in ['no_double', 'double', 'super_double', 'total']:
        if action in stats['difference']:
            d = stats['difference'][action]
            rows.append({
                '机器人版本': '差值(新版-旧版)',
                '加倍动作': '不加倍' if action == 'no_double' else 
                          '加倍' if action == 'double' else 
                          '超级加倍' if action == 'super_double' else '总计',
                '局数': '',
                '净赢银总计': d['total'],
                '平均净赢银': d['avg'],
                '胜率': d['win_rate'],
                '胜局数': '',
                '负局数': '',
                '胜局净赢银': '',
                '负局净赢银': '',
                '胜局平均净赢银': d['win_avg'],
                '负局平均净赢银': d['loss_avg'],
                '标准差': '',
                '变异系数': ''
            })
    
    # 创建DataFrame并导出
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"统计数据已导出到CSV文件: {os.path.abspath(output_file)}")

def export_stats_to_json(stats, output_file):
    """
    将统计数据导出到JSON文件
    
    Args:
        stats (dict): 统计数据
        output_file (str): 输出文件路径
    """
    import json
    import os
    import numpy as np
    
    # 创建一个自定义的JSON编码器，处理numpy类型
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return super(NumpyEncoder, self).default(obj)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
    
    print(f"统计数据已导出到JSON文件: {os.path.abspath(output_file)}")

def format_number(number, comma=True, precision=2):
    """格式化数字，用于显示"""
    if isinstance(number, (int, float)):
        if comma:
            if isinstance(number, int):
                return f"{number:,}"
            else:
                return f"{number:,.{precision}f}"
        else:
            if isinstance(number, int):
                return str(number)
            else:
                return f"{number:.{precision}f}"
    return str(number)

def visualize_net_win_comparison(stats, output_file=None):
    """
    创建净赢银对比的可视化图表
    
    Args:
        stats (dict): 由generate_net_win_report生成的统计数据
        output_file (str, optional): 输出文件路径，如果提供则保存图表
    
    Returns:
        matplotlib.figure.Figure: 生成的图表
    """
    # 设置图表样式
    sns.set(style="whitegrid")
    
    # 创建图表和子图
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 准备数据
    categories = ['不加倍', '加倍', '超级加倍', '总计']
    actions = ['no_double', 'double', 'super_double', 'total']
    
    new_robot_avg = [stats['new_robot'][action]['avg'] for action in actions]
    old_robot_avg = [stats['old_robot'][action]['avg'] for action in actions]
    
    # 设置条形图位置
    x = range(len(categories))
    width = 0.35
    
    # 绘制条形图
    rects1 = ax.bar([i - width/2 for i in x], new_robot_avg, width, label='新版机器人')
    rects2 = ax.bar([i + width/2 for i in x], old_robot_avg, width, label='旧版机器人')
    
    # 添加数据标签
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            label_height = height if height >= 0 else height - 20
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, label_height),
                        xytext=(0, 3 if height >= 0 else -15),
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    add_labels(rects1)
    add_labels(rects2)
    
    # 添加图表元素
    ax.set_title('不同加倍动作下的平均净赢银对比', fontsize=16)
    ax.set_xlabel('加倍动作类型', fontsize=12)
    ax.set_ylabel('平均净赢银', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"净赢银对比图表已保存到: {os.path.abspath(output_file)}")
    
    return fig

def visualize_win_rate_comparison(stats, output_file=None):
    """
    创建胜率对比的可视化图表
    
    Args:
        stats (dict): 由generate_net_win_report生成的统计数据
        output_file (str, optional): 输出文件路径，如果提供则保存图表
    
    Returns:
        matplotlib.figure.Figure: 生成的图表
    """
    # 设置图表样式
    sns.set(style="whitegrid")
    
    # 创建图表和子图
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 准备数据
    categories = ['不加倍', '加倍', '超级加倍', '总计']
    actions = ['no_double', 'double', 'super_double', 'total']
    
    new_robot_win_rates = [
        stats['new_robot'][action]['wins'] / stats['new_robot'][action]['count'] 
        if stats['new_robot'][action]['count'] > 0 else 0 
        for action in actions
    ]
    old_robot_win_rates = [
        stats['old_robot'][action]['wins'] / stats['old_robot'][action]['count'] 
        if stats['old_robot'][action]['count'] > 0 else 0 
        for action in actions
    ]
    
    # 转换为百分比
    new_robot_win_rates = [rate * 100 for rate in new_robot_win_rates]
    old_robot_win_rates = [rate * 100 for rate in old_robot_win_rates]
    
    # 设置条形图位置
    x = range(len(categories))
    width = 0.35
    
    # 绘制条形图
    rects1 = ax.bar([i - width/2 for i in x], new_robot_win_rates, width, label='新版机器人')
    rects2 = ax.bar([i + width/2 for i in x], old_robot_win_rates, width, label='旧版机器人')
    
    # 添加数据标签
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    add_labels(rects1)
    add_labels(rects2)
    
    # 添加图表元素
    ax.set_title('不同加倍动作下的胜率对比', fontsize=16)
    ax.set_xlabel('加倍动作类型', fontsize=12)
    ax.set_ylabel('胜率 (%)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"胜率对比图表已保存到: {os.path.abspath(output_file)}")
    
    return fig

def print_enhanced_net_win_report(stats):
    """
    打印增强版净赢银统计报告
    
    Args:
        stats (dict): 由generate_net_win_report生成的统计数据
    """
    print("\n=== 增强版净赢银统计报告 ===")
    
    # 打印对比汇总表格
    print("\n机器人版本对比汇总：")
    print("┌──────────┬──────────┬──────────┬──────────┬──────────┐")
    print("│ 版本     │ 不加倍   │ 加倍     │ 超级加倍 │ 总计     │")
    print("├──────────┼──────────┼──────────┼──────────┼──────────┤")
    
    # 新版机器人行
    new_no_double = stats['new_robot']['no_double']['total']
    new_double = stats['new_robot']['double']['total']
    new_super_double = stats['new_robot']['super_double']['total']
    new_total = stats['new_robot']['total']['total']
    
    print(f"│ 新版机器人│ {format_number(new_no_double):^8} │ {format_number(new_double):^8} │ {format_number(new_super_double):^8} │ {format_number(new_total):^8} │")
    
    # 旧版机器人行
    old_no_double = stats['old_robot']['no_double']['total']
    old_double = stats['old_robot']['double']['total']
    old_super_double = stats['old_robot']['super_double']['total']
    old_total = stats['old_robot']['total']['total']
    
    print(f"│ 旧版机器人│ {format_number(old_no_double):^8} │ {format_number(old_double):^8} │ {format_number(old_super_double):^8} │ {format_number(old_total):^8} │")
    
    # 差值行
    diff_no_double = stats['difference']['no_double']['total']
    diff_double = stats['difference']['double']['total']
    diff_super_double = stats['difference']['super_double']['total']
    diff_total = stats['difference']['total']['total']
    
    print(f"│ 差值     │ {format_number(diff_no_double):^8} │ {format_number(diff_double):^8} │ {format_number(diff_super_double):^8} │ {format_number(diff_total):^8} │")
    print("└──────────┴──────────┴──────────┴──────────┴──────────┘")
    
    # 打印详细统计
    print("\n详细统计：")
    print(f"新版机器人平均净赢银：{format_number(stats['new_robot']['total']['avg'], comma=False)}")
    print(f"旧版机器人平均净赢银：{format_number(stats['old_robot']['total']['avg'], comma=False)}")
    
    # 计算胜率差异
    new_win_rate = stats['new_robot']['total']['wins'] / stats['new_robot']['total']['count'] if stats['new_robot']['total']['count'] > 0 else 0
    old_win_rate = stats['old_robot']['total']['wins'] / stats['old_robot']['total']['count'] if stats['old_robot']['total']['count'] > 0 else 0
    win_rate_diff = new_win_rate - old_win_rate
    
    print(f"新版机器人胜率优势：{win_rate_diff:.2%}")
    
    # 打印加倍动作效果分析
    print("\n加倍动作效果分析：")
    
    # 新版机器人不同加倍动作
    print("新版机器人：")
    for action, label in [('no_double', '不加倍'), ('double', '加倍'), ('super_double', '超级加倍')]:
        s = stats['new_robot'][action]
        win_rate = s['wins'] / s['count'] if s['count'] > 0 else 0
        print(f"  {label}: 净赢银总计 = {format_number(s['total'])}, 平均净赢银 = {format_number(s['avg'], comma=False)}, 胜率 = {win_rate:.2%}")
    
    # 旧版机器人不同加倍动作
    print("\n旧版机器人：")
    for action, label in [('no_double', '不加倍'), ('double', '加倍'), ('super_double', '超级加倍')]:
        s = stats['old_robot'][action]
        win_rate = s['wins'] / s['count'] if s['count'] > 0 else 0
        print(f"  {label}: 净赢银总计 = {format_number(s['total'])}, 平均净赢银 = {format_number(s['avg'], comma=False)}, 胜率 = {win_rate:.2%}")

# 原始的净赢银统计结果部分
print("\n=== 净赢银统计结果 ===")
print("新版机器人：")

# 统计新版机器人不同加倍动作下的净赢银
if len(double_robot_df_dz_no_double) > 0:
    net_win_total = double_robot_df_dz_no_double['net_win'].sum()
    print(f"  不加倍(1): 净赢银总计 = {net_win_total:,}")
else:
    print("  不加倍(1): 净赢银总计 = 无数据")

if len(double_robot_df_dz_double) > 0:
    net_win_total = double_robot_df_dz_double['net_win'].sum()
    print(f"  加倍(2): 净赢银总计 = {net_win_total:,}")
else:
    print("  加倍(2): 净赢银总计 = 无数据")

if len(double_robot_df_dz_super_double) > 0:
    net_win_total = double_robot_df_dz_super_double['net_win'].sum()
    print(f"  超级加倍(4): 净赢银总计 = {net_win_total:,}")
else:
    print("  超级加倍(4): 净赢银总计 = 无数据")

print("\n旧版机器人：")

# 统计旧版机器人不同加倍动作下的净赢银
if len(double_old_robot_df_dz_no_double) > 0:
    net_win_total = double_old_robot_df_dz_no_double['net_win'].sum()
    print(f"  不加倍(1): 净赢银总计 = {net_win_total:,}")
else:
    print("  不加倍(1): 净赢银总计 = 无数据")

if len(double_old_robot_df_dz_double) > 0:
    net_win_total = double_old_robot_df_dz_double['net_win'].sum()
    print(f"  加倍(2): 净赢银总计 = {net_win_total:,}")
else:
    print("  加倍(2): 净赢银总计 = 无数据")

if len(double_old_robot_df_dz_super_double) > 0:
    net_win_total = double_old_robot_df_dz_super_double['net_win'].sum()
    print(f"  超级加倍(4): 净赢银总计 = {net_win_total:,}")
else:
    print("  超级加倍(4): 净赢银总计 = 无数据")


# 如果是直接运行脚本
if __name__ == "__main__":
    # 使用增强版净赢银统计功能
    print("\n开始生成增强版净赢银统计...")
    
    # 整理数据结构以供统计函数使用
    new_robot_dfs = {
        'no_double': double_robot_df_dz_no_double,
        'double': double_robot_df_dz_double,
        'super_double': double_robot_df_dz_super_double
    }
    
    old_robot_dfs = {
        'no_double': double_old_robot_df_dz_no_double,
        'double': double_old_robot_df_dz_double,
        'super_double': double_old_robot_df_dz_super_double
    }
    
    # 创建输出目录
    output_dir = "robot_analysis_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 进行全面分析并生成可视化结果
    print("\n开始进行全面分析并生成可视化结果...")
    analysis_result = analyze_and_visualize(new_robot_dfs, old_robot_dfs, output_dir)
    
    print("\n分析完成，结果已保存到目录:", os.path.abspath(output_dir))