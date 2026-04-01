#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from auto_hardware_test.utils.test_base_install import *
from auto_hardware_test.utils.connectClient import *
from auto_hardware_test.utils.log_to_excel import *
import glob
import threading

class Put_Files:
    # 批量远程ssh节点，并执行命令
    def sftp_shell(config_path, sections, cmd):
        start = time.time()
        pool = Pool()
        for i in range(1, len(sections)):
            section = 'ssh' + str(i)
            res = pool.apply_async(Multiprocess.stfp_multiprocess_cmd, args=(config_path, section, cmd,)).get()  # .get()获取pool对象的值
            print("section---", section, " res---", res)
        pool.close()
        pool.join()
        print(time.time() - start)
        return res

    # 批量远程上传文件
    def remote_put_files(config_path, sections, local_dir, remote_dir):
        start = time.time()
        pool = Pool()
        for i in range(1, len(sections)):
            # remote_ip = Config.read_config(config_path, sections[i], "host")
            # remote_port = Config.read_config(config_path, sections[i], "port")
            # ssh_username = Config.read_config(config_path, sections[i], "username")
            # ssh_password = Config.read_config(config_path, sections[i], "password")
            # conn = SSHConnection(remote_ip=remote_ip, remote_port=int(remote_port), ssh_username=ssh_username,
            #                      ssh_password=ssh_password)
            # pool.apply_async(conn.sftp_put_dir, args=(local_dir, remote_dir,))

            pool.apply_async(Multiprocess.sftp_put_dir, args=(config_path, sections[i], local_dir, remote_dir,))
            print("section---", sections[i])
        pool.close()
        pool.join()
        print(time.time() - start)

    # 判断是否运行上传
    def test_upload_run(config_path, local_dir, remote_dir, unzip_cmd):
        # config_path = "config.conf"
        node, key = "case", "upload"
        flag = int(Config.read_config(config_path, node, key))
        print(flag)
        if flag:                                #Python程序语言指定任何非0和非空（null）值为true，0 或者 null为false，所以Python中的 1 代表 True，0代表False
            sections = Config.get_conf_sections(config_path)
            # local_dir, remote_dir = "D:\\test", "/home/test/"
            # local_dir, remote_dir = r"../files", "/home/test/"
            # 上传文件到各服务器
            Put_Files.remote_put_files(config_path, sections, local_dir, remote_dir)

            # 解压文件
            Install.sftp_shell(config_path, sections, unzip_cmd)
        else:
            print("已跳过上传文件！")

    # 解压上传的文件
    def test_unzip_run(config_path, cmd):
        # config_path = "config.conf"
        sections = Config.get_conf_sections(config_path)
        Install.sftp_shell(config_path, sections, cmd)

    # 批量远程获取文件
    def remote_get_file(config_path, section, cmd, local_dir):
        try:
            start = time.time()
            remote_path = Multiprocess.stfp_multiprocess_cmd(config_path, section, cmd).replace("\r\n", "")  # .get()获取pool对象的值;替换掉结尾的换行
            print("remote_path---", remote_path)
            filepath, filename = Log.formatFilePath(remote_path)  # 使用文件路径格式化，把路径和文件名拆分开
            local_path = local_dir + filename.__str__()
            Multiprocess.sftp_get_file(config_path, section, remote_path, local_path)
            print("section---", section, " remote_path---", remote_path, "local_path---", local_path)
            print(time.time() - start)
            return remote_path
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
#     Put_Files.test_upload_run(1)
#     # unzip -t检查zip文件是否损坏；-o覆盖原先的文件；
    config_path = "../config.conf"
#     cmd = "cd /home/test/;unzip -o auto_capture.zip"
#     Put_Files.test_unzip_run(config_path, cmd)

    # cmd = "cd /home/test/;unzip auto_capture.zip"
    # Put_Files.test_unzip(cmd)
    # Put_Files.search_file("D:\\test\\count_20201112_212928.log", ".log")
    # Put_Files.search_file("D:\\test\\count*.log", ".log")
    # Put_Files.search_file("D:\\test\\*count*.log", ".log")
    #
    # config_path = "config.conf"
    # sections = Config.get_conf_sections(config_path)
    # search_file = "/home/test/auto_capture/auto_capture/config.ini"
    # postfix = ".ini"
    # Put_Files.remote_get_files(config_path, sections, search_file, "D:\\test\\config.ini")、

    # 查询并批量下载文件
    sections = Config.get_conf_sections(config_path)
    cmd = "find /home/auto_capture_log/ -name *net.log | awk 'END {print}'" # find查找默认按修改时间正序排列，awk 'END {print}'获取排序的最后一个值
    local_dir = r"../log/"
    Put_Files.remote_get_file(config_path, sections[2], cmd, local_dir)





