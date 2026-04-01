#!/usr/bin/env python3
# coding: utf-8
import paramiko, os, datetime, glob

class SSHConnection(object):
    def __init__(self, remote_ip, remote_port, ssh_username, ssh_password):
        self.remote_ip = remote_ip
        self.remote_ssh_port = remote_port
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password

    def sftp_connect_ssh(self):
        try:
            # 实例化SSHClient
            self.ssh = paramiko.SSHClient()
            # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接SSH服务端，以用户名和密码进行认证
            self.ssh.connect(hostname=self.remote_ip, port=self.remote_ssh_port, username=self.ssh_username,
                             password=self.ssh_password)
        except Exception as e:
            print(e)
        return self.ssh

    def sftp_close_ssh(self):
        try:
            self.ssh.close()
        except Exception as e:
            print(e)

    # 远程执行多条命令
    def sftp_exec_shell(self, shell):
        global line
        ssh = self.sftp_connect_ssh()
        print('exec shell start %s ' % datetime.datetime.now())
        try:
            # 打开一个Channel并执行命令
            stdin, stdout, stderr = ssh.exec_command(shell, get_pty=True)
            for line in stdout.readlines():
            #     # if "refused" in str(line, encoding="utf-8"):
                print(line)
            # 获取命令结果
            # result = stdout.read()
            return line
        except Exception as e:
            print(e)
        finally:
            # 关闭SSHClient
            self.sftp_close_ssh()
            # print('exec shell success %s ' % datetime.datetime.now())

    # 上传文件夹
    # 思路是来自既然paramiko支持单体文件上传，并支持新建目录，就递单体上传目录中的所有文件并克隆当地文件的目录格式
    def sftp_put_dir(self, local_dir, remote_dir):  # host, user, password,
        try:
            t = paramiko.Transport((self.remote_ip, int(self.remote_ssh_port)))
            t.connect(username=self.ssh_username, password=self.ssh_password)
            # client = Multiprocess(config_path, section)
            # t = client.connect()
            sftp = paramiko.SFTPClient.from_transport(t)
            print('upload file start %s ' % datetime.datetime.now())
            for root, dirs, files in os.walk(local_dir):
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    a = local_file.replace(local_dir, '').replace("\\", "")
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

    # 上传单个文件到服务器
    def sftp_put_file(self, local_file, remote_file):
        t = paramiko.Transport((self.remote_ip, int(self.remote_ssh_port)))
        # 连接SSH服务端，使用password
        t.connect(username=self.ssh_username, password=self.ssh_password)
        # 获取SFTP实例
        sftp = paramiko.SFTPClient.from_transport(t)
        print('upload file start %s ' % datetime.datetime.now())
        sftp.put(local_file, remote_file)
        print('upload file success %s ' % datetime.datetime.now())
        t.close()

    # 下载单个文件到本地
    def sftp_get_file(self, remotepath, localpath):
        t = paramiko.Transport((self.remote_ip, int(self.remote_ssh_port)))
        # 连接SSH服务端，使用password
        t.connect(username=self.ssh_username, password=self.ssh_password)
        # 获取SFTP实例
        sftp = paramiko.SFTPClient.from_transport(t)
        print('download file start %s ' % datetime.datetime.now())
        # remotefile = SSHConnection.search_file(remotepath, ".ini")
        sftp.get(remotepath, localpath)
        print('download file success %s ' % datetime.datetime.now())
        t.close()


    # 模糊查询指定路径下指定后缀文件，默认log
    @staticmethod
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


if __name__ == '__main__':
    remote_ip = '172.17.7.41'
    remote_port = 22
    ssh_username = 'root'
    ssh_password = 'abc#123'
    conn = SSHConnection(remote_ip=remote_ip, remote_port=remote_port, ssh_username=ssh_username, ssh_password=ssh_password)

    # 批量上传文件
    # local_dir, remote_dir = "D:\\test", "/home/test/"
    # res = conn.sftp_put_dir(local_dir, remote_dir)

    #下载文件
    # remote_dir = "/home/log/1.log"
    # local_dir = r"D:\python-auto-code\auto-capture\test\2.log"  #后面必须要有一个名字 可以是同样的名字 也可以重命名
    # conn.sftp_get_file(remote_dir, local_dir)

    # 远程执行ssh命令
    # shell = "lsblk"
    # result = conn.sftp_exec_shell(shell)
    # print(result)
    # conn.sftp_close_ssh()

    # cmd = "sh /home/test/test.sh"
    # stdin, stdout, stderr = conn.sftp_exec_shell(cmd)
    # for line in stdout.readlines():
    #     print(line)
    # conn.close_ssh()

