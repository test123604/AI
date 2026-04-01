#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os, time
import paramiko
from multiprocessing import Pool
from auto_hardware_test.utils.log_to_excel import Config, Log
from auto_hardware_test.utils.multiprocess import Multiprocess
from auto_hardware_test.utils.test_put_files import Put_Files


class Capture:
    # 多线程远程压测服务器执行命令
    def sftp_shell(config_path, sections, cmd):
        start = time.time()
        pool = Pool()
        for i in range(2, len(sections)):
            pool.apply_async(Multiprocess.stfp_multiprocess_cmd, args=(config_path, sections[i], cmd,))
            print("section---", sections[i])
        pool.close()
        pool.join()
        print(time.time() - start)

    # 判断读写服务器类型，并返回命令
    # def test_server(config_path, node, key, cmd_r, cmd_w, cmd_mv_package, local_decom, remote_decom, local_package, remote_package):
    #     server = Config.read_config(config_path, node, key)
    #     if server.__eq__("read"):
    #         print("read server")
    #         return cmd_r
    #     if server.__eq__("write"):
    #         print("write server")
    #         sections = Config.get_conf_sections(config_path)
    #         for i in range(2, len(sections)):
    #             Multiprocess.sftp_put_file(config_path, sections[i], local_decom, remote_decom)
    #             Multiprocess.stfp_multiprocess_cmd(config_path, sections[i], cmd_mv_package)
    #             Multiprocess.sftp_put_file(config_path, sections[i], local_package, remote_package)
    #         return cmd_w
    #     else:
    #         print("请正确填写服务器！")


    # 判断是否做包，并执行ssh
    def test_make_package(config_path, node, key, key_server, cmd_r, cmd_w, cmd_mv_package, local_decom, remote_decom, local_package, remote_package):
        flag = int(Config.read_config(config_path, node, key))  # 把str转换成int
        print(flag)
        flag_server = Config.read_config(config_path, node, key_server)
        print(flag_server)

        # 如果为1，则为是，运行做包
        if flag:
            sections = Config.get_conf_sections(config_path)
            print("sections------------", sections)
            if flag_server.__eq__("read"):
                print("read server--make pckage")
                # cmd = Capture.test_server(config_path, node, key_server, cmd_r, cmd_w, cmd_mv_package, local_decom, remote_decom, local_package, remote_package)
                # 运行读服务器做包
                Capture.sftp_shell(config_path, sections, cmd_r)
            if flag_server.__eq__("write"):
                print("write server--make pckage")
                start = time.time()
                pool = Pool()
                for i in range(2, len(sections)):
                    # 上传decom.json
                    Multiprocess.sftp_put_file(config_path, sections[i], local_decom, remote_decom)
                    # 修改1h.pac，备注为1h.pac_read
                    Multiprocess.stfp_multiprocess_cmd(config_path, sections[i], cmd_mv_package)
                    # 上传写数据包1h.pac；使用多线程方式，以便提升效率；
                    # Multiprocess.sftp_put_file(config_path, sections[i], local_package, remote_package)
                    pool.apply_async(Multiprocess.sftp_put_file, args=(config_path, sections[i], local_package, remote_package,))
                pool.close()
                pool.join()
                print("write server--upload file time:", time.time() - start)
                # 运行写服务器做包
                Capture.sftp_shell(config_path, sections, cmd_w)
        else:
            print("已跳过做包过程！")

    # 判断是否运行capture，并执行ssh
    def test_capture(config, node, key, cmd):
        flag = int(Config.read_config(config, node, key))
        print(flag)
        # 如果为1，则为是，运行压测
        if flag:
            sections = Config.get_conf_sections(config)
            print("sections------------", sections)
            # 如果是读服务器，运行读压测
            Capture.sftp_shell(config, sections, cmd)
        else:
            print("已跳过运行capture压测过程！")

    # 运行压测
    def test_capture_run(config_path, local_capture_config, remote_capture_config, local_decom, remote_decom, local_package, remote_package, local_data_logpath, remote_data_logpath):
        #'''
        # 如果做包，则运行准备做包文件；否则不准备，以节约时间；
        make_package = int(Config.read_config(config_path, "case", "make_package"))
        sections = Config.get_conf_sections(config_path)
        if make_package:
            # 一、删除数据服务日志并重启顺网雲数据服务-------------------------------------------------------------------------------------------------------------
            cmd = "rm -rf /swyun/log/dataservice*.log;servermgr restart dataservice;servermgr status all"
            Multiprocess.stfp_multiprocess_cmd(config_path, sections[1], cmd)
            # 下载数据服务日志到本地，已被capture使用
            data_log = "find /swyun/log/ -name 'dataservice*.log' | awk 'END {print}'"  # find查找默认按修改时间正序排列，awk 'END {print}'获取排序的最后一个值
            getlog = Put_Files.remote_get_file(config_path, sections[1], data_log, local_data_logpath)

            # 格式化日志文件路径，获取日志名称并组装本地/远程日志路径
            logpath, logname = Log.formatFilePath(getlog)
            local_data_log = local_data_logpath + logname
            remote_data_log = remote_data_logpath + logname
            print("local_data_log:", local_data_log, "remote_data_log:", remote_data_log)
            # 再将下载的数据服务日志上传到客户机服务器capture/test下
            for i in range(2, len(sections)):
                section = sections[i]
                Multiprocess.sftp_put_file(config_path, section, local_data_log, remote_data_log)

        # 启动capture重新获取bar_num；
        # 修改capture的config.ini配置文件-------------------------------------------------------------------------------------------------------------
        serverIP = Config.read_config(config_path, "ssh1", "host")
        test_datadisk_size = Config.read_config(config_path, "case", "test_datadisk_size")
        # 修改服务器ip和数据盘大小； # 替换第N行整行为新的数据 sed -i -e '5s/.*/serverIP = ;-e 可以拼接替换;sed -i -e '5s/.*/serverIP = "+serverIP+"/g' -e '9s/.*/test_datadisk_size = " + test_datadisk_size + "/g' ./config.ini;

        # 正則匹配並替換serverIP
        regex = "(serverIP =.+)"
        key_word = "serverIP"
        old_str = Log.get_value_list(local_capture_config, regex, key_word)
        new_str = "serverIP = " + serverIP
        Log.alter(local_capture_config, old_str[1], new_str)

        # 正則匹配並替換test_datadisk_size
        regex = "(test_datadisk_size = .+)"
        key_word = "test_datadisk_size"
        old_str = Log.get_value_list(local_capture_config, regex, key_word)
        new_str = "test_datadisk_size = " + test_datadisk_size
        Log.alter(local_capture_config, old_str[1], new_str)

        # 遍历并修改客户机ip和网吧数;这里替换是对应客户端服务器；启动capture重新获取bar_num；
        for i in range(2, len(sections)):
            clientIP = Config.read_config(config_path, sections[i], "host")
            bar_num = Config.read_config(config_path, sections[i], "bar_num")

            # 正則匹配並替換clientIP
            regex = "(clientIP = .+)"
            key_word = "clientIP"
            old_str = Log.get_value_list(local_capture_config, regex, key_word)
            new_str = "clientIP = " + clientIP
            Log.alter(local_capture_config, old_str[1], new_str)

            # 正則匹配並替換bar_num
            regex = "(bar_num = .+)"
            key_word = "bar_num"
            old_str = Log.get_value_list(local_capture_config, regex, key_word)
            new_str = "bar_num = " + bar_num
            Log.alter(local_capture_config, old_str[1], new_str)

            # 上傳替換好的壓測配置文件，並轉為unix文件
            Multiprocess.sftp_put_file(config_path, sections[i], local_capture_config, remote_capture_config)
            cmd = "dos2unix /home/auto_capture/auto_capture/config.ini"  # sed -i -e '13s/.*/clientIP = " + clientIP + "/g' -e '15s/.*/bar_num = " + bar_num + "/g' ./config.ini;
            print(cmd)
            Multiprocess.stfp_multiprocess_cmd(config_path, sections[i], cmd)

        # 做包make_package
        node, key, key_server = "case", "make_package", "server"
        cmd_r = "cd /home/auto_capture/auto_capture/;python3 make_package.py;hostname"  # python3 make_package.py
        cmd_w = "cd /home/auto_capture/auto_capture/;python3 make_package_writeback.py;hostname"  # python3 make_package_writeback.py
        cmd_mv_package = "cd /home/auto_capture/auto_capture/new_capture/;mv 1h.pac 1h.pac_read;hostname"
        print("make_package...")
        Capture.test_make_package(config_path, node, key, key_server, cmd_r, cmd_w, cmd_mv_package, local_decom, remote_decom, local_package, remote_package)  # 做包

        # 启动压测capture（如已做包，可独立运行）
        # 一、清除服务器缓存并重启顺网雲服务---------------------------------------------------------------------
        print("服务端释放缓存！")
        sections = Config.get_conf_sections(config_path)
        cmd = "rm -rf /swyun/log/*;free -h;echo 3 > /proc/sys/vm/drop_caches;free -h;servermgr restart all;servermgr status all"
        Multiprocess.stfp_multiprocess_cmd(config_path, sections[1], cmd)

        # 二、清除客户机服务器缓存--------------------------------------------------------------------------------
        print("客户端释放缓存！")
        for i in range(2, len(sections)):
            section = sections[i]
            cmd = "free -h;echo 3 > /proc/sys/vm/drop_caches;free -h"
            Multiprocess.stfp_multiprocess_cmd(config_path, section, cmd)

        # 三、启动压测capture（如已做包，可独立运行），根据读/写服务器需要传参read/write，如：python3 run_capture.py read
        flag_server = Config.read_config(config_path, node, key_server)
        node, key = "case", "run_capture"
        run_capture = "cd /home/auto_capture/auto_capture/;python3 run_capture.py " + flag_server + ";hostname"
        print("run_capture...")
        Capture.test_capture(config_path, node, key, run_capture)

if __name__ == '__main__':
    config_path = "../config.conf"
    local_capture_config, remote_capture_config = "../log/temp/config.ini", "/home/auto_capture/auto_capture/config.ini"
    local_decom, remote_decom = "../log/temp/decom.json", "/home/auto_capture/auto_capture/new_capture/decom.json"
    local_package, remote_package = "../log/temp/1h.pac", "/home/auto_capture/auto_capture/new_capture/1h.pac"
    local_data_logpath, remote_data_logpath = "../log/temp/", "/home/auto_capture/auto_capture/test/"
    Capture.test_capture_run(config_path, local_capture_config, remote_capture_config, local_decom, remote_decom, local_package, remote_package, local_data_logpath, remote_data_logpath)


    # se = Config.get_conf_sections(config_path)
    # Multiprocess.sftp_put_file(config_path, se[1], local_capture_config, remote_capture_config)

    # # 运行压测capture
    # node, key = "case", "run_capture"
    # run_capture = "cd /home/auto_capture/auto_capture/;python3 run_capture.py;hostname"  # python3 run_capture.py
    # print("run_capture...")
    # Capture.test_capture(config_path, node, key, run_capture)
