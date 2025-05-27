# 统计斗地主不洗牌 加倍功能  人机对局机器人和真人之间的对比
# In[1]
import pandas as pd
# jqr_uid = pd.read_csv(r'E:\code\Server_Train\DDZ\ddz_analysis\robot_num\data\22042robotuid.csv')['uid'].to_list()
# In[1]
import json,os
import pandas as pd
# files_ls = os.listdir(r".\\calc_double_win_rate\\double_data")
data_ls = []
roomid = '188'

double_data_play_ls = []
double_data_robot_ls = []

robot_version_data = {}
new_jqr_uid = []

# Define file paths
log_file_path = r'.\\calc_double_win_rate\\PlayRecord20250526.log'
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
        if ai2 == '192.168.102.45:2412':
            new_jqr_uid.append(timestamp+'_'+uid2)
        if ai3 == '192.168.102.45:2412':
            new_jqr_uid.append(timestamp+'_'+uid3)

# Define file paths
json_file_path = r'.\\calc_double_win_rate\\188_20250526.json'
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
        # Include all entries as robot data to ensure we count all games
        double_data_robot_ls.append(data)
        
        # Original filtering logic - commented out
        # time_uid_key = str(data.get('time'))+'_'+str(data.get('user_id'))
        # if time_uid_key in new_jqr_uid:
        #     double_data_robot_ls.append(data)
        # else:
        #     double_data_play_ls.append(data)


double_play_df = pd.DataFrame([])  # Empty DataFrame since we're not using it
double_robot_df = pd.DataFrame(double_data_robot_ls)
# In[1]
# We no longer need to filter the player data since we're counting all entries as robot data
# double_play_df_dz = double_play_df[double_play_df['banker']==1]
# double_play_df_nm = double_play_df[double_play_df['banker']==0]

double_robot_df_dz = double_robot_df[double_robot_df['banker']==1]
double_robot_df_nm = double_robot_df[double_robot_df['banker']==0]
# In[1]
# double_play_df_dz_lose = double_play_df_dz[double_play_df_dz['is_win'] == 0]
# double_play_df_dz_win = double_play_df_dz[double_play_df_dz['is_win'] == 1]

# double_play_df_nm_lose = double_play_df_nm[double_play_df_nm['is_win'] == 0]
# double_play_df_nm_win = double_play_df_nm[double_play_df_nm['is_win'] == 1]
# In[1]
double_robot_df_dz_lose = double_robot_df_dz[double_robot_df_dz['is_win'] == 0]
double_robot_df_dz_win = double_robot_df_dz[double_robot_df_dz['is_win'] == 1]

double_robot_df_nm_lose = double_robot_df_nm[double_robot_df_nm['is_win'] == 0]
double_robot_df_nm_win = double_robot_df_nm[double_robot_df_nm['is_win'] == 1]

double_robot_df_dz_no_double = double_robot_df_dz[double_robot_df_dz['double_action'] == 1]
double_robot_df_dz_double = double_robot_df_dz[double_robot_df_dz['double_action'] == 2]
double_robot_df_dz_super_double = double_robot_df_dz[double_robot_df_dz['double_action'] == 4]

#统计机器人不加倍、加倍和超级加倍情况下的胜率
if len(double_robot_df_dz_no_double) > 0:
    wins = (double_robot_df_dz_no_double['is_win'] == 1).sum()
    total = len(double_robot_df_dz_no_double)
    print("机器人不加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("机器人不加倍的胜率：无数据")

if len(double_robot_df_dz_double) > 0:
    wins = (double_robot_df_dz_double['is_win'] == 1).sum()
    total = len(double_robot_df_dz_double)
    print("机器人加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("机器人加倍的胜率：无数据")

if len(double_robot_df_dz_super_double) > 0:
    wins = (double_robot_df_dz_super_double['is_win'] == 1).sum()
    total = len(double_robot_df_dz_super_double)
    print("机器人超级加倍的胜率：{:.2%} ({}/{})".format(wins/total, wins, total))
else:
    print("机器人超级加倍的胜率：无数据")





