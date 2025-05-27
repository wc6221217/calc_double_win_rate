# encoding=utf-8
import os,json,copy
import multiprocessing as mp
from collections import deque

import pandas as pd
# jqr_uid = pd.read_csv(r'E:\code\Server_Train\DDZ\ddz_analysis\robot_num\data\22042robotuid.csv')['uid'].to_list()
def get_call_rob_data(file,i):
    print(i,file)
    all_data = []
    # rob_all_data = []
    with open(r'.\\logs\\{}'.format(file), "r", encoding='gb18030',errors='ignore') as f:
    # with open(r'D:\ddz_double\ddz_double\{}'.format(file), "r", encoding='gb18030',errors='ignore') as f:
    # with open(r'E:\code\Server_Train\DDZ\ddz_bxp\datadeal\data\middle_data\game\zgdasvr\Record\{}'.format(file),
    #           "r", encoding='gb18030', errors='ignore') as f:
        f = f.readlines()
        throw_chair = deque(maxlen=15)
        banker = None
        double_data = []
        for i, line in enumerate(f):

            line = line.replace('\n', '')
            # 将读取的数据转为列表
            linels = line.split(' ')

            if linels[0] == 'Version':
                #初始化

                if banker != None:
                    win_chair = int(throw_chair[-1])

                    if win_chair == banker:
                        for d_data in double_data:
                            if d_data.get('chair_no') == d_data.get('banker'):
                                d_data['is_win'] = 1
                            else:
                                d_data['is_win'] = 0
                    else:
                        for d_data in double_data:
                            if d_data.get('chair_no') == d_data.get('banker'):
                                d_data['is_win'] = 0
                            else:
                                d_data['is_win'] = 1

                    all_data.extend(double_data)


                double_data = []

                hand_tile_dic = {0:'',1:'',2:''}
                chairno_dic = {0:None,1:None,2:None}
                is_robot_dict = {0: False, 1: False, 2: False}
                call_label_dict = {0: -1, 1: -1, 2: -1}
                rob_label_dict = {0: -1, 1: -1, 2: -1}
                double_label_dict = {0: -1, 1: -1, 2: -1}

                is_have_jqr = False

            if linels[0] == 'Timestamp':
                timestamp = linels[1]

            is_have_jqr = True
            if linels[0] == 'ChairNO':
                #存储用户id
                chairno_dic[int(linels[1])] = int(linels[2])
            #     if int(linels[2]) in jqr_uid:
            #         is_have_jqr = True
            #         # is_robot_dict[int(linels[1])] = True

            if linels[0] == 'Deal':
                hand_tile_dic[int(linels[1])] = linels[2][1::2]

            if linels[0] == 'Call':

                call_label_dict[int(linels[1])] = int(linels[2])
            if linels[0] == 'Rob':

                rob_label_dict[int(linels[1])] = int(linels[2])


            if linels[0] == 'Bottom':
                bottom = linels[2][1::2]
                hand_tile_dic[int(linels[1])] += linels[2][1::2]
                banker = int(linels[1])


            if linels[0].capitalize() == 'Double':
                # if is_robot_dict[int(linels[1])] == False:
                if is_have_jqr:
                    # if int(linels[2]) != 0:

                    if int(linels[2]) == 1:
                        double_action = 2
                    elif int(linels[2]) == 2:
                        double_action = 4
                    else:
                        double_action = 1

                    data = {
                        'chair_no':int(linels[1]),
                        'user_id':chairno_dic[int(linels[1])],
                        'hand_tile': hand_tile_dic[int(linels[1])],
                        'banker':banker,
                        'bottom': bottom,
                        'his_call': copy.deepcopy(call_label_dict),
                        'his_rob': copy.deepcopy(rob_label_dict),
                        'his_double': copy.deepcopy(double_label_dict),
                        'double_action': double_action,
                        'time':timestamp,
                        'key':file[6:14]+'_'+str(timestamp)+'_'+str(chairno_dic[int(linels[1])])
                    }
                    double_data.append(data)

                double_label_dict[int(linels[1])] = int(linels[2])

            if linels[0] == 'Throw' or 'AutoThrow':
                throw_chair.append(linels[1])

    for index, data in enumerate(all_data):
        data_dumps = json.dumps(data)

        with open(r'.\\{}.json'.format(file[:-7]), 'a', encoding='utf-8') as f:
        # with open(r'D:\ddz_double\datadeal\{}.json'.format(file[:-7]), 'a', encoding='utf-8') as f:
            json.dump(data_dumps, f)
            f.write("\n")

    # for index, data in enumerate(rob_all_data):
    #     data_dumps = json.dumps(data)
    #
    #     with open(r'./call_rob_data/rob/{}.json'.format(file[:-7]), 'a', encoding='utf-8') as f:
    #         json.dump(data_dumps, f)
    #         f.write("\n")


if __name__ == "__main__":

    # log_files = os.listdir(r"E:\code\Server_Train\DDZ\ddz_bxp\datadeal\data\middle_data\game\zgdasvr\Record")
    # log_files = os.listdir(r"D:\jqrdouble")
    # log_files = os.listdir(r"E:\code\Server_Train\DDZ\ddz_analysis\robot_num\logs")
    log_files = os.listdir(r".\\logs")
    select_log_files = [fille for fille in log_files if fille[:3] in ['188']]
    # target_dir = 'E:\code\Server_Train\DDZ\ddz_analysis\\robot_num\double_data'
    target_dir = '.\\'

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(len(select_log_files))
    pool = mp.Pool(4)
    for i, log_file in enumerate(select_log_files):
        pool.apply_async(get_call_rob_data,args=(log_file, i))


    pool.close()
    pool.join()
    print("ok!")