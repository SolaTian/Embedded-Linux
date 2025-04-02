- [PostgreSQL](#postgresql)
  - [PostgreSQL 的非交互模式](#postgresql-的非交互模式)
  - [PostgreSQL 的交互模式](#postgresql-的交互模式)
    - [进入并查看数据库](#进入并查看数据库)
    - [查看表](#查看表)
    - [查询、插入、删除、更改语句](#查询插入删除更改语句)
    - [退出交互模式](#退出交互模式)
# PostgreSQL

## PostgreSQL 的非交互模式

    psql [OPTIONS] [SQL]

参数

- -U：指定要连接的 PostgreSQL 用户。
- -d：指定要连接的数据库名称。
- -c：后面跟上要执行的 SQL 命令，需要用引号括起来。

        #查询 public 模式下 users 表的所有记录
        psql -U postgres -d mydatabase -c "SELECT * FROM public.users;"

        #查看 new_table 的结构
        psql -U postgres -d mydatabase -c "\d new_table"

        #输出重定向。将 users 表的查询结果保存到 users_result.txt 文件中：
        psql -U postgres -d mydatabase -c "SELECT * FROM public.users;" > users_result.txt

## PostgreSQL 的交互模式

交互模式适用于手动调试或交互式查询。

只要在非交互模式的基础上，不执行 [SQL] 语句就可以进入到交互界面

**进入交互界面之后，也是同样不区分大小写，但是需要注意的是，每一句命令的最后需要加上`;`**


### 进入并查看数据库

执行命令 `sudo -u postgres psql` 即可进入交互模式

    [root@localhost ~]# sudo -u postgres psql
    could not change directory to "/root": Permission denied
    psql (13.3)
    Type "help" for help.

    postgres=#

可以查看到数据库的版本

首先需要查找有哪些数据库，使用命令 `\l`

    postgres=# \l
                                   List of databases
     Name     |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
    --------------+----------+----------+-------------+-------------+-----------------------
    data_store   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
    postgres     | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
    server_store | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
    template0    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                 |          |          |             |             | postgres=CTc/postgres
    template1    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                 |          |          |             |             | postgres=CTc/postgres
    (5 rows)

    postgres=#

使用命令 `\c database_name`切换到指定的数据库

    postgres=# \c server_store
    You are now connected to database "server_store" as user "postgres".
    server_store=#


### 查看表

使用命令 `\dt`查看数据库中的所有表

    server_store=# \dt
              List of relations
     Schema |      Name       | Type  |  Owner
    --------+-----------------+-------+----------
    public | accountcfg_v2   | table | postgres
    public | area_region     | table | postgres
    public | base_param_v30  | table | postgres
    public | basiconfig      | table | postgres
    public | cascade_service | table | postgres
    public | certificaty     | table | postgres
    public | cloud           | table | postgres
    public | cruiseschedule  | table | postgres
    public | custom          | table | postgres
    public | deviceinfo      | table | postgres
    public | exprule         | table | postgres
    public | ftp_host        | table | postgres
    public | gb28181_service | table | postgres
    public | gobalparam      | table | postgres
    public | hgr             | table | postgres
    public | ipconfig        | table | postgres
    public | lane_line       | table | postgres
    public | lltude          | table | postgres
    public | manualconfig    | table | postgres
    public | network         | table | postgres
    public | ntpserver       | table | postgres
    public | organization    | table | postgres
    public | pic_merge       | table | postgres
    ...
    (42 rows)

    server_store=#

使用命令 `\d table_name`可以查看表的结构

    server_store=# \d ipconfig
                        Table "public.ipconfig"
      Column       |       Type        | Collation | Nullable | Default
    -------------------+-------------------+-----------+----------+---------
    deviceid          | character varying |           | not null |
    ichannel          | integer           |           |          |
    ifactory          | integer           |           |          |
    addrtype          | integer           |           |          |
    inputchan         | integer           |           |          |
    imode             | integer           |           |          |
    iport             | integer           |           |          |
    itransmode        | integer           |           |          |
    iparentid         | integer           |           |          |
    straddr           | text              |           |          |
    strusername       | text              |           |          |
    strpwd            | text              |           |          |
    strurl            | text              |           |          |
    stripcname        | text              |           |          |
    strsipid          | text              |           |          |
    iptz              | integer           |           |          |
    ecamtype          | integer           |           |          |
    isselectinpolling | integer           |           |          |
    Indexes:
        "ipconfig_pkey" PRIMARY KEY, btree (deviceid)

    server_store=#

### 查询、插入、删除、更改语句

查看到表之后就可以使用查询、插入、删除、更改等语句，可以参考可以参考[Sqlite 交互模式下的查询、插入、删除、更新](Sqlite.md#交互模式下的查询、插入、删除、更新)

### 退出交互模式

输入 `quit`或者`exit`或者`\q`或者 Ctrl+D 退出交互模式

    server_store=# quit
    [root@localhost ~]#
