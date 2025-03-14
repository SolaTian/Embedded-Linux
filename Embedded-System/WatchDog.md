# WatchDog

嵌入式设备一般都是有一个主进程，若干个子进程一起协同工作的，当我们的设备主进程在运行过程中由于一些因素挂掉时，整个系统都会崩溃，设备挂掉开始重启，如果这个因素必现，那么设备就会出现反复重启的情况。什么都无法操作。“设备就变砖了”，这种情况非常让人头大，只能带着串口线到设备旁边进行串口升级……

既然嵌入式系统是一个 Linux 系统，是一台“电脑”，那么为什么一个进程挂掉之后，这个“电脑”就起不来了呢？

嵌入式系统由于资源受限，当主进程崩溃之后，系统重启的原因可能为：

1. 主进程负责初始化硬件，加载必要的驱动，缺少主进程，系统将无法正常运行
2. 嵌入式系统不像正真的电脑，缺乏复杂的错误处理恢复机制
3. 主进程往往负责关系系统资源，如内存、I/O 设备等。主进程崩溃可能导致资源无法正确释放或管理，其他进程可能无法继续运行，迫使系统重启。
4. 看门狗机制：嵌入式系统中常用看门狗定时器来监控系统状态。如果主进程因故障未能在指定时间内重置看门狗，系统将自动重启以避免死机。

前面几点原因可能与嵌入式系统的特性、内核机制有关。看门狗机制可以在主进程应用软件中或者硬件中设置，来主要研究一下。

## Watchdog 的分类

|特性|软件看门狗 Software Watchdog |硬件看门狗 Hardware Watchdog|
|-|-|-|
|实现方式|软件实现，依赖系统进程，一般是主进程|硬件电路实现，独立于系统软件。|
|监控范围|监控特定进程或系统状态。|监控整个系统运行状态。|
|触发机制|软件检测异常条件，触发恢复措施。|硬件检测超时或异常，触发硬件重置。|
|可靠性|可靠性依赖于软件，可能受软件崩溃影响。|硬件独立运行，可靠性更高。|
|资源需求|无需额外硬件，完全软件实现。|需要额外硬件，增加系统复杂性和成本。|
|应用场景|适用于资源受限的嵌入式系统。|适用于高可靠性要求的嵌入式系统。|


## 软狗 Software Watchdog

> 软狗（Software Watchdog），是一种通过软件实现的监控机制。监控系统的运行状态，确保系统或特定进程在预期的时间内正常响应。如果系统或进程由于某种原因（如崩溃、死锁或无限循环）未能及时响应，软狗会触发相应的恢复措施，例如重启系统或启动错误处理程序。



软狗的工作原理：
1. 主进程在初始化时，会初始化一个软件看门狗，一般可能为一个全局的消息队列
2. 在主进程的其他地方，初始化看门狗任务线程
3. 看门狗线程的主要是一个循环，用于监测当前系统的各个状态，比如一些关键子进程是否还在运行，

## 硬狗 Hardware Watchdog


