- [网络状况排查](#网络状况排查)
  - [ping](#ping)
    - [ping 小包](#ping-小包)
    - [ping 大包](#ping-大包)
  - [telnet](#telnet)
- [网络基本配置](#网络基本配置)
  - [ifconfig](#ifconfig)
- [网络抓包](#网络抓包)
  - [tcpdump](#tcpdump)
- [网络状态](#网络状态)
  - [netstat](#netstat)
  - [traceroute](#traceroute)
- [路由](#路由)
  - [route](#route)
- [网络带宽测试](#网络带宽测试)
  - [iperf](#iperf)
- [应用层测试](#应用层测试)
  - [curl](#curl)

# 网络状况排查

## ping

ping 命令主要用于测试网络连通性，通过发送 ICMP 回声请求包来确定目标主机是否可达。

### ping 小包

    ping <目标 IP 或 域名> -c 次数

-c 可选，不加就会一直 ping ,按下 Ctrl + C 结束命令，可以查看丢包率， 通过这个命令可以判断网络是否可达

### ping 大包

    ping -s <包大小> <目标 IP 或 域名> -c 次数


不加 -s ，就会 ping 默认大小的数据包， 一般默认为 64 bytes

有时虽然目标 IP 可达，但是网络状况不好，存在丢包，就可能会存在数据丢失情况。


## telnet

测试端口连通性

    telnet <目标 IP 或 域名> <端口号>

若端口开放，则建立连接，否则会提示建立连接失败。

telnet 也可以用于远程登录（默认端口23），当远程服务器开启了 telnet 服务，可以使用

    telnet <目标 IP 或 域名>

来远程登录，但是由于安全问题，一般使用 SSH 登录（默认端口22）

# 网络基本配置

## ifconfig

> `ifconfig` 功能：查看或配置网络接口参数（IP地址、子网掩码、启用/禁用接口等）

包括以下用法

```bash
#查看所有网络接口信息
$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    inet 192.168.1.10  netmask 255.255.255.0  broadcast 192.168.1.255
    ether 00:11:22:33:44:55  txqueuelen 1000  (Ethernet)
    RX packets 1000  bytes 100000 (100.0 KB)
    TX packets 800  bytes 80000 (80.0 KB)


#查看指定接口信息
ifconfig <网卡名称>


#启用和禁用网络接口
ifconfig <网卡名称> up
ifconfig <网卡名称> down

#临时配置网络接口的IP地址和子网掩码
ifconfig <网卡名称> <IP地址> netmask 255.255.255.0

#启用和禁用ARP
ifconfig <网卡名称> arp 
ifconfig <网卡名称> -arp    
```

有时网卡信息较多，可以使用

    ifconfig | grep "inet"

来查看所有的 `IPv4` 地址


# 网络抓包

## tcpdump

除了 `WireShark` 这一图形化界面抓包软件，在嵌入式 Linux 中，经常会使用 `tcpdump` 工具进行抓包。命令如下

    tcpdump -i <网卡> -C <文件大小，MB> -W <最多保存文件数量> -w <抓包保存路径及文件名> -v host <主机IP> [and port <端口号>] 

-v 表示数据包输出比默认模式更多的数据包信息，如协议类型，时间戳等。一般情况下，不需要限制抓包的大小，-C 和 -W　可以缺省。

抓出来的包再使用 WireShark 进行分析

# 网络状态

## netstat

`netstat` 用于展示系统当前的网络连接状态，包括 Internet 连接和 UNIX 域套接字连接

```bash
$ netstat
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0     64 10.11.97.166:22         10.11.97.122:61588      ESTABLISHED
tcp        0      0 10.11.97.166:50620      10.11.97.24:5000        TIME_WAIT

Proto RefCnt Flags       Type       State         I-Node Path
unix  2      [ ]         DGRAM                      6149 @/org/kernel/udev/udevd
```

- Recv-Q：接收队列，指的是在本地接收缓冲区中等待应用程序读取的数据字节数
- Send-Q：发送队列，代表本地发送缓冲区中还未被对方确认的数据字节数
- Local Address：本地地址和端口号
- Foreign Address：远程地址和端口号
- State：连接状态
- RefCnt：引用计数，指的是有多少个进程正在使用这个套接字。例如 2 表示有 2 个进程正在使用该套接字。
- Flags：套接字的标志，这里 [ ] 表示没有特殊标志。
- Type：套接字的类型，DGRAM 表示数据报套接字，通常用于无连接的通信；STREAM 表示流式套接字，用于面向连接的可靠通信。
- State：套接字的状态，对于 DGRAM 类型通常为空，CONNECTED 表示流式套接字已经建立连接。
- Path：套接字文件的路径。对于一些抽象的套接字，路径以 @ 开头；对于普通的文件套接字，显示其在文件系统中的实际路径


    netstat [选项]

- -a：显示所有活动的网络连接
- -p：显示每隔网络连接对应的进程ID和程序名称
- -l：显示监听中的套接字
- -t: 显示TCP连接
- -n：显示UDP连接

还有些其他的选项，可以使用  `netstat -h` 来获取

示例： 

    netstat -tp

会列出系统中所有 TCP 协议的网络连接，并且同时显示每个连接对应的进程 ID 和进程名称


## traceroute 

`traceroute` 用于跟踪网络数据包从源主机到目标主机所经过的路由路径。

    traceroute [选项] 目标主机

- -m：设置最大跳数，如果无法达到目标主机，traceroute 就会停止输出相应信息，若不指定，则按照默认最大跳数。
- -n: 直接显示IP地址，而不进行反向 DNS 查找将 IP 地址解析成域名，加快显示速度

    ```bash
    $ traceroute www.example.com
    traceroute to www.example.com (93.184.216.34), 30 hops max, 60 byte packets
    1  router1.example.net (192.168.1.1)  1.234 ms  1.567 ms  1.890 ms
    2  router2.example.net (10.0.0.1)  2.345 ms  2.678 ms  2.901 ms
    3  123.45.67.89  3.456 ms  3.789 ms  4.012 ms
    ...
    30  * * *    
    ```            

表示一个跳的信息，包括路由器的域名（如果可以解析）、IP 地址和三次尝试的往返时间（RTT，Round-Trip Time）
符号 * 表示该跳没有收到响应，可能是路由器设置了不响应 ICMP 消息，或者存在网络故障。

# 路由

## route

> `route`命令用于查看或操作内核的`IP`路由表（添加、删除、修改路由规则） 


基本用法

```bash
# 查看路由表，-n以数字形式显示IP和端口（不解析主机名和服务名），加快输出速度
route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0

# 添加默认网关
route add default gw 192.168.1.1 eth0

# 添加特定目标网络的路由
route add -net 10.0.0.0/24 gw 192.168.1.2 eth0

# 添加主机路由（单个IP）
route add -host 203.0.113.5 gw 192.168.1.3 eth0

# 删除默认网关
route del default gw 192.168.1.1 eth0

# 删除特定网络路由
route del -net 10.0.0.0/24

# 删除主机路由
route del -host 203.0.113.5

```

一些常用场景：

```bash
# 检查默认网关
route -n | grep '^0.0.0.0'  # 查找默认网关行

# 临时添加静态路由
# 访问 172.16.0.0/24 网段需通过网关 192.168.1.100
route add -net 172.16.0.0 netmask 255.255.255.0 gw 192.168.1.100 eth0

```

`ifconfig`和`route`设置的`IP`地址、网关、路由等，都会在重启之后失效。长久生效需要结合 Linux 操作系统发行版，修改网络配置文件。比如`Debian/Ubuntu`：编辑 `/etc/network/interfaces`


# 网络带宽测试

## iperf

iperf 是一个网络性能测试工具，当网络带宽等限制时，有可能会出现数据拥堵等问题，这时就可以用 iperf 工具测试网络带宽，同时也可以测试丢包率、延迟等性能指标。


测试网络带宽时，需要在服务器和客户端同时启用。

测试步骤如下：

1. 服务端操作：

        iperf -s 

2. 客户端操作：

        iperf -c <服务器 IP 地址> 

还有一些可选项

服务器选项：

- -s: 以服务器模式启动，服务器会监听指定端口（默认5001），等待客户端连接并接收数据
- -p：指定服务器监听的端口号
- -u：以 UDP 模式运行服务器。默认情况，iperf 使用 TCP 协议

客户端选项：

- -c：以客户端模式启动 iperf
- -p：指定客户端要连接到服务器的端口号，需与服务器监听的端口一致
- -u：以 UDP 模式运行客户端，与服务器的 UDP 模式对应
- -b：指定客户端发送数据的带宽，单位可以是 K（千比特）、M（兆比特）、G（吉比特）等。例如 -b 10M 表示以 10Mbps 的带宽发送数据，常用于 UDP 测试模拟不同带宽的流量。

测试参数选项：

- -t：指定测试的持续时间，单位为 s。
- -n：指定要传输的数据量，单位可以为 K、M、G 等。例如 -n 1G 表示传输 1GB 的数据，测试会在传输完指定数据量后停止。
- -i：指定统计信息的输出间隔，单位为 s。
- -w：设置套接字缓冲区的大小，合适的缓冲区大小可以提高传输效率，设置过大可能会占用过多的系统内存资源。单位可能是字节或者千字节
- -d：以双工模式运行，服务器不仅接收客户端数据，还会向客户端发送数据，同时测试网络两个方向的性能。


测试效果示例分析

服务端：

    #iperf -s -w 320k -i 1 -d
    ------------------------------------------------------------
    Server listening on TCP port 5001
    TCP window size: 320 KByte (WARNING: requested 320 KByte)
    ------------------------------------------------------------

    [  4] local 192.168.1.100 port 5001 connected with 192.168.1.101 port 49152
    [ ID] Interval       Transfer     Bandwidth
    [  4]  0.0-1.0 sec  110 MBytes   973 Mbits/sec

在 0s - 1s 的时间段内，传输的数据总量是 110M 字节，带宽为 973 Mbit/s, 根据网口的带宽限制，就可以知道是否当前状况下，上行带宽是怎样的。

客户端：

    #iperf -c 192.168.1.100 -w 320k -i 1
    ------------------------------------------------------------
    Client connecting to 192.168.1.100, TCP port 5001
    TCP window size: 320 KByte (WARNING: requested 320 KByte)
    ------------------------------------------------------------
    [  3] local 192.168.1.101 port 49152 connected with 192.168.1.100 port 5001
    [ ID] Interval       Transfer     Bandwidth
    [  3]  0.0- 1.0 sec  110 MBytes   922 Mbits/sec
    [  3]  1.0- 2.0 sec  112 MBytes   940 Mbits/sec

在 0 - 1 sec 表示从测试开始后的 0 秒到 1 秒这 1 秒钟的时间段，传输了 110 兆字节（MB）的数据，带宽为 922 兆比特每秒（Mbits/sec）。

通过这些指标对比客户端和服务端之间的网络传输性能

1. 服务端带宽波动较大或者数值较低，客户端带宽较稳定，服务端数据接收时存在网络拥堵情况。
2. 客户端带宽波动较大或者数值较低，服务端带宽较稳定，服务端数据接收时存在网络拥堵情况。


# 应用层测试

## curl

curl 用于在网络上传输数据，支持 HTTP，HTTPS，FTP 等，能够发送 HTTP 请求并获取响应，常用于测试和数据获取等场景。

    curl [选项] [URL]

- -X: 指定请求方法（GET、POST、PUT等），若不指定默认使用的 GET 方法
- -d 或 --data: 发送 POST 数据
- -H 或 --header：添加请求头
- -o 或 --output：将响应内容保存到文件
- -v 或 --verbose：显示详细的请求和响应信息
- -L 或 --location：自动跟踪重定向
- -s 或 --silent：让 curl 以静默模式输出，不显示进度条，错误信息和其他不必要的数据


下面给出几个示例并解释

    #从指定的 URL 下载 file.txt 文件，并将文件内容输出到终端
    curl https://example.com/file.txt 
    
    #从指定的 URL 下载 file.txt 文件，并将文件内容保存到本地
    curl https://example.com/file.txt > /tmp/local_file.txt

    #显示详细的请求和响应信息，包括请求头、响应头和状态码等，方便调试
    curl -v https://example.com

    #POST 请求
    curl -X POST https://example.com/api
    #PUT 请求
    curl -X PUT https://example.com/api/resource
    #DELETE 请求
    curl -X DELETE https://example.com/api/resource







