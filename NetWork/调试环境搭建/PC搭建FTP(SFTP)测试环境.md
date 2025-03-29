- [PC 端搭建 FTP(SFTP) 测试环境](#pc-端搭建-ftpsftp-测试环境)
  - [服务端环境搭建](#服务端环境搭建)
    - [PC 端搭建 FTP 服务端](#pc-端搭建-ftp-服务端)
    - [PC 端搭建 SFTP 服务端](#pc-端搭建-sftp-服务端)
  - [客户端环境搭建](#客户端环境搭建)
    - [使用 FileZilla 连接 FTP(SFTP)](#使用-filezilla-连接-ftpsftp)
    - [使用 WinSCP 连接 FTP(SFTP)](#使用-winscp-连接-ftpsftp)

# PC 端搭建 FTP(SFTP) 测试环境

在日常测试的过程中，常常会用到 FTP(SFTP) 这两种应用层协议，本篇介绍如何在电脑上搭建 FTP(SFTP) 服务端以及客户端。

这里仅介绍 Windows 系统下的第三方软件搭建环境（**除了下文提到的一些软件，还有很多其他的软件，没有列出的软件在使用的时候给 Google 一下即可**）。

关于 Linux 中搭建 FTP/SFTP 服务端与客户端可以参考[嵌入式设备中搭建FTP服务与客户端](嵌入式设备中搭建FTP服务与客户端.md)、[嵌入式设备中搭建SFTP服务与客户端](嵌入式设备中搭建SFTP服务与客户端.md)

## 服务端环境搭建

FTP 服务端软件准备工具：Filezilla  Server

下载链接（点击跳转）：[Filezilla](https://filezilla-project.org)

SFTP 服务端软件准备工具：

下载链接（点击跳转）：[freesshd(似乎很久没有更新)](https://freesshd.informer.com/download/)、[Bitvise SSH Server](https://bitvise.com/download-area)

选择对应系统的服务端软件即可。

### PC 端搭建 FTP 服务端

1. 打开 Filezilla  Server 软件，Host 默认为127.0.0.1，即默认将本机作为 FTP 服务器。

    ![](https://img-blog.csdn.net/20180107225457202)

2. 设置用户名和密码，以及共享文件夹，具体过程如下：

    ![设置用户名](https://img-blog.csdn.net/20180107225502539)
    ![设置密码](https://img-blog.csdn.net/20180107225503130)
    ![设置 FTP 根目录](https://img-blog.csdn.net/20180107225508592)
    ![设置 FTP 根目录](https://img-blog.csdn.net/20180107225510255)

    至此 FTP 服务器就搭建好了。
3. 登录 FTP 服务
    
    可以使用浏览器或者 FTP 登录工具 Filezilla Client登录到 FTP 

    ![chrome 登录 FTP](https://img-blog.csdn.net/20180107225511476)
    ![chrome 登录 FTP](https://img-blog.csdn.net/20180107225514773)

    也可以直接通过本地的文件浏览器直接访问 FTP 的根目录（无需密码）
4. 高级设置，上述为基本设置，还有一些高级设置

    ![General settings（常规设置）](https://img2018.cnblogs.com/blog/454642/201812/454642-20181214143404682-866001119.png)
    - Listen on Port：监听端口，其实就是FTP服务器的连接端口。（一般都是21）
    - Max.Number of users：允许最大并发连接客户端的数量。（0为不限制）
    - Number of Threads：处理线程。也就是CPU优先级别。数值调得越大优先级越高，一般默认即可
    ![IP Filter（IP过滤器）](https://img2018.cnblogs.com/blog/454642/201812/454642-20181214143452318-403133536.png)
    - 设置IP过滤规则，在上面栏目中的IP是被禁止与FTP服务器连接的，下面的是允许的

    

其余的一些高级设置可以参考：[FTP服务器FileZilla Server配置及使用方法
](https://www.cnblogs.com/pinpin/p/10119229.html)


### PC 端搭建 SFTP 服务端

1. 添加用户，并设置 SSH 服务器 ip，端口等信息

    ![](https://i-blog.csdnimg.cn/blog_migrate/f52182503aadc46ebb51391b9b179636.png)
    ![](https://i-blog.csdnimg.cn/blog_migrate/a532ef30b09731501059fa9d4dc8fa54.png)
2. 设置登录授权选项，其中 Public key auth 意指通过公钥登录

    ![](https://i-blog.csdnimg.cn/blog_migrate/6ec899c1c1c070ba96f0074f48dfe9fa.png)
3. 设置 sftp 服务器根目录

    ![](https://i-blog.csdnimg.cn/blog_migrate/daa9c49dd9a992f4cea23f20627d5a5f.png)
4. 启动服务器 Server Status，这里我们只用到 sftp，所以只启动 sftp

    ![](https://i-blog.csdnimg.cn/blog_migrate/6253c16579b41d76b9f7884c8d3fa34b.png)


## 客户端环境搭建

准备工具：FileZilla, WinSCP

下载链接(点击跳转)：

[FileZilla](https://filezilla-project.org/)

[WinSCP](https://winscp.net/eng/download.php)

这两个软件都同时支持连接 FTP 和 SFTP 服务端

### 使用 FileZilla 连接 FTP(SFTP)

1. 打开 FileZilla 软件，点击 "文件->站点管理器"，连接 FTP（端口21） 或者 SFTP（端口22且支持 SSH）
    ![连接FTP](https://img2018.cnblogs.com/blog/639765/201909/639765-20190903174220380-1150545823.png)
    ![连接SFTP](https://i-blog.csdnimg.cn/blog_migrate/9d6f2256fb32e05af210c03b6a80fd5f.png)
    - 连接到 SFTP 是可以通过密码方式或者密钥方式连接（无需输入密码）
2. 与服务端进行文件传输（只需要在本地和远程的窗口进行文件的拖拽即可）
    ![文件上传和下载](https://i-blog.csdnimg.cn/blog_migrate/63ee9625da59e7910b46c802ecfc667a.png)

### 使用 WinSCP 连接 FTP(SFTP)

使用 WinSCP 连接到 FTP 和 SFTP 的方式与 FileZilla 基本一致。
