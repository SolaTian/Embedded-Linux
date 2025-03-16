- [MySQL](#mysql)
  - [MySQL 的非交互模式](#mysql-的非交互模式)
  - [MySQL 的交互模式](#mysql-的交互模式)
  - [查看并进入数据库](#查看并进入数据库)
  - [查看表](#查看表)
  - [查询、插入、删除、更改语句](#查询插入删除更改语句)
# MySQL 

本篇在于介绍 Linux 系统下 MySQL 数据库命令的使用

## MySQL 的非交互模式

MySQL 支持非交互模式，可以批量处理 SQL 语句。如果只是临时执行一条 SQL 语句，普通命令模式更方便。

    mysql [options] [SQL]

有以下的参数：

- -u root 指定 MySQL 用户名（root）。
- -p 输入密码（如果没有密码，可以省略 -p）。
- -e 让 MySQL 直接执行 SQL 语句并返回结果。

        #执行单条 MySQL 命令
        mysql -u root -e "USE mydatabase; SELECT * FROM vehicleinfo LIMIT 5;"

        #执行 SQL 脚本，自动执行 myscript.sql 脚本中的语句
        mysql -u root -p -e "source /path/to/myscript.sql"

## MySQL 的交互模式

交互模式适用于手动调试或交互式查询。

只要在非交互模式的基础上，不执行 [SQL] 语句就可以进入到交互界面

**进入交互界面之后，也是同样不区分大小写，但是需要注意的是，每一句命令的最后需要加上`;`**

## 查看并进入数据库

输入 `mysql` 之后就进入了 mysql 的交互界面，如下：

    # mysql
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 19
    Server version: 5.7.41-log Source distribution

    Copyright (c) 2000, 2023, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Cannot read termcap database;
    using dumb terminal settings.
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>

进入 MySQL 的交互模式，可以查看到 MySQL 的版本，以及输入 `help` 或者 `\h`获取帮助，处于等待输入命令的状态。


首先需要查找有哪些数据库，使用命令 show databases;

    mysql>
    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | sda                |
    | sys                |
    +--------------------+
    5 rows in set (0.00 sec)

可以看到有 5 个数据库，可以使用`use database_name`来进行切换
 
    mysql> use sda
    Database changed

这样，数据库就被切换到了 `sda`


## 查看表

进入到对应的数据库之后，就可以查看该数据库有哪些表，使用命令`show tables;`

    mysql> show tables;
    +--------------------------+
    | Tables_in_sda            |
    +--------------------------+
    | accumulationdayinfo      |
    | accumulationmonthinfo    |
    | aidData                  |
    | checkPointData           |
    | cid                      |
    | faceData                 |
    | humanData                |
    | intervalLancgVehicleinfo |
    | intervalParkVehicleinfo  |
    | intervalvehicleinfo      |
    | picDiskBuf               |
    | printLog                 |
    | ship                     |
    | shipData                 |
    | statisticinfo            |
    | surveilanceinfo          |
    | tfsData                  |
    | vehicleOBUInfo           |
    | violationData            |
    | weather                  |
    +--------------------------+
    20 rows in set (0.00 sec)
    mysql>

查看到有 `sda` 数据库有 20 个表.

## 查询、插入、删除、更改语句

查看到表之后就可以使用查询、插入、删除、更改等语句，可以参考可以参考[Sqlite 交互模式下的查询、插入、删除、更新](Sqlite.md#交互模式下的查询、插入、删除、更新)