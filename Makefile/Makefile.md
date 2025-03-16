# makefile


## makefile 简介

首先介绍什么是 makefile ？

在一个工程中的源文件不计其数，且按照功能和模块放在若干个目录中，makefile 定义了一系列规则来指定：哪些文件需要先编译，哪些文件需要后编译，甚至一些更加复杂的功能操作。


makefile 带来的好处就是——“自动化编译”，一旦写好，只需要一个 make 命令，整个工程完全自动编译，极大的提高了软件开发的效率。 


### 程序的编译和链接

代码源文件首先会生成中间目标文件，再由中间目标文件生成可执行文件。在编译时，编译器只检测程序语法和函数、变量是否被声明。如果函数未被声明，编译器会给出一个警告，但可以生成Object File。而在链接程序时，链接器会在所有的Object File中找寻函数的实现，如果找不到，那到就会报链接错误码（Linker Error）


## makefile 介绍

下面以一个示例来介绍 Makefile

假设这个工程有 8 个 c 文件和 3 个头文件，且需要实现的规则是：

1. 如果这个工程没有编译过，所有的 c 文件都需要被编译并被链接
2. 如果这个工程的某几个 c 文件被修改，那么只编译被修改的 c 文件，并链接目标程序
3. 如果这个工程的头文件被改变了，那么我们需要编译引用了这几个头文件的c文件，并链接目标程序。

### makefile 的规则

makefile 的最核心的规则如下

    target... : prerequisites...
        recipe 
        ...
        ...

- target: 可以是一个目标文件，也可以是一个可执行文件，还可以是一个标签，标签在后续的伪目标章节中介绍。
- prerequisites：生成该 target 所依赖的文件和/或 target。
- recipe：该 target 要执行的命令（任意的 shell 命令）。


也就是说，target 这一个或多个的目标文件依赖于 prerequisites 中的文件，其生成规则定义在 recipe 中。

换句话说

**prerequisites 中如果有一个以上的文件比 target 文件要新的话，recipe所定义的命令就会被执行。**


### 一则示例

下面给出一则示例，并结合上面介绍的规则来分析一下：

    edit : main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o
    cc -o edit main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o

    main.o : main.c defs.h
        cc -c main.c
    kbd.o : kbd.c defs.h command.h
        cc -c kbd.c
    command.o : command.c defs.h command.h
        cc -c command.c
    display.o : display.c defs.h buffer.h
        cc -c display.c
    insert.o : insert.c defs.h buffer.h
        cc -c insert.c
    search.o : search.c defs.h buffer.h
        cc -c search.c
    files.o : files.c defs.h buffer.h command.h
        cc -c files.c
    utils.o : utils.c defs.h
        cc -c utils.c
    clean :
        rm edit main.o kbd.o command.o display.o \
            insert.o search.o files.o utils.o

- 目标文件(target)包括：
  - 可执行文件 edit
  - 目标文件 (*.o)：
- 依赖文件(prerequisites)：冒号后面的那些 .c 和 .h 文件
- recipe 行定义了如何生成目标文件的操作系统命令，一定要以一个 Tab 键作为开头。
- 反斜杠(\\): 换行符，便于阅读

上面的 makefile，每个 .o 文件都有一组依赖文件，.o 文件又是 edit 的依赖文件。依赖关系的实质就是说明了目标文件是由哪些文件生成的，换言之，目标文件是哪些文件更新的。

make 会比较 targets 文件和 prerequisites 文件的修改日期，如果 prerequisites 文件的日期要比 targets 文件的日期要新，或者target不存在的话，那么，make 就会执行后续定义的命令。


还有个点需要注意的就是 clean，clean 不是一个文件，它只不过是一个动作名字，有点像 C 语言中的 label 一样，其冒号后什么也没有，那么，make 就不会自动去找它的依赖性，也就不会自动执行其后所定义的命令。要执行其后的命令，就要在 make 命令后明显得指出这个 label 的名字，比如 make clean 即清除所有的目标文件。这样的方法非常有用，我们可以在一个 makefile 中定义不用的编译或是和编译无关的命令，比如程序的打包，程序的备份，等等。


### make 是如何工作的

当输入 make 的时候，

1. make 会在当前的目录下寻找名字为 Makefile 或者 makefile 的文件
2. 找到之后，它会找文件中的第一个目标文件，即第一个 target。并将这个文件作为最终的目标文件，比如上述的 edit。
3. 如果 edit 文件不存在，或是 edit 所依赖的后面的 .o 文件的文件修改时间要比 edit 这个文件新，那么，他就会执行后面所定义的命令来生成 edit 这个文件。
4. 如果 edit 所依赖的 .o 文件也不存在，那么 make 会在当前文件中找目标为 .o 文件的依赖性，如果找到则再根据那一个规则生成 .o 文件。（这有点像一个堆栈的过程）
5. 由于对应的 c 文件和头文件存在，于是 make 会生成 .o 文件，然后再用 .o 文件生成 make 的终极任务，也就是可执行文件 edit 了


make 会一层一层的找文件的依赖关系，直至编译出第一个目标文件。在寻找的过程中，如果出现了错误，或者最后的文件找不到，那么 make 就会直接退出。


### makefile 中使用变量

再看一下上面的 edit 的规则和 clean 的规则

    edit : main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o
    cc -o edit main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o
    ...
    clean :
        rm edit main.o kbd.o command.o display.o \
            insert.o search.o files.o utils.o

可以看到 .o 文件的字符串被重复了两次，如果工程中需要加入一个新的 .o 文件，那么我们需要在这三个地方加。当然，这个 makefile 并不复杂，所以在三个地方加也不麻烦，但如果makefile 变得复杂，那么我们就有可能会忘掉一个需要加入的地方，而导致编译失败。所以，为了 makefile 的易维护，在 makefile 中我们可以使用变量。makefile的变量也就是一个字符串，理解成C语言中的宏可能会更好。

引入变量之后的 makefile 如下

    objects = main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o
    edit : $(objects)
        cc -o edit $(objects)
    main.o : main.c defs.h
        cc -c main.c
    kbd.o : kbd.c defs.h command.h
        cc -c kbd.c
    command.o : command.c defs.h command.h
        cc -c command.c
    display.o : display.c defs.h buffer.h
        cc -c display.c
    insert.o : insert.c defs.h buffer.h
        cc -c insert.c
    search.o : search.c defs.h buffer.h
        cc -c search.c
    files.o : files.c defs.h buffer.h command.h
        cc -c files.c
    utils.o : utils.c defs.h
        cc -c utils.c
    clean :
        rm edit $(objects)

如果后续有新的 .o 文件加入，只需要修改 objects 即可。

### make 自动推导

只要 make 看到一个 .o 文件，就会自动把 .c 文件加在依赖关系中。如果 make 找到一个 whatever.o ，那么 whatever.c 就会是 whatever.o 的依赖文件。并且 cc -c whatever.c 也会被推导出来，就可以简化 makefile

    objects = main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o
    edit : $(objects)
        cc -o edit $(objects)
    main.o : defs.h
    kbd.o : defs.h command.h
    command.o : defs.h command.h
    display.o : defs.h buffer.h
    insert.o : defs.h buffer.h
    search.o : defs.h buffer.h
    files.o : defs.h buffer.h command.h
    utils.o : defs.h

    .PHONY : clean
    clean :
        rm edit $(objects)

.PHONY 表示 clean 是个伪目标文件，会在后续详细介绍。


### 另一种 makefile 风格

可以看到上面的 makefile 里面，头文件有很多重复的，因此还可以进一步简化

    objects = main.o kbd.o command.o display.o \
        insert.o search.o files.o utils.o

    edit : $(objects)
        cc -o edit $(objects)

    $(objects) : defs.h
    kbd.o command.o files.o : command.h
    display.o insert.o search.o files.o : buffer.h

    .PHONY : clean
    clean :
        rm edit $(objects)

`defs.h` 是所有目标文件的依赖文件， `command.h` 和 `buffer.h` 是对应目标文件的依赖文件。这种方式可以简化 makefile，但是其依赖关系就会变得很乱。当要多加如几个 .o 文件时就会比较麻烦。

### make clean

clean 的规则不要放在文件的开头，否则就会变成 make 的默认目标，一般 clean 都是放在最后。

以上就介绍了一个 makefile 的基础，还有很多细节在下面介绍。

### makefile 里有什么

makefile 里面主要包括了5个东西：显式规则、隐式规则、变量定义、指令和注释


|组成|说明|
|-|-|
|显式规则|显式规则说明了如何生成一个或多个目标文件。这是由 makefile 的书写者明显指出要生成的文件、文件的依赖文件和生成的命令。|
|隐式规则|make 有自动推导的功能，所以隐式规则可以让我们比较简略地书写Makefile，这是由make所支持的。|
|变量|在 makefile 中我们要定义一系列的变量，变量一般都是字符串，这个有点像你C语言中的宏，当 makefile 被执行时，其中的变量都会被扩展到相应的引用位置上。|
|指令|包括了三个部分，一个是在一个 makefile 中引用另一个 makefile，就像C语言中的include一样；另一个是指根据某些情况指定 makefile中的有效部分，就像C语言中的预编译#if一样；还有就是定义一个多行的命令。|
|注释|makefile 中只有行注释，和 UNIX 的 Shell 脚本一样，其注释是用 # 字符。如果你要在 makefile 中使用 # 字符，可以用反斜杠进行转义，如： \# 。|


### makefile 文件名

make 命令会在当前目录下按顺序寻找文件名为 GNUmakefile 、 makefile 和 Makefile 的文件。最好使用 Makefile 这个文件名，因为这个文件名在排序上靠近其它比较重要的文件，比如 README。最好不要用 GNUmakefile，因为这个文件名只能由 GNU make ，其它版本的 make 无法识别，但是基本上来说，大多数的 make 都支持 makefile 和 Makefile 这两种默认文件名。

也可以使用别的文件名来写 Makefile，如果要指定特定的 Makefile。可以使用 make 的 -f 或者 --file 参数。例如

    make -f Make.Linux

也可以使用 -f 参数指定多个 Makefile 文件

### 包含其他的 makefile

在 makefile 中可以使用 `include` 指令将别的 makefile 包含进来，被包含的文件会原模原样的放在当前文件的包含位置。 `include` 的语法是：

    include <filename>...

在 `include` 前面可以有一些空字符，但是绝不能是 Tab 键开始。 `include` 和`<filenames>` 可以用一个或多个空格隔开。

有这样几个 Makefile： `a.mk` 、 `b.mk` 、 `c.mk` ，还有一个文件叫 `foo.make` ，以及一个变量 `$(bar)` ，其包含了 `bish` 和 `bash`

    include foo.make *.mk $(bar)

等价于

    include foo.make a.mk b.mk c.mk bish bash

make 命令开始时，会找寻 `include` 所指出的其它 Makefile，并把其内容安置在当前的位置。如果文件都没有指定绝对路径或是相对路径的话，make 会在当前目录下首先寻找，如果当前目录下没有找到，那么，make 还会在下面的几个目录下找：

- 如果 make 执行时，有 `-I` 或 `--include-dir` 参数，那么 make 就会在这个参数所指定的目录下去寻找。
- 接下来按顺序寻找目录 `<prefix>/include` （一般是 `/usr/local/bin` ）、 `/usr/gnu/include` 、 `/usr/local/include` 、 `/usr/include` 。

环境变量 `.INCLUDE_DIRS` 包含当前 make 会寻找的目录列表。应当避免使用命令行参数 `-I` 来寻找以上这些默认目录，否则会使得 make “忘掉”所有已经设定的包含目录，包括默认目录。


如果有文件没有找到的话，make会生成一条警告信息，但不会马上出现致命错误。它会继续载入其它的文件，一旦完成 makefile 的读取，make 会再重试这些没有找到，或是不能读取的文件，如果还是不行，make 才会出现一条致命信息。如果你想让make不理那些无法读取的文件，而继续执行，可以在 include 前加一个减号“-”。如：

    -include <filenames>...

表示，无论`include`过程中出现什么错误，都不要报错继续执行。

### make 的工作方式

GNU 的 make 工作时的执行步骤如下：
1. 读入所有的 Makefile。
2. 读入被 `include` 的其它 Makefile。
3. 初始化文件中的变量。
4. 推导隐式规则，并分析所有规则。
5. 为所有的目标文件创建依赖关系链。
6. 根据依赖关系，决定哪些目标要重新生成。
7. 执行生成命令。

## 书写规则

makefile 只有一个最终目标，其他的目标都是被这个目标连带出来的。一般来说，makefile 中的第一条规则中的目标会被确认为最终的目标。如果一条规则中的目标有多个，那么第一个目标会成为最终的目标。

规则格式如下：

    targets : prerequisites
        command
        ...

或者

    targets : prerequisites ; command

### 在规则中使用通配符

make 支持3个通配符，`*`,`?`,`~`。

波浪号（ `~` ）字符在文件名中也有比较特殊的用途。如果是 `~/test` ，这就表示当前用户的 `$HOME` 目录下的`test`目录。而 `~hchen/test` 则表示用户`hchen`的宿主目录下的`test` 目录。（这些都是Unix下的小知识了，make也支持）而在 Windows 或是 MS-DOS下，用户没有宿主目录，那么波浪号所指的目录则根据环境变量`“HOME”`而定。

通配符代替了你一系列的文件，如 `*.c` 表示所有后缀为`c`的文件。一个需要我们注意的是，如果我们的文件名中有通配符，如： `*` ，那么可以用转义字符 `\` ，如 `\*`来表示真实的 `*` 字符，而不是任意长度的字符串。