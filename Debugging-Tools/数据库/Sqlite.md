- [Linux 下执行 Sqlite3 步骤](#linux-下执行-sqlite3-步骤)
  - [查看 Sqlite3 是否安装以及版本](#查看-sqlite3-是否安装以及版本)
  - [sqlite3 本身支持的命令](#sqlite3-本身支持的命令)
  - [进入 sqlite3 操作界面](#进入-sqlite3-操作界面)
  - [常见交互命令](#常见交互命令)
  - [执行查询过滤命令](#执行查询过滤命令)

# Linux 下执行 Sqlite3 步骤

## 查看 Sqlite3 是否安装以及版本

首先需要在当前的嵌入式系统中确认，是否已经支持了 Sqlite3 

    sqlite3 -version

查看 Sqlite3 的版本，如果返回了版本信息，则表示已经安装，如果没有则需要进行安装。

例如

    sudo apt update
    sudo apt install sqlite3    

但是考虑到嵌入式系统的工具基本都是使用交叉编译工具链编译的，在一般的工程中，Sqlite3 工具基本都是编译好的，如果系统没有 Sqlite3 工具则使用挂载的方式将其导入到系统的 /bin 目录下，注意给它赋权限即可

    chmod -R 777 /bin/sqlite3

## sqlite3 本身支持的命令

输入 `sqlite3 -help` 查看 sqlite3 支持的命令有哪些

    #sqlite3 -help
    Usage: sqlite3 [OPTIONS] FILENAME [SQL]
    FILENAME is the name of an SQLite database. A new database is created
    if the file does not previously exist.
    OPTIONS include:
        -ascii               set output mode to 'ascii'
        -bail                stop after hitting an error
        -batch               force batch I/O
        -column              set output mode to 'column'
        -cmd COMMAND         run "COMMAND" before reading stdin
        -csv                 set output mode to 'csv'
        -echo                print commands before execution
        -init FILENAME       read/process named file
        -[no]header          turn headers on or off
        -help                show this message
        -html                set output mode to HTML
        -interactive         force interactive I/O
        -line                set output mode to 'line'
        -list                set output mode to 'list'
        -lookaside SIZE N    use N entries of SZ bytes for lookaside memory
        -mmap N              default mmap size set to N
        -newline SEP         set output row separator. Default: '\n'
        -nullvalue TEXT      set text string for NULL values. Default ''
        -pagecache SIZE N    use N slots of SZ bytes each for page cache memory
        -scratch SIZE N      use N slots of SZ bytes each for scratch memory
        -separator SEP       set output column separator. Default: '|'
        -stats               print memory stats before each finalize
        -version             show SQLite version
        -vfs NAME            use NAME as the default VFS

来看几个主要的参数

输出模式：





    sqlite3 -csv test.db "SELECT * FROM users;"

    sqlite3 -header -init init.sql test.db

## 进入 sqlite3 操作界面

sqlite3 确认已经安装后，需要到对应硬盘的挂载目录下。

    sqlite3 /dev/sdx

/dev/sdx 表示硬盘对应的挂载文件名，可以是 sda，也可以是 sdb 等文件名。

出现例如下面的界面就表示进入 sqlite3 成功

    SQLite version 3.18.0 2017-03-28 18:48:43
    Enter ".help" for usage hints.
    sqlite>

## 常见交互命令

这里介绍几个常见的交互命令

    .help               #查看当前sqlite3支持的命令
    .tables             #查看所有数据库的表
    .exit               #退出
    .quit               #退出

由于嵌入式系统资源有限，sqlite3 支持的交互命令也有限，可以先使用 .help 获取当前系统下支持的命令。

## 执行查询过滤命令

由于是阉割版的 Sqlite3，因此可能并不支持 Sqlite 的所有关键字。

下面列出几条查询过滤命令

    select * from tablename limit 5;         #查询 tablename 中最前面5条的数据
    select coloum1 from tablename limit 5;    #查询 tablename 中最前面5条的 coloum1 列信息
    select * from tablename desc limit 5;     #查询 tablename 中最后面5条信息
    select * from tablename order by coloum1 desc limit 5; #查询 tablename 中按照 coloum1 排序的最后5条信息
    select * from tablename where coloum1 = 'xxxx';  #按照 coloum1 列进行过滤，字符串过滤用单引号。

注意后面以分号进行结尾。