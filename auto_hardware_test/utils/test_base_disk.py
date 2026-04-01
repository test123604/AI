#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from auto_hardware_test.utils.test_put_files import *
import time
import re

class BaseDisk:
    # 查找文件中指定内容
    def get_value(text, regex, key_word: str):
        if key_word in text:
            # 利用正则表达式提取所需字符串
            str = re.findall(regex, text) #re.findall输出['1122']#?控制只匹配0或1个,所以只会输出和最近的b之间的匹配情况
            # print("findall--------", str)
            result = re.sub(r'[\[\'\]]*', '', str.__str__())  # 前面是正则表达式，匹配多种字符（串）；去掉正则提取后的括号
        else:
            result = ''
            message = f"未在文件中发现{key_word}"
        return result

    # 将内容追加写入文件
    def fio_write(file, content):
        with open(file, 'a')as f:  # "a" - 追加 - 会追加到文件的末尾
            f.write(content)
        return file


    # 注意：运行shell脚本需要使用dos2unix fiotest.sh格式化一下
    # 100%随机，30%读，70%写 64K
    def fio_test(disk_name, log_name, fio_shell):
        # 计算磁盘占比20-40-60-80%容量大小，记住要除以线程数
        # size = []
        # for i in range(0, 11, 2):
        #     # if i != 0:
        #     i = ceil(i/10*744.6/24)
        #     if i == 32:
        #         i -= 1
        #     size.append(i)
        #     print("磁盘容量：" + i.__str__())

        baseData = " -thread -runtime=300 -group_reporting"  ## -runtime=300 -size=500G
        rw = ['read', 'write', 'randread', 'randwrite', 'randrw -rwmixread=70']  # 'read', 'write', 'randread', 'randwrite', 'randrw -rwmixread=70'
        ioengine = ['psync']
        bs = ['4k', '64k']  # '4k', '64k'
        numjobs = [1, 4, 8, 16, 32, 64, 128]  # 1, 4, 8, 16, 32, 64, 128
        iodepth = [1]
        direct = [1]
        line = 0
        fio_temp = []
        date = "date +\"%Y-%m-%d %H-%M-%S\""
        mkfs = "echo y | mkfs.ext4 "  # /dev/nvme0n1
        mount = "mount -t ext4 -o discard "  # /dev/nvme0n1 /mnt/
        fstrim = "fstrim -v /mnt/"
        fstrim_a = "fstrim -a -v"
        umount = "umount /mnt/"
        # dd = "dd if=/dev/zero bs=1G count=200 of="
        # rm = "rm -rf "
        # stop = "servermgr stop writeback"
        # start = "servermgr start writeback"
        # status = "servermgr status all"
        drop_cache = 'echo 3 > /proc/sys/vm/drop_caches'
        # 循环并剔除不符合的fio脚本，然后保存到列表
        for ioe in ioengine:
            for r in rw:
                for b in bs:
                    for job in numjobs:
                        for iod in iodepth:
                            for di in direct:
                                line += 1
                                fio_comm ="fio -filename=" + disk_name + baseData + ' -bs=' + b + ' -direct=' + di.__str__() + ' -rw=' + r + ' -ioengine=' + ioe + ' -numjobs=' + job.__str__() + ' -iodepth=' + iod.__str__() + ' -name=fiotest' + line.__str__() + ' >> /home/auto_capture_log/'+ log_name +'/fiotest' + line.__str__() + '.log'
                                fio_temp.append(fio_comm)

        # 遍历保存的fio脚本，并存入shell文件
        line = 0
        for f in fio_temp:
            # 测试用例case加1
            line += 1

            # 使用正则获取filename中磁盘测试文件名
            regex_fname = r"-filename=(.+?) -thread"
            diskname = BaseDisk.get_value(f, regex_fname, "-filename=")

            # 删除测试文件名 + rm + fname + '\r\n' + 'sleep 1\r\n'
            fio_str = '#---test' + line.__str__() + '-------------------------------\r\n' + date + '\r\n' + mkfs + diskname + '\r\n' + mount + diskname + ' /mnt/\r\n' + fstrim + '\r\n' + umount + '\r\n' +'sync\r\n' + drop_cache + '\r\n' + 'sleep 1\r\n' + 'free -h\r\n' + 'echo fio running...\r\n' + f + '\r\n' + 'sleep 1\r\n'
            # print(fio_str)
            sh_name = BaseDisk.fio_write(fio_shell, fio_str)
        return sh_name


    # 生成fio测试脚本
    def test_make_shell(disk_name, log_name, sh_name):
        disk_list = []
        sh_file = ''
        if disk_name != "":
            # disk_list = disk_name.__str__().split(",")
            # print(disk_list)
            sh_file = BaseDisk.fio_test(disk_name, log_name, sh_name)
        return sh_file

    # 找到节点对应ssh并执行命令
    def sftp_shell(config_path, section, cmd):
        start = time.time()
        ip = Config.read_config(config_path, section, "host")
        port = Config.read_config(config_path, section, "port")
        username = Config.read_config(config_path, section, "username")
        password = Config.read_config(config_path, section, "password")

        conn = SSHConnection(ip, port, username, password)
        conn.sftp_exec_shell(cmd)
        print(time.time() - start)

    # 判断是否安装基础环境，并执行多個磁盤測試
    def test_disk_base(config_path, node, key, remote_way):
        flag = int(Config.read_config(config_path, node, key))
        print(flag)
        if flag:
            # 一、生成fio测试脚本
            section = "case"
            disk_key_list = ["data_path", "disk_path", "writeback_path"]
            # 獲取磁盤路徑名並存入list
            disk_path_list = []
            for i in disk_key_list:
                disk_path = Config.read_config(config_path, section, i)
                disk_path_list.append(disk_path)
            print("disk_path_list:", disk_path_list)

            log_list = ["log_data", "log_disk", "log_writeback"]
            shFile_list = ["fiotest_data.sh", "fiotest_disk.sh", "fiotest_writeback.sh"]

            # 同步遍歷list中對應的磁盤名稱、日誌名稱、腳本名稱；生成三者對應的測試腳本；
            for disk_name, log_name, sh_name in zip(disk_path_list, log_list, shFile_list):
                BaseDisk.test_make_shell(disk_name, log_name, sh_name)
                print("disk_name, log_name, sh_name---", disk_name, log_name, sh_name)

            # 二、下發並執行腳本
            sections = Config.get_conf_sections(config_path)
            for shFile in shFile_list:
                # 下载脚本到被测试服务器，並將格式轉為Unix
                remote_path = remote_way + shFile.__str__()
                dos2unix = "dos2unix " + remote_path
                Multiprocess.sftp_put_file(config_path, sections[1], shFile, remote_path)
                BaseDisk.sftp_shell(config_path, sections[1], dos2unix)

                # 执行shell磁盘测试脚本
                print("fio test...")
                cmd = "sh " + remote_path
                BaseDisk.sftp_shell(config_path, sections[1], cmd)
        else:
            print("已跳过磁盤测试！")



if __name__ == '__main__':
    # node, key = "case", "test_disk"
    # remote_way = "/home/auto_capture_log/"
    # config_path = "../config.conf"
    # BaseDisk.test_disk_base(config_path, node, key, remote_way)

    disk_name, log_name, fio_shell = "/dev/sdc", "log_data", "fiotest_sdc.sh"

    BaseDisk.fio_test(disk_name, log_name, fio_shell)

    # 1,手动执行fio脚本，需要用dos2unix xx.sh
    # 2,运行后看一下fio.log内容是否正确；

