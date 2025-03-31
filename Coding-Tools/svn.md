# SVN

> SVN（版本控制系统）:用于管理软件开发过程中的代码版本的工具

## 检出-checkout

    svn co(checkout) <服务器代码路径> <本地目录>

若不加本地目录则默认当前目录

## 更新-update

    #更新本地工作副本到最新版本
    svn up(update)
    #更新本地工作副本到指定版本
    svn up(update) -r(--revision) <版本号>

如果在指定目录下执行此命令，会更新该目录及其子目录下的所有文件，也可以指定特定的文件或目录进行更新：
    svn up(update) specific_file.txt

## 新增-add

    svn add <文件或者目录名>

执行此命令后，还需要使用 `svn commit` 命令将删除操作提交到仓库。

## 删除-delete

    #删除文件或者目录
    svn del(delete) <文件或目录名>

执行此命令后，还需要使用 `svn commit` 命令将删除操作提交到仓库。

## 状态-status

    #查看本地副本的工作状态，显示文件的修改情况
    svn st(status)

常见状态标识

- A：新增的文件或目录。
- M：已修改的文件
- D：已删除的文件。
- ?：未被 SVN 管理的文件。

## 差异-diff

    #查看本地文件与 SVN 仓库文件中的差异
    svn diff [OPTIONS] <文件或目录名>

目标路径：可以是本地工作副本中的文件或目录，也可以是版本库的 URL。如果不指定目标路径，默认会显示当前目录及其子目录下的提交日志。

常见参数如下：
- `-r REV1:REV2 或 --revision=REV1:REV2`：比较两个不同版本（REV1 和 REV2）之间的差异
- `--summarize`：仅显示有差异的文件列表，不显示具体的修改内容，可快速了解哪些文件被修改
- `-x ARGS 或 --extensions=ARGS`：将额外的参数传递给底层的 diff 工具，以自定义差异显示格式

    #查看当前工作副本中的文件与版本库中最新版本的差异
    svn diff
    #比较版本号 100 和 105 之间 example.txt 文件的差异
    svn diff -r 100:105 example.txt
    #仅显示有差异的文件列表,不查看具体的修改内容
    svn diff --summarize
    #比较本地文件与指定版本的差异
    svn diff -r 50 example.txt

当比较大量文件或较大版本范围时，`svn diff` 可能会消耗较多时间和系统资源。可以加上`--summarize`

## 撤销-revert

    #撤销本地文件的修改，使其恢复到上一次从 SVN 仓库更新或提交时的状态
    svn revert <文件或目录名>
    #对指定目录及其所有子目录和文件进行递归操作
    svn revert -R <目录名>

撤销不可逆

## 提交-commit

    svn ci(commit) -m "提交说明" <文件或目录名>

## 日志-log

    svn log <目标路径> [OPTIONS]

目标路径：可以是本地工作副本中的文件或目录，也可以是版本库的 URL。如果不指定目标路径，默认会显示当前目录及其子目录下的提交日志。

参数包括以下：
- `-r(--revision)`:指定版本范围
- `-l(--limit)`:限制显示的日志数量
- `-v（--verbose）`:显示详细信息

使用`--xml`将日志以 XML 格式输出

    svn log --xml > log.xml

## 切分支-cpoy

    svn cp [OPTIONS] <SOURCE> <DEST>

常用参数
- `-m MESSAGE 或 --message=MESSAGE`：为复制操作添加日志消息。
- `-r REVISION 或 --revision=REVISION`：指定要复制的源文件或目录的版本号。
