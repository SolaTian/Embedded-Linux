- [Linux 下执行 Sqlite3 步骤](#linux-下执行-sqlite3-步骤)
  - [查看 Sqlite3 是否安装以及版本](#查看-sqlite3-是否安装以及版本)
  - [sqlite3 的非交互模式](#sqlite3-的非交互模式)
  - [sqlite3 交互模式](#sqlite3-交互模式)
  - [常见交互命令](#常见交互命令)
  - [交互模式下的查询、插入、删除、更新](#交互模式下的查询插入删除更新)
    - [执行查询过滤命令](#执行查询过滤命令)
    - [执行插入命令](#执行插入命令)
    - [执行删除命令](#执行删除命令)
    - [执行修改命令](#执行修改命令)

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

## sqlite3 的非交互模式

非交互模式主要用于批量处理 SQL 语句。如果只是临时执行一条 SQL 语句，普通命令模式更方便。

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

sqlite3 的基本用法是

    sqlite3 [OPTIONS] FILENAME [SQL]

- FILENAME：SQLite 数据库文件名（如 test.db）。如果文件不存在，会自动创建新数据库。
- [SQL]：可选参数，直接执行一条 SQL 命令后退出（非交互模式）

来看非交互模式下的几个主要的参数

输出模式：
- -ascii：将结果以 ASCII 文本格式输出，列之间用 | 分隔，行之间用换行符分隔。
    
        sqlite3 -ascii test.db "SELECT * FROM users;"
- -csv：将结果输出为 CSV 格式（逗号分隔），适合导入 Excel 或数据分析工具
  
        sqlite3 -csv test.db "SELECT * FROM users;" > users.csv

- -column：以列对齐的表格形式显示结果（默认模式）

        sqlite3 -column test.db "SELECT * FROM users;"
- -line：每行显示一个字段，格式为 列名 = 值，适合少量数据的详细查看

        sqlite3 -line test.db "SELECT * FROM users WHERE id=1;"
- -list：以列表模式显示，列之间用默认分隔符（|）分隔。

        sqlite3 -list test.db "SELECT * FROM users;"
- -[no]header：显示或隐藏列标题（默认关闭）

        sqlite3 -header test.db "SELECT * FROM users;"

执行控制：
- -init FILENAME：从指定文件读取并执行初始化 SQL 命令（如配置参数或创建表）

        sqlite3 -init config.sql test.db

信息与调试：
- -version：显示 SQLite 版本信息。
- -stats：在每次查询后打印内存使用统计信息（调试性能时有用）

        sqlite3 -stats test.db "SELECT * FROM users;"

## sqlite3 交互模式

默认情况下，如果没有执行 [SQL] 语句，则会进入到交互模式，适用于手动调试或交互式查询。

在嵌入式设备中，数据往往都会先插入到内存数据库，过一段时间之后，固定将内存数据库中的数据刷到硬盘数据库中。 sqlite3 需要进入到对应硬盘的挂载目录下（即进入对应的硬盘数据库），之后才能操作硬盘数据库的表。

例如：

    sqlite3 /dev/sdx

/dev/sdx 表示硬盘对应的挂载文件名，可以是 sda，也可以是 sdb 等文件名。

出现例如下面的界面就表示进入 sqlite3 交互界面成功

    SQLite version 3.18.0 2017-03-28 18:48:43
    Enter ".help" for usage hints.
    sqlite>

在 sqlite3 的交互界面，数据库标准的查询语句等，默认都是支持大小写的，也就是 `SELECT` 和 `select`是同样可以的。

## 常见交互命令

这里介绍几个常见的交互命令参数

- .help                     ：查看当前sqlite3支持的命令
- .database                 ：列出所有附加的数据库及其文件路径
- .schema ?TABLE?           ：显示数据库的建表语句（支持通配符 TABLE 过滤）

        .schema         --显示所有的表结构
        .schema veh     --显示 veh 表的 CREATE 语句
- .tables ?TABLE?           ：查看所有数据库的表名（支持通配符 TABLE 过滤）

        .tables         --列出所有表
        .tables veh%    --列出以"veh"开头的所有表
- .indexes ?TABLE?          ：列出所有索引（支持通配符 TABLE 过滤）

        .indexes users  -- 列出 users 表的所有索引
- .dump ?TABLE?             ：将数据库内容导出为 SQL 脚本（支持通配符 TABLE 过滤）。

        .dump           -- 导出整个数据库
        .dump users     -- 导出 users 表（包括数据库的所有操作）
- .mode MODE                ：设置输出格式（MODE 支持多种模式）：
  - ascii：ASCII 分隔符格式（默认）。
  - csv：逗号分隔值（CSV）。
  - column：列对齐表格（需配合 .width 调整列宽）。
  - line：每行显示一个字段（列名 = 值）。
  - list：每个值使用 | 分开
  - html：HTML 表格。
  - insert：生成 SQL INSERT 语句（需指定表名）。

            .mode csv
            SELECT * FROM users;
- .headers on|off           ：显示或隐藏查询结果的列标题。

        .headers on
        SELECT * FROM users;

- .stats on|off             ：显示内存和 I/O 统计信息（性能分析）

        .stats on
        SELECT * FROM users;
- .once FILENAME            ：将下一条 SQL 查询的结果输出到文件（适用于单次导出）。

        .once output.csv
        SELECT * FROM users;
- .version                  ：显示 SQLite 版本信息
- .exit               #退出
- .quit               #退出

由于嵌入式系统资源有限，sqlite3 支持的交互命令也有限，可以先使用 .help 获取当前系统下支持的命令。一些其他的命令也可以在使用之前再了解一下用法

## 交互模式下的查询、插入、删除、更新<a id="交互模式下的查询、插入、删除、更新"></a>

**注意后面以分号进行结尾，如果不以分号结束，可能会出现无法正常输入命令的情况。**

### 执行查询过滤命令

由于是阉割版的 sqlite3，因此可能并不支持 sqlite 的所有关键字。

下面列出几条查询过滤命令

    #导出数据为csv
    .headers on
    .mode csv
    .once /tmp/users.csv
    select * from users;

    #仅查看数据
    .headers on
    .mode acsii / .mode list
    select * from users;

在一些数据库中，数据量比较大，且直接 `select`出来的目标是从最开始插入的数据开始显示的，有时需要查看最新的数据有无插入数据库。可以用下面的一些过滤命令。

    #查询 tablename 中最前面 5 条的数据
    select * from tablename limit 5; 

    #查询 tablename 中最前面 5 条的 coloum1 列信息，仅显示 coloum1
    select coloum1 from tablename limit 5;    

    #查询 tablename 中最后面 5 条信息（最新的 5 条信息）
    select * from tablename desc limit 5;     

    # 查询 tablename 中按照 coloum1 排序的最后 5 条信息（最新的 5 条信息）
    select * from tablename order by coloum1 desc limit 5; 

    #按照 coloum1 列进行过滤，字符串过滤用单引号。
    select * from tablename where coloum1 = 'xxxx';  



### 执行插入命令

向数据库中插入数据的命令如下：

    #标准向 tablename 中插入单行数据
    insert into tablename (column1, column2, ...) values (value1, value2, ...);

    #省略列名，所有列都要赋值，且顺序与表定义一致
    insert into tablename values (value1, value2, ...);

    #标准向 tablename 中插入多行数据
    insert into tablename (column1, column2, ...) values (value1, value2, ...);
    insert into tablename (column1, column2, ...) values (value10, value11, ...);

    #向 tablename 中插入单行数据并忽略冲突，若 id=1 已存在，忽略此插入
    insert or ignore into tablename (id, name) VALUES (1, 'Alice');

    #向 tablename 中插入单行数据并替换冲突，若 id=1 已存在，替换原有插入
    insert or replace into tablename (id, name) VALUES (1, 'Alice_New');



### 执行删除命令

删除操作的部分命令（删除命令慎用）：

    #删除表中的所有记录，慎用
    delete from tablename;

    #删除符合条件的记录
    delete from tablename where column > 30;

### 执行修改命令

修改表中的数据命令

    #修改表中符合条件的数据的 column1 和 column2
    update tablename set column1 = new_value, column2 = new_value2
    where condition;

