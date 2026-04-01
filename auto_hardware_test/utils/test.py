#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, subprocess, re
# from auto_hardware_test.utils.log_to_excel import *
# cmd = "adb shell 'grep total_request ../log/172.17.7.40_count_total_row'"
# print(cmd)
# log_list = Log.get_key_line("../log/172.17.7.40_count_20201103_175145.log", "total_request")
# print(log_list[len(log_list)-1])
#
# log_list2 = Log.get_key_line("../log/dataservice_20201103.log", "[gameservice_dump]|total")
# last_line = log_list2[len(log_list2)-1]

# file_path_key = "../log/dataservice_*.log"
# context_key_word = "[gameservice_dump]|total"
# new_file = "test.log"
# Log.get_last_line(file_path_key, context_key_word, new_file)
#
# file_path_key="../log/*_count_*.log"
# context_key_word = "total_request"
# new_file = "count.log"
# Log.get_last_line(file_path_key, context_key_word, new_file)

import re,os
# from auto_hardware_test.utils.log_to_excel import *

def alter(file,old_str,new_str):

    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(re.sub(old_str,new_str,line))
    os.remove(file)
    os.rename("%s.bak" % file, file)

# 通过後綴模糊匹配，获得指定路径下最後文件名
def get_last_log(log_path):
    files = os.listdir(log_path)
    file_list = []
    for f in files:
        if 'dataservice' in f and f.endswith('.log'):
            file_list.append(f)
            print("Found it! " + f)
    print("file_list", file_list)
    return file_list[len(file_list)-1]

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
python 文件中接受 shell 中的 参数
'''
import sys, time

def YKenan():
    # time.sleep(int(sys.argv[1]))
    # print(sys.argv[1], sys.argv[2], sys.argv[3])

    # 传入一个参数，如果是读服务器/写服务器运行十一分钟/一小时三十分钟，结束统计时间
    try:
        if sys.argv[1].__eq__("read"):
            print("read server test，sleep 660s...")
            time.sleep(10)
        if sys.argv[1].__eq__("write"):
            print("write server test，sleep 5400s...")
            time.sleep(60)
    except Exception as e:
        print(e)
    finally:
        # 每隔60s检查一次，如果满足条件则杀掉进程并结束循环
        while True:
            play_num = int(subprocess.getoutput("ps -ef | grep play | wc -l"))
            print("目前有play_num:", play_num.__str__())
            if play_num <= 2:
                subprocess.getoutput("pkill -2 count")
                print("pkill -2 count")
                break
            time.sleep(60)

'''
如果上面的 加入 sys.argv[0] 则，sys.argv[0] 的结果为 python 文件名字
'''


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        print(file_path, "文件目录为空！")
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        print(dir_list)
        return dir_list


if __name__ == "__main__":
    # YKenan()

    # import psutil
    #
    # mem = psutil.virtual_memory()
    # print(mem)
    #
    # disk = psutil.disk_io_counters()
    # print(disk)
    #
    # str = re.findall("a.+?b", "aabbcc")
    # print(type(str))
    #
    # li = [1]
    # li.insert(0, 2323)
    # if li:
    #     print("li:", li)



    get_file_list(r"../log/")
