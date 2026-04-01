#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from auto_hardware_test.utils.multiprocess import Multiprocess
from auto_hardware_test.utils.log_to_excel import *


class Hardware:
    # 获取cpu型号
    def get_cpu(config_path):
        # 查看逻辑CPU的个数和 CPU信息（型号）
        cpu_cmd = "cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c"
        cpu_model_list = []
        sections = Config.get_conf_sections(config_path)
        for i in range(1, len(sections)):
            section = sections[i]
            cpu_model = Multiprocess.stfp_multiprocess_cmd(config_path, section, cpu_cmd).replace("\r\n", "").replace("     ", "")
            cpu_model_list.append(cpu_model)
        print("cpu_model_lisk:", cpu_model_list)
        return cpu_model_list

    # 获取CPU颗数
    def get_cpu_num(config_path):
        # 查看物理CPU个数
        cpu_core_cmd = "cat /proc/cpuinfo| grep 'physical id'| sort| uniq| wc -l"
        cpu_physical_core = []
        sections = Config.get_conf_sections(config_path)
        for i in range(1, len(sections)):
            section = sections[i]
            cpu_core = Multiprocess.stfp_multiprocess_cmd(config_path, section, cpu_core_cmd).replace("\r\n", "")
            cpu_physical_core.append(cpu_core)
        print("cpu_physical_core:", cpu_physical_core)
        return cpu_physical_core

    # 获取总内存大小列表
    def get_mem_total(config_path):
        # 查看内存total
        Mem_cmd = "free -h | grep Mem|cut -d\":\" -f2|sed 's/\s\+/,/g'|cut -d\",\" -f2"  # 其中\s代表空格，+代表出现一次或多次。
        Mem_total_list = []
        sections = Config.get_conf_sections(config_path)
        for i in range(1, len(sections)):
            section = sections[i]
            Mem = Multiprocess.stfp_multiprocess_cmd(config_path, section, Mem_cmd).replace("\r\n", "")
            Mem_total_list.append(Mem)
        print("Mem_total_list:", Mem_total_list)
        return Mem_total_list

    # 获取网卡列表
    def get_net_list(config_path):
        # 网卡
        net_cmd = "lspci | grep Ethernet | awk 'END {print}' | awk -F 'controller: ' '{print $2}'"  # awk -F使用指定字符串作为分隔符
        net_list = []
        sections = Config.get_conf_sections(config_path)
        for i in range(1, len(sections)):
            section = sections[i]
            net = Multiprocess.stfp_multiprocess_cmd(config_path, section, net_cmd).replace("\r\n", "")
            net_list.append(net)
        print("net_list:", net_list)
        return net_list

    # linux查看版本当前操作系统发行信息
    def get_OS_list(config_path):
        # linux系统版本
        OS_cmd = "cat /etc/centos-release"  # awk -F使用指定字符串作为分隔符
        OS_list = []
        sections = Config.get_conf_sections(config_path)
        for i in range(1, len(sections)):
            section = sections[i]
            OS = Multiprocess.stfp_multiprocess_cmd(config_path, section, OS_cmd).replace("\r\n", "")
            OS_list.append(OS)
        print("OS_list:", OS_list)
        return OS_list

    # linux查看版本当前操作系统内核版本
    def get_kernel_list(config_path):
        # 网卡
        kernel_cmd = "uname -r"  # awk -F使用指定字符串作为分隔符
        kernel_list = []
        sections = Config.get_conf_sections(config_path)
        for i in range(1, len(sections)):
            section = sections[i]
            net = Multiprocess.stfp_multiprocess_cmd(config_path, section, kernel_cmd).replace("\r\n", "")
            kernel_list.append(net)
        print("kernel_list:", kernel_list)
        return kernel_list


if __name__ == '__main__':
    config_path = "../config.conf"
    '''
    Hardware.get_cpu(config_path)
    Hardware.get_cpu_num(config_path)
    Hardware.get_mem_total(config_path)
    Hardware.get_net_list(config_path)
    '''
    Hardware.get_OS_list(config_path)
    Hardware.get_kernel_list(config_path)