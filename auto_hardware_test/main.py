#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from auto_hardware_test.utils.test_put_files import *
from auto_hardware_test.utils.test_base_install import *
from auto_hardware_test.utils.test_base_net import *
from auto_hardware_test.utils.test_capture import *
from auto_hardware_test.utils.log_to_excel import *
from auto_hardware_test.utils.test_base_disk import *
from auto_hardware_test.utils.test_hardware import *

if __name__ == '__main__':
    config_path = "config.conf"
    sections = Config.get_conf_sections(config_path)     #['case', 'ssh1', 'ssh2', 'ssh3']
    excel = "服务器性能测试结果统计.xlsx"

    # 创建客户机服务器文件夹
    cmd = "cd /home/;mkdir auto_capture_log"
    Install.sftp_shell(config_path, sections, cmd)

    # 创建被测服务器磁盘基准测试日志文件夹
    cmd = "cd /home/auto_capture_log/;mkdir log_data;mkdir log_disk;mkdir log_writeback"
    Multiprocess.stfp_multiprocess_cmd(config_path, sections[1], cmd)
    cmd = "cd /home/auto_capture_log/;rm -rf log_data/*;rm -rf log_disk/*;rm -rf log_writeback/*"
    Multiprocess.stfp_multiprocess_cmd(config_path, sections[1], cmd)


    # 第一步：下发测试脚本------------------------------------------------------------------------
    local_dir, remote_dir = r"./files", "/home/"
    # unzip -o覆盖原先的文件；
    cmd = "cd /home/;unzip -o auto_capture.zip;unzip -o install_base.zip"
    Put_Files.test_upload_run(config_path, local_dir, remote_dir, cmd)

    #  第二步：运行环境优化脚本-----------------------------------------------------------------
    node, key = "case", "install"
    for i in range(1, len(sections)):
        hostname = Config.read_config(config_path, sections[i], "hostname")
        server = Config.read_config(config_path, "case", "server")
        if server.__eq__("read"):
            cmd = "cd /home/install_base/;sh main.sh read " + hostname
            print("read---" + hostname)
            Install.test_install(config_path, node, key, cmd, sections[i])
        if server.__eq__("write"):
            cmd = "cd /home/install_base/;sh main.sh write " + hostname
            print("write---" + hostname)
            Install.test_install(config_path, node, key, cmd, sections[i])

    # 升级内核需要重启服务器
    # # time.sleep(300)
    #
    # # 第三步：运行硬件基准测试--------------------------------------------------------------------------------
    # # 3.1运行网卡带宽基准测试
    # # node, key = "case", "test_net"
    # # sections = Config.get_conf_sections(config_path)
    # # ip_s = Config.read_config(config_path, "ssh1", "host")
    # # cmd_s = "iperf -s"
    # # cmd_c = "iperf -c " + ip_s + " -i 1 -t 10 -P 12 > /home/auto_capture_log/iperf.log"
    # Network.test_iperf(config_path, node, key, cmd_s, cmd_c)
    # 3.2生成并运行磁盘基准测试
    # # 如果本地存在fio測試腳本即刪除
    # # fio_data = "fiotest_data.sh"
    # # fio_disk = "fiotest_disk.sh"
    # # fio_writeback = "fiotest_writeback.sh"
    # # if os.path.exists(fio_data):
    # #     os.remove(fio_data)
    # # if os.path.exists(fio_disk):
    # #     os.remove(fio_disk)
    # # if os.path.exists(fio_writeback):
    # #     os.remove(fio_writeback)
    # # node, key = "case", "test_disk"
    # # remote_way = "/home/auto_capture_log/"
    # # BaseDisk.test_disk_base(config_path, node, key, remote_way)


    # 第四步：修改配置并做包、运行capture压测工具--------------------------------------------------------------------
    # 运行capture压测
    local_capture_config, remote_capture_config = "log/temp/config.ini", "/home/auto_capture/auto_capture/config.ini"
    local_decom, remote_decom = "log/temp/decom.json", "/home/auto_capture/auto_capture/new_capture/decom.json"
    local_package, remote_package = "log/temp/1h.pac", "/home/auto_capture/auto_capture/new_capture/1h.pac"
    local_data_log, remote_data_log = "log/temp/", "/home/auto_capture/auto_capture/test/"
    Capture.test_capture_run(config_path, local_capture_config, remote_capture_config, local_decom, remote_decom, local_package, remote_package, local_data_log, remote_data_log)


    # 第五步：收集日志---------------------------------------------------------------------------------------------------

    # 搜集各服务器ip，包括被测服务器、模拟客户机服务器，回写到各表格；
    sections = Config.get_conf_sections(config_path)
    serverIP_list = []
    for i in range(1, len(sections)):
        section = sections[i]
        ip = Config.read_config(config_path, section, "host")  # 获取配置文件服务器ip；获取实际服务器ip：ip = subprocess.getoutput("ifconfig | grep 'inet' | awk 'NR==1{print}' | sed 's/\s\+/,/g' | cut -d',' -f3").__str__().replace("b'", "").replace("\\n'", "")
        serverIP_list.append(ip)
    print("serverIP_list:", serverIP_list)
    # # 将ip回写到Excel中用例case
    sheetname = "软硬件环境"
    sheetname2 = "网卡基准测试"
    sheetname3 = "capture压测客户端统计"
    sheetname4 = "capture压测服务端统计"
    row = 3
    column = 3
    Excel.write_excel_xlsx(excel, sheetname4, row, 2, serverIP_list[0])  # 写入capture压测服务端统计表
    for ip in serverIP_list:
        Excel.write_excel_xlsx(excel, sheetname, row, column, ip)  # 写入软硬件环境表
        Excel.write_excel_xlsx(excel, sheetname2, row, column, ip)  # 写入网卡基准测试表
        Excel.write_excel_xlsx(excel, sheetname3, row, column, ip)  # 写入capture压测客户端统计表
        row += 1

    # # # 收集网卡带宽基准测试日志
    # # sections = Config.get_conf_sections(config_path)
    # # cmd = "find /home/auto_capture_log/ -name '*net.log' | awk 'END {print}'" # find查找默认按修改时间正序排列，awk 'END {print}'获取排序的最后一个值
    # # local_dir = r"log/"
    # # for i in range(2, len(sections)):
    # #     section = sections[i]
    # #     Put_Files.remote_get_file(config_path, section, cmd, local_dir)
    # #
    # # # 收集磁盘基准测试日志
    # # remote_dir = "/home/auto_capture_log/"
    # # local_dir = "log/"
    # # log_path_list = ["log_data/", "log_disk/", "log_writeback/"]
    # # for log_path in log_path_list:
    # #     sections = Config.get_conf_sections(config_path)
    # #     Multiprocess.sftp_get_dir(config_path, sections[1], remote_dir+log_path, local_dir+log_path)

    # 收集服务器游戏、镜像、回写服务日志
    data_log = "find /swyun/log/ -name 'dataservice_*.log' | awk 'END {print}'" # find查找默认按修改时间正序排列，awk 'END {print}'获取排序的最后一个值
    disk_log = "find /swyun/log/ -name 'diskservice_*.log' | awk 'END {print}'" # find查找默认按修改时间正序排列，awk 'END {print}'获取排序的最后一个值
    writeback_log = "find /swyun/log/ -name 'writeback_*.log' | awk 'END {print}'" # find查找默认按修改时间正序排列，awk 'END {print}'获取排序的最后一个值
    local_dir = "log/"
    server = Config.read_config(config_path, "case", "server")
    if server.__eq__("read"):
        Put_Files.remote_get_file(config_path, sections[1], data_log, local_dir)
        Put_Files.remote_get_file(config_path, sections[1], disk_log, local_dir)        #将储存在服务器上的日志复制到本地
    elif server.__eq__("write"):
        Put_Files.remote_get_file(config_path, sections[1], writeback_log, local_dir)
    else:
        print("请正确填写服务！")

    # 收集客户机服务器count统计日志
    sections = Config.get_conf_sections(config_path)
    log_path = "cd /home/auto_capture/auto_capture/;ls -tr *count*.log | awk '{print i$0}' i=`pwd`'/' | awk 'END {print}'" # ls -r 将文件以相反次序显示(原定依英文字母次序),-t 将文件依建立时间之先后次序列出；awk 'END {print}'获取排序的最后一个值
    local_dir = r"log/"
    for i in range(2, len(sections)):
        section = sections[i]
        Put_Files.remote_get_file(config_path, section, log_path, local_dir)


    # 搜集被测服务器、客户机服务器的CPU、内存、网卡信息列表，并写入Excel
    # CPU线程数/CPU型号
    cpu_list = Hardware.get_cpu(config_path)
    row = 3
    column = 5
    for cpu in cpu_list:
        Excel.write_excel_xlsx(excel, sheetname, row, column, cpu)
        row += 1
    # CPU颗数
    cpu_num_list = Hardware.get_cpu_num(config_path)
    row = 3
    column = 6
    for cpu_num in cpu_num_list:
        Excel.write_excel_xlsx(excel, sheetname, row, column, cpu_num)
        row += 1
    # 内存总量
    mem_list = Hardware.get_mem_total(config_path)
    row = 3
    column = 7
    for mem in mem_list:
        Excel.write_excel_xlsx(excel, sheetname, row, column, mem)
        row += 1
    # 网卡型号
    net_list = Hardware.get_net_list(config_path)
    row = 3
    column = 8
    for net in net_list:
        Excel.write_excel_xlsx(excel, sheetname, row, column, net)
        row += 1
    # 操作系统/内核版本
    OS_list = Hardware.get_OS_list(config_path)
    kernel_list = Hardware.get_kernel_list(config_path)
    row = 3
    column = 12
    for OS, kernel in zip(OS_list, kernel_list):
        Excel.write_excel_xlsx(excel, sheetname, row, column, OS+"\n"+kernel)  # 换行写入
        # print(OS, kernel)
        row += 1


    # 第六步：解析日志----------------------------------------------------------------------------------------------------------------------

    # 导出网卡基准测试日志到Excel


    # 导出磁盘基准测试日志到Excel
    # 读取磁盘基准测试fio日志，并将延迟等回写到Excel
    sheetname_list = ["磁盘基准测试-游戏盘", "磁盘基准测试-镜像盘", "磁盘基准测试-回写盘"]
    log_path_list = ["log/log_data/", "log/log_disk/", "log/log_writeback/"]
    for sheetname, log_path in zip(sheetname_list, log_path_list):
        log_path_key = log_path + "fiotest*.log"
        LogToExcel.write_fio_Excel(excel, sheetname, log_path, log_path_key)


    # 导出服务器游戏、镜像、回写服务日志到Excel
    # 读取游戏服务日志并写入Excel
    sheetname = "capture压测服务端统计"
    file_path = "log/"
    file_path_key = file_path + "dataservice_*.log"
    casename="dataservice"
    LogToExcel.write_service_Excel(excel, sheetname, file_path, file_path_key, casename)


    # 读取镜像服务日志并写入Excel
    file_path_key = file_path + "diskservice_*.log"
    casename = "diskservice"
    LogToExcel.write_service_Excel(excel, sheetname, file_path, file_path_key, casename)

    # 读取回写服务日志并写入Excel
    file_path_key = file_path + "writeback_*.log"
    casename = "writeback"
    LogToExcel.write_service_Excel(excel, sheetname, file_path, file_path_key, casename)

    # 导出count日志到Excel
    # 读取客户端count日志并提取延迟区间写入Excel
    sheetname = "capture压测客户端统计"
    file_path = "log/"
    sections = Config.get_conf_sections(config_path)
    print(sections)
    for i in range(2, len(sections)):
        section = sections[i]
        ip = Config.read_config(config_path, section, "host")
        file_path_key = file_path + ip.__str__() + "_count_*.log"
        print("ip---", ip)
        LogToExcel.write_count_Excel(excel, sheetname, file_path, file_path_key, ip)
