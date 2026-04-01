#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from auto_hardware_test.utils.log_to_excel import Config
from auto_hardware_test.utils.multiprocess import Multiprocess
import time
from multiprocessing import Pool

class Install:
    # 远程ssh节点，并执行命令
    def sftp_shell_one(config_path, section, cmd):
        start = time.time()
        pool = Pool()
        res = pool.apply_async(Multiprocess.stfp_multiprocess_cmd, args=(config_path, section, cmd,)).get()  # .get()获取pool对象的值
        print("section---", section, " res---", res)
        pool.close()
        pool.join()
        print(time.time() - start)
        return res

    # 远程ssh节点，并执行命令
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

    # 判断是否安装基础环境，并执行多线程ssh
    def test_install(config, node, key, cmd, section):
        flag = int(Config.read_config(config, node, key))
        print(flag)
        if flag:
            # sections = Config.get_conf_sections(config)
            # print("sections------------", sections)
            Install.sftp_shell_one(config, section, cmd)
        else:
            print("已经跳过安装基础环境！")


if __name__ == '__main__':
    config, node, key = "config.conf", "case", "test_net"
    cmd = "cd /home/auto_capture/auto_capture;hostname"
    Install.test_install(config, node, key, cmd)

