#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import configparser
from multiprocessing import Pool
import time
import datetime
import os
from auto_hardware_test.utils.log_to_excel import Config
import glob
import stat
import paramiko
import traceback

class Multiprocess:
    def __init__(self, file, node):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.config = configparser.ConfigParser()
        try:
            self.config.read(file, encoding='utf-8')
        except Exception as e:
            print(str(e))
        self.node = node

    def connect(self):
        try:
            self.client.connect(
                hostname=self.config.get(self.node, 'host'),
                port=self.config.getint(self.node, 'port'),
                username=self.config.get(self.node, 'username'),
                password=self.config.get(self.node, 'password'),
                timeout=self.config.getfloat(self.node, 'timeout')
            )
        except Exception as e:
            print(e)
            try:
                self.client.close()
            except:
                pass

    # ssh发送无需交互的单条命令
    def ssh_exec_onecommand(self, cmd):
        try:
            # 返回decode的指令stdout和stderr信息
            stdin, stdout, stderr = self.client.exec_command(cmd)
            return stdout.read().decode('utf8')
        except Exception as e:
            return 'ssh指令执行失败\t原因：%s\n' % e

    # ssh发送无需交互的多条命令
    def ssh_exec_command(self, cmd):
        client = paramiko.SSHClient()
        try:
            # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # client.connect(self.hostip, self.port, username=self.username, password=self.pwd, timeout=20)
            stdin, stdout, stderr = self.client.exec_command(cmd, get_pty=True)
            # logWriteToTxt(self.sitename + "执行"+cmd)
            res = ""
            results = stdout.readlines()
            for line in results:
                res += line
            try:
                err = stderr.readlines()
                for line in err:
                    res += line
                # print("res----", res)
            except:
                pass
                # results = stdout.readlines()
            # logWriteToTxt("在" + self.sitename + "执行"+cmd + res)
            return res
        except:
            pass
        finally:
            client.close()

    # 上传文件夹
    # 思路是来自既然paramiko支持单体文件上传，并支持新建目录，就递单体上传目录中的所有文件并克隆当地文件的目录格式
    def sftp_put_dir(config_path, section, local_dir, remote_dir):  # host, user, password,
        try:
            hostname = Config.read_config(config_path, section, "host")
            port = Config.read_config(config_path, section, "port")
            username = Config.read_config(config_path, section, "username")
            password = Config.read_config(config_path, section, "password")
            t = paramiko.Transport((hostname, int(port)))
            t.connect(username=username, password=password)
            # client = Multiprocess(config_path, section)
            # t = client.connect()
            sftp = paramiko.SFTPClient.from_transport(t)
            print('upload file start %s ' % datetime.datetime.now())
            for root, dirs, files in os.walk(local_dir):
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    a = local_file.replace(local_dir, '').replace("\\","")
                    remote_file = os.path.join(remote_dir, a)
                    try:
                        sftp.put(local_file, remote_file)
                    except Exception as e:
                        sftp.mkdir(os.path.split(remote_file)[0])
                        sftp.put(local_file, remote_file)
                    print("upload %s to remote %s" % (local_file, remote_file))
                for name in dirs:
                    local_path = os.path.join(root, name)
                    a = local_path.replace(local_dir, '')
                    remote_path = os.path.join(remote_dir, a)
                    try:
                        sftp.mkdir(remote_path)
                        print("mkdir path %s" % remote_path)
                    except Exception as e:
                        print(e)
            print('upload file success %s ' % datetime.datetime.now())
            t.close()
        except Exception as e:
            print(e)

    # 递归遍历远程服务器指定目录下的所有文件
    def _get_all_files_in_remote_dir(sftp, remote_dir):
        all_files = list()
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]
        files = sftp.listdir_attr(remote_dir)
        for file in files:
            filename = remote_dir + '/' + file.filename
            if stat.S_ISDIR(file.st_mode):  # 如果是文件夹的话递归处理
                all_files.extend(Multiprocess._get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        print("all_files---", all_files)
        return all_files

    def sftp_get_dir(config_path, section, remote_dir, local_dir):
        try:
            hostname = Config.read_config(config_path, section, "host")
            port = Config.read_config(config_path, section, "port")
            username = Config.read_config(config_path, section, "username")
            password = Config.read_config(config_path, section, "password")
            t = paramiko.Transport((hostname, int(port)))
            t.connect(username=username, password=password)
            # client = Multiprocess(config_path, section)
            # t = client.connect()
            sftp = paramiko.SFTPClient.from_transport(t)
            print(sftp)
            all_files = Multiprocess._get_all_files_in_remote_dir(sftp, remote_dir)
            for file in all_files:
                local_filename = file.replace(remote_dir, local_dir)
                local_filepath = os.path.dirname(local_filename)
                if not os.path.exists(local_filepath):
                    os.makedirs(local_filepath)
                sftp.get(file, local_filename)
        except:
            print('ssh get dir from master failed.')
            print(traceback.format_exc())

    # 模糊查询指定路径下指定后缀文件，默认log
    def search_file(files, file_format=".ini"):
        def _get_all_filepath(path_file, file_forma):
            # 默认获取log日志
            all_path = [os.path.join(x[0], y)
                for x in os.walk(path_file)
                    for y in x[2] if
                        os.path.splitext(y)[1]
                            == file_format]
            return all_path
        if not os.path.isdir(files):
            # 获取文件绝对路径，支持*.*模糊匹配
            actual_files = glob.glob(files)
        else:
            actual_files = _get_all_filepath(files, file_format)
        print(actual_files)
        return actual_files

    # 下载单个文件到本地
    def sftp_get_file(config_path, section, remotepath, localpath):
        try:
            hostname = Config.read_config(config_path, section, "host")
            port = Config.read_config(config_path, section, "port")
            username = Config.read_config(config_path, section, "username")
            password = Config.read_config(config_path, section, "password")
            t = paramiko.Transport((hostname, int(port)))
            # # 连接SSH服务端，使用password
            t.connect(username=username, password=password)
            # client = Multiprocess(config_path, section)
            # t = client.connect()
            # 获取SFTP实例
            sftp = paramiko.SFTPClient.from_transport(t)
            print('download file start %s ' % datetime.datetime.now())
            sftp.get(remotepath, localpath)
            print('download file success %s ' % datetime.datetime.now())
            t.close()
        except Exception as e:
            print(e)

    # 上传单个文件到远程
    def sftp_put_file(config_path, section, localpath, remotepath):
        try:
            hostname = Config.read_config(config_path, section, "host")
            port = Config.read_config(config_path, section, "port")
            username = Config.read_config(config_path, section, "username")
            password = Config.read_config(config_path, section, "password")
            t = paramiko.Transport((hostname, int(port)))
            # # 连接SSH服务端，使用password
            t.connect(username=username, password=password)
            # client = Multiprocess(config_path, section)
            # t = client.connect()
            # 获取SFTP实例
            sftp = paramiko.SFTPClient.from_transport(t)
            print('upload file start %s ' % datetime.datetime.now())
            sftp.put(localpath, remotepath)
            print('upload file success %s ' % datetime.datetime.now())
            t.close()
        except Exception as e:
            print(e)

    # 读取配置文件节点，并执行命令
    def stfp_put_files(config_path, section, local_dir, remote_dir):
        client = Multiprocess(config_path, section)
        client.connect()
        arr = client.sftp_put_dir(config_path, section, local_dir, remote_dir)
        print(arr, end='')

    # 读取配置文件节点，并执行命令
    def stfp_multiprocess_cmd(config_path, section, cmd):
        client = Multiprocess(config_path, section)
        client.connect()
        arr = client.ssh_exec_command(cmd)
        print(arr, end='')
        return arr

    # 通过配置文件参数key，获取value
    def get_config_value(config_path, section, key):
        # 创建配置对象
        config = configparser.ConfigParser()
        # 读取ini文件
        config.read(config_path, encoding='utf-8')  # python3,若有中文，需要使用utf-8
        value = config.get(section, key)
        # print(value)
        return value

    # 压测工具capture做包
    def make_package(config_path, task_num):
        start = time.time()
        task_num += 1
        pool = Pool()
        for i in range(1, task_num):
            node = 'ssh' + str(i)
            cmd = 'cd /home/auto_capture/auto_capture/;python3 make_package.py'
            pool.apply_async(Multiprocess.get_section_run, args=(config_path, node, cmd,))
        pool.close()
        pool.join()
        print(time.time() - start)

    # 压测工具capture做回写包
    def make_package_writeback(config_path, task_num):
        start = time.time()
        task_num = task_num + 1
        pool = Pool()
        for i in range(1, task_num):
            node = 'ssh' + str(i)
            cmd = 'cd /home/auto_capture/auto_capture/;python3 make_package_writeback.py'
            pool.apply_async(Multiprocess.get_section_run, args=(config_path, node, cmd,))
        pool.close()
        pool.join()
        print(time.time() - start)

    # 压测工具capture运行
    def run_capture(config_path, task_num):
        start = time.time()
        task_num = task_num + 1
        pool = Pool()
        for i in range(1, task_num):
            node = 'ssh' + str(i)
            cmd = 'cd /home/auto_capture/auto_capture/;python3 run_capture.py'
            pool.apply_async(Multiprocess.get_section_run, args=(config_path, node, cmd,))
        pool.close()
        pool.join()
        print(time.time() - start)

if __name__ == '__main__':
    # single process time;
    # start = time.time()
    # process('ssh1')
    # process('ssh2')
    # process('ssh3')
    # print(time.time() - start)

    # multi process time;
    # Multiprocess.make_package(1)
    config_path = "../config.conf"
    section = Config.get_conf_sections(config_path)[2]
    print(section)
    # localpath, remotepath = "D:\\test\\", "/home/test/"
    # # localpath, remotepath = "D:\\Program Files\\Works\Coding\\auto_hardware_test\\auto_hardware_test\\files", "/home/test/"
    # Multiprocess.sftp_get_dir(config_path, section, remotepath, localpath)

    cmd = "find /home/auto_capture_log/ -name *net.log"
    Multiprocess.stfp_multiprocess_cmd(config_path, section, cmd)