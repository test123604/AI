# JMeter 压测完整指南

> 版本：v1.0
> 更新日期：2026-04-01
> 适用人群：软件测试工程师、性能测试工程师

---

## 目录

- [一、JMeter 安装教程](#一jmeter-安装教程)
  - [1.1 Windows 安装](#11-windows-安装)
  - [1.2 Linux/Mac 安装](#12-linuxmac-安装)
  - [1.3 验证安装](#13-验证安装)
- [二、JMeter 插件安装教程](#二jmeter-插件安装教程)
  - [2.1 插件管理器安装](#21-插件管理器安装)
  - [2.2 常用插件推荐](#22-常用插件推荐)
  - [2.3 手动安装插件](#23-手动安装插件)
- [三、压测场景配置模板](#三压测场景配置模板)
  - [3.1 完整配置模板](#31-完整配置模板)
  - [3.2 配置示例](#32-配置示例)
  - [3.3 快速填写模板](#33-快速填写模板)
- [四、JMeter 目录结构](#四jmeter-目录结构)
- [五、常用命令](#五常用命令)
- [六、插件清单](#六插件清单)
- [七、常见问题](#七常见问题)

---

## 一、JMeter 安装教程

### 1.1 Windows 安装

```bash
# 1. 检查/安装 Java（JDK 11+）
java -version

# 2. 下载 JMeter
访问：https://jmeter.apache.org/download_jmeter.cgi
下载：apache-jmeter-5.6.3.zip

# 3. 解压到指定目录
解压到：C:\Program Files\apache-jmeter-5.6.3

# 4. 配置环境变量（可选）
系统变量 → 新建
变量名：JMETER_HOME
变量值：C:\Program Files\apache-jmeter-5.6.3

系统变量 → Path → 新建
%JMETER_HOME%\bin

# 5. 启动 JMeter
双击：C:\Program Files\apache-jmeter-5.6.3\bin\jmeter.bat

或命令行：
jmeter
```

### 1.2 Linux/Mac 安装

```bash
# 1. 检查/安装 Java
java -version
# 如未安装：
sudo apt install openjdk-11-jdk  # Ubuntu/Debian
sudo yum install java-11-openjdk # CentOS/RHEL
brew install openjdk@11          # macOS

# 2. 下载 JMeter
wget https://downloads.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz

# 3. 解压
tar -xzf apache-jmeter-5.6.3.tgz
sudo mv apache-jmeter-5.6.3 /opt/jmeter

# 4. 配置环境变量
echo 'export JMETER_HOME=/opt/jmeter' >> ~/.bashrc
echo 'export PATH=$PATH:$JMETER_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# 5. 启动 JMeter
jmeter
```

### 1.3 验证安装

```bash
# 查看版本
jmeter -v

# 应该输出：
# Apache JMeter 5.6.3
```

---

## 二、JMeter 插件安装教程

### 2.1 插件管理器安装

```
1. 下载插件管理器
   地址：https://jmeter-plugins.org/install/Install/

2. 下载文件：JMeterPlugins-Standard-1.4.zip

3. 解压后，将 JMeterPlugins-Standard.jar 复制到：
   Windows: C:\Program Files\apache-jmeter-5.6.3\lib\ext\
   Linux:   /opt/jmeter/lib/ext/

4. 重启 JMeter

5. 在菜单中验证：
   Options → Plugins Manager（出现则安装成功）
```

### 2.2 常用插件推荐

| 插件名称 | 用途 | 推荐指数 |
|---------|------|----------|
| **JPG Graphics (Synthetic Blends)** | 生成更漂亮的性能图表 | ⭐⭐⭐⭐⭐ |
| **PerfMon (Server Performance Monitor)** | 实时监控服务器资源 | ⭐⭐⭐⭐⭐ |
| **Custom Thread Groups** | 更灵活的并发控制 | ⭐⭐⭐⭐ |
| **JSON Support** | 增强 JSON 处理能力 | ⭐⭐⭐⭐ |
| **WebSocket Samplers** | WebSocket 协议压测 | ⭐⭐⭐ |

#### 通过插件管理器安装

```
1. JMeter GUI
   Options → Plugins Manager

2. 选择 "Available Plugins" 标签

3. 推荐安装的插件：
   ☑ JPG Graphics (Synthetic Blends)
   ☑ PerfMon (Server Performance Monitor)
   ☑ Custom Thread Groups
   ☑ JSON Support
   ☑ WebSocket Samplers

4. 点击 "Apply Changes and Restart JMeter"
```

### 2.3 手动安装插件

```bash
# 1. 下载插件 JAR 包
# 2. 复制到 jmeter/lib/ext/ 目录
# 3. 重启 JMeter
```

---

## 三、压测场景配置模板

### 3.1 完整配置模板

```
╔════════════════════════════════════════════════════════════════╗
║                   JMeter 压测场景配置模板                      ║
╚════════════════════════════════════════════════════════════════╝

【基本信息】
项目名称：______________________________
测试场景：______________________________
接口协议：HTTP / HTTPS

【接口信息】
接口名称：______________________________
请求方法：GET / POST / PUT / DELETE
接口地址：______________________________

【请求配置】
1. 请求头（Headers）：
   Content-Type: application/json
   Authorization: Bearer ${token}
   其他：______________________________

2. 请求参数：

   如果是 GET（Query 参数）：
   参数名1 = 参数值1
   参数名2 = ${参数化变量}

   如果是 POST（Body）：
   Content-Type: application/json
   Body内容：
   {
     "key1": "value1",
     "key2": "${变量名}",
     "key3": 123
   }

   或者 Content-Type: application/x-www-form-urlencoded
   key1=value1&key2=value2

【并发配置】
虚拟用户数（线程数）：_______
准备时长：_______秒
循环次数：_______
持续时间：_______

【断言配置】
预期响应码：200
预期响应内容包含：success
JSON Path 断言（可选）：$.code = 0

【参数化配置】（可选）
需要参数化的字段：____________________
CSV 文件名：__________________________
CSV 数据示例：
value1,value2,value3
test001,123456,normal
test002,123456,vip
test003,123456,admin

【关联提取】（可选）
需要从响应中提取的字段：______________
提取变量名：__________________________
提取表达式（JSON Path）：$.data.token
提取表达式（正则）："token":"(.*?)"

【思考时间】（可选）
固定思考时间：_______毫秒
随机思考时间：_______到_______毫秒

【监控配置】（可选）
是否监控服务器：是 / 否
被测服务器IP：_______________________
```

### 3.2 配置示例

#### 示例场景：电商登录接口压测

```
╔════════════════════════════════════════════════════════════════╗
║                   JMeter 压测场景配置示例                      ║
╚════════════════════════════════════════════════════════════════╝

【基本信息】
项目名称：电商平台性能测试
测试场景：用户登录高并发测试
接口协议：HTTPS

【接口信息】
接口名称：用户登录
请求方法：POST
接口地址：https://api.example.com/v1/user/login

【请求配置】
1. 请求头：
   Content-Type: application/json
   User-Agent: JMeter-Test

2. 请求Body（JSON）：
   {
     "username": "${username}",
     "password": "${password}",
     "captcha": "1234"
   }

【并发配置】
虚拟用户数：100
准备时长：10秒
循环次数：10

【断言配置】
预期响应码：200
预期响应内容包含：登录成功
JSON Path 断言：$.code = 0

【参数化配置】
需要参数化的字段：username, password
CSV 文件名：users.csv
CSV 数据：
username,password
user001,123456
user002,123456
user003,123456
...（共100条）

【关联提取】
需要提取登录后的 token
提取变量名：auth_token
提取表达式：$.data.token

【思考时间】
随机思考时间：1000到2000毫秒

【监控配置】
是否监控服务器：是
被测服务器IP：172.16.1.100
```

### 3.3 快速填写模板

```
【基本信息】
项目名称：
测试场景：
接口协议：HTTP / HTTPS

【接口信息】
接口名称：
请求方法：GET / POST / PUT / DELETE
接口地址：

【请求配置】
Content-Type：
请求头（Headers）：
请求Body/参数：

【并发配置】
虚拟用户数：
准备时长：
循环次数：

【断言配置】
预期响应码：
预期响应内容：

【参数化配置】
是否需要参数化：是 / 否
参数化字段：
CSV数据示例：

【关联提取】
是否需要提取响应数据：是 / 否
提取内容：
提取表达式（JSON Path或正则）：

【思考时间】
固定/随机思考时间：

【其他需求】
```

---

## 四、JMeter 目录结构

```
apache-jmeter-5.6.3/
├── bin/                    # 可执行文件和配置
│   ├── jmeter.bat         # Windows 启动脚本
│   ├── jmeter.sh          # Linux 启动脚本
│   ├── jmeter.properties  # JMeter 主配置
│   └── system.properties  # 系统配置
├── lib/
│   ├── ext/               # 插件 JAR 放这里
│   ├── junit/             # JUnit 相关
│   └── ...
├── printable_docs/        # 可打印文档
├── backups/               # 脚本备份
└── ...

# .jmx 脚本保存位置（自定义）
Windows: D:\JMeter_Scripts\
Linux:   ~/jmeter_scripts/
```

---

## 五、常用命令

```bash
# GUI 模式启动（调试用）
jmeter

# CLI 模式运行（正式压测）
jmeter -n -t test.jmx -l result.jtl -e -o report/

# 查看版本
jmeter -v

# 远程启动 Server
./jmeter-server -Djava.rmi.server.hostname=192.168.1.100

# 分布式压测
jmeter -n -t test.jmx -R 192.168.1.101,192.168.1.102
```

### 命令参数说明

| 参数 | 说明 |
|------|------|
| -n | 非 GUI 模式 |
| -t | 指定测试脚本文件 |
| -l | 指定结果日志文件 |
| -e | 测试结束后生成报告 |
| -o | 指定报告输出目录 |
| -R | 指定远程压测机 |

---

## 六、插件清单

### 6.1 推荐安装插件

| 插件 | 功能 | 安装方式 |
|------|------|----------|
| **Plugins Manager** | 插件管理器 | 手动安装 |
| **PerfMon** | 服务器监控 | Plugins Manager |
| **Custom Thread Groups** | 自定义线程组 | Plugins Manager |
| **JPG Graphics** | 增强图表 | Plugins Manager |
| **WebSocket** | WebSocket 协议 | Plugins Manager |

### 6.2 PerfMon 服务器监控配置

#### 被测服务器安装 ServerAgent

```bash
# 下载
wget https://github.com/undera/perfmon-agent/releases/download/2.2.3/ServerAgent-2.2.3.zip

# 解压
unzip ServerAgent-2.2.3.zip
cd ServerAgent-2.2.3

# 启动（Linux）
./startAgent.sh --udp-port 4444 --tcp-port 4444

# 启动（Windows）
startAgent.bat

# 验证启动
netstat -an | grep 4444
```

#### JMeter 配置

```
添加 → 监听器 → jp@gc - PerfMon Metrics Collector

配置：
Host: 被测服务器IP
Port: 4444
Metric to collect: CPU / Memory / Disk I/O / Network
```

---

## 七、常见问题

### Q1: JMeter 启动报错找不到 Java

```bash
# 解决方法：配置 JAVA_HOME 环境变量
Windows:
系统变量 → 新建
变量名：JAVA_HOME
变量值：C:\Program Files\Java\jdk-11

Linux:
echo 'export JAVA_HOME=/usr/lib/jvm/java-11' >> ~/.bashrc
source ~/.bashrc
```

### Q2: 插件安装后不显示

```
解决方法：
1. 确认 JAR 包放在 lib/ext/ 目录
2. 重启 JMeter
3. 检查 JMeter 版本与插件兼容性
```

### Q3: 压测时内存溢出

```bash
# 修改 jmeter.bat (Windows) 或 jmeter.sh (Linux)
HEAP="-Xms1g -Xmx4g -XX:MaxMetaspaceSize=256m"
```

### Q4: 分布式压测连接失败

```bash
# 检查防火墙
# 开放端口
sudo ufw allow 50000/tcp

# 检查 jmeter.properties 配置
server_port=50000
server.rmi.localport=50000
```

---

## 附录

### A. 下载地址

| 资源 | 地址 |
|------|------|
| JMeter 官网 | https://jmeter.apache.org/ |
| JMeter 下载 | https://jmeter.apache.org/download_jmeter.cgi |
| 插件管理器 | https://jmeter-plugins.org/ |
| PerfMon Agent | https://github.com/undera/perfmon-agent |

### B. 参考文档

- [JMeter 官方文档](https://jmeter.apache.org/usermanual/index.html)
- [JMeter Plugins Wiki](https://jmeter-plugins.org/wiki/)

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-04-01 | 初始版本 |

---

**文档结束**

> 如有问题或建议，请联系文档维护人员
