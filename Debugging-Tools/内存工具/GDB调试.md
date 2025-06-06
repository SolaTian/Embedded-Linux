- [coredump](#coredump)
  - [使用 GDB 分析 coredump 文件](#使用-gdb-分析-coredump-文件)
  - [使用 addr2line 分析 coredump 文件](#使用-addr2line-分析-coredump-文件)
  - [app.nostrip 文件](#appnostrip-文件)
    - [app 和 app.nostrip 文件的区别和联系](#app-和-appnostrip-文件的区别和联系)


# coredump 

`coredump` 文件是进程崩溃时内存状态的快照，通过分析它可以找出进程崩溃的原因。


## 使用 GDB 分析 coredump 文件

`gdb` 是一个命令行调试工具。

`gdb` 可以调试正在运行的程序

    gdb -p <进程ID>

`gdb` 也可以调试 `coredump` 文件

    gdb <可执行文件> <coredump 文件名>

不管是哪种方式启用 `gdb`，都会进入 `gdb` 调试界面

    (gdb)

调试界面支持的命令包括：
- r/run: 开始执行程序
- b <行号>/break <行号>：在指定行号处设置断点
- b <函数名>/break <函数名>：在指定函数的入口处设置断点
- c/continue：在程序暂停时继续执行，直到下一个断点
- i b/info breakpoints: 查看所有已经设置的断点信息
- delete <断电编号>：删除指定编号的断点
- n/next: 单步执行下一行代码，如果遇到函数调用，会将函数调用当作一行代码执行，不会进入函数内部
- s/strp: 单步执行下一行代码，如果遇到函数调用，会进入函数内部继续调试
- p <变量名>/print <变量名>：打印指定变量的值
- bt/backtrace: 显示当前的函数调用栈
- l/list：显示当前执行位置附近的源代码
- list <行号>：显示指定行号附近的源代码。
- list <函数名>：显示指定函数的源代码。
- q: 退出 gdb

使用 `gdb` 调试 `coredump` 文件，输入 `bt` 查看程序崩溃时候的调用栈。使用 `l` 显示崩溃时候的源代码。

在一些嵌入式 Linux 中，`gdb` 这个工具可能会带有交叉编译工具链的前缀。如：`arm-hisv300-linux-gdb`


## 使用 addr2line 分析 coredump 文件

`addr2line` 是一个将程序地址转换成为文件名和行号的工具。

    addr2line [选项] [地址，地址...]

- -e <可执行文件>：指定要分析的可执行文件或者共享库
- -f：显示函数名，除了输出文件名和行号外，还会显示该地址对应的函数名
- -p：以更易读的方式输出结果
- -C：将低级别的符号名解码为用户级别的名称（即进行符号名的反修饰），对于 C++ 程序特别有用，因为 C++ 编译器会对函数名进行修饰
- -h：查看帮助，部分嵌入式 Linux 可能会阉割命令。

分析步骤

1. 从 `coredump` 中获取到崩溃地址：在 `gdb` 中使用 `bt` 命令查看调用栈，找到崩溃发生的地址，或者有时可以从串口等日志信息中直接获取到 `Undefined Signal 11` 这些段错误信号，会输出 `PC` 和 `LR` 的地址。
2. 使用 `addr2line` 转换崩溃地址，输出对应的源代码文件和行号。

        addr2line -e <可执行文件> <崩溃地址>

在一些嵌入式 Linux 中，`addr2line` 这个工具可能会带有交叉编译工具链的前缀。如：`arm-hisv300-linux-addr2line`

## app.nostrip 文件

在嵌入式设备中，一般升级固件都是由主进程、子进程、脚本、二进制文件等一系列的文件压缩而成的。通过`web`页面将该固件升级或者是通过其他的方式进行升级。

当设备的主进程发生内存泄露时，我们可以获取到内存地址`PC/LR`，为了获取到内存泄漏的具体原因，我们需要使用**含有符号表的未剥离文件**，如`app.nostrip`文件。


### app 和 app.nostrip 文件的区别和联系

> `app`: 通过 `strip` 命令移除了调试信息（体积更小），无法用于解析符号。
> `app.nostrip`: 保留完整符号表和调试信息，专门用于地址解析。


|文件类型|用途|是否包含调试信息|
|-|-|-|
|`app`|设备实际运行的二进制文件|否|
|`app.nostrip`|调试符号文件|是|


```bash
#使用 addr2line 工具解析
addr2line -e app.nostrip <PC> <LR>

#使用 gdb 分析 coredump
gdb app.nostrip core.dump  # 加载符号文件和 coredump
(gdb) bt  # 查看调用栈
```