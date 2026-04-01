#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from auto_hardware_test.utils import connectClient
from auto_hardware_test.utils.test_base_install import *
import threading
import os


class Network:
    # 连接客户端服务器，执行命令
    def sftp_exec_shell(ip, port, username, password, cmd):
        # for i in range(60):

        conn = connectClient.SSHConnection(remote_ip=ip, remote_port=port, ssh_username=username,
                                       ssh_password=password)
        result = conn.sftp_exec_shell(cmd)
            # if "refused" in str(result,encoding="utf-8"):
            #     continue
            # else:
            #     return result

    def iperf_threading(config, sections, cmd_s, cmd_c):
        for i in range(2, len(sections)):
            ip = Config.read_config(config, sections[i], "host")
            port = Config.read_config(config, sections[i], "port")
            username = Config.read_config(config, sections[i], "username")
            password = Config.read_config(config, sections[i], "password")
            if i == 2:
                subthread = threading.Thread(target=Network.sftp_exec_shell, args=(ip, port, username, password, cmd_s,))
                subthread.start()
                print(ip, " \'"+cmd_s+"\' 已启动!")
                continue
            time.sleep(10)
            subthread = threading.Thread(target=Network.sftp_exec_shell, args=(ip, port, username, password, cmd_c,))
            subthread.start()
            print(ip, " \'"+cmd_c+"\' 已启动!")

    # 判断是否运行网卡测试，并执行多线程ssh
    def test_network_run(config, node, key, cmd_s, cmd_c):
        flag = int(Config.read_config(config, node, key))
        print(flag)
        if flag:
            sections = Config.get_conf_sections(config)
            print("sections------------", sections)
            Network.iperf_threading(config, sections, cmd_s, cmd_c)
        else:
            print("已跳过网卡测试！")

if __name__ == '__main__':
    # # 连接客户端服务器并上传文件
    # remote_ip = '172.17.7.41'
    # remote_port = 22
    # ssh_username = 'root'
    # ssh_password = 'abc#123'

    # conn = connectClient.SSHConnection(remote_ip=remote_ip, remote_port=remote_port, ssh_username=ssh_username,
    #                      ssh_password=ssh_password)
    # conn.sftp_put_dir("D:\\Program Files\\Works\Coding\\auto_hardware_test\\auto_hardware_test", "/home/test/")
    # # conn.sftp_put_file("D:\\Program Files\\Works\Coding\\auto_hardware_test\\auto_hardware_test\\files\\auto_capture.zip", "/home/test/auto_capture.zip")
    # # 如果unzip不存在，则安装
    # unzip = conn.sftp_exec_shell("yum list | grep unzip | wc -l")
    # if unzip == 0:
    #     conn.sftp_exec_shell("yum install -y unzip")
    # conn.sftp_exec_shell("cd /home/test/;unzip auto_capture.zip")


    # 判断是否安装内核4.18
    # ip = "172.17.7.40"
    # port = 22
    # username = "root"
    # password = "abc#123"
    #
    # cmd_s = "iperf -s"
    # cmd_c = "iperf -c " + ip + " -i 1 -t 1000 -P 12 > /home/" + ip + "_iperf.log"
    #
    # uname = "ip addr"
    # config, nofe, key = "config.conf", "service", "test_net"
    # # 运行iperf服务端
    # subthread = threading.Thread(target=Install.isRun_local, args=(config, nofe, key, cmd_s))
    # subthread.start()
    # # 运行iperf客户端
    # Install.isRun_sftp(ip, port, username, password, config, nofe, key, cmd_c)

    config, node, key = "../config.conf", "case", "test_net"
    sections = Config.get_conf_sections(config)
    ip_s = Config.read_config(config, "ssh1", "host")
    print("ip_s:", ip_s)
    cmd_s = "iperf -s -p 9999"
    cmd_c = "iperf -c " + ip_s + " -p 9999 -i 1 -t 10 -P 12 > /home/iperf.log"
    Network.test_network_run(config, node, key, cmd_s, cmd_c)
