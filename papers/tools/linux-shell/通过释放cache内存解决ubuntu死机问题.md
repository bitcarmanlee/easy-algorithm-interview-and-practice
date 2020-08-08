## 1.ubuntu老死机
工作机器是ubuntu系统，配有16G的物理内存。按理说这个内存量已经不小了，但是同时还运行了一个windows虚拟机，所以机器的资源会略显紧张。每次系统运行不了多少时间，多则三五天，少则一两天，系统就卡死不动了。。。任何操作都没法解决这个问题，每次只能重启大法，长按power键，重启机器。终于某一次一天之内重启两次以后，本人实在受不了了，下决心要解决这个问题。。  


根据之前的几次经验来看，每次快要死机之前，用free查看机器的内存使用情况，发现cache的内存都特别大，初步怀疑是内存不够捣的鬼。虽然linux系统里会有cache内存释放策略，但是linux内核这种东西，谁知道呢。。。好吧，那咱们写个脚本给强制释放一下cache好了。。。  

## 2.释放cache内存
写了个简单的脚本：  

```
#!/bin/bash                                                                                                                                                                                                 

sync && echo 1 | sudo tee /proc/sys/vm/drop_caches
sync && echo 2 | sudo tee /proc/sys/vm/drop_caches
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```  

然后加到crontab里，每小时执行一次，定时释放cache。。。  
几天以后，发现脚本没有起作用。。。每次查看内存使用情况，发现cache并没有释放。。。该死机还是死机。。。  
想了想，`/proc/sys/vm/drop_caches`这个路径，普通账号应该是没有权限去操作的。。。  
果断将这个脚本添加到root的crontab里，每小时跑一次。发现起作用了。。。  
距上次强制重启已经两周，完美解决。。。  

## 3.sync命令
sync命令用于强制被改变的内容立刻写入磁盘，更新超块信息。 在Linux/Unix系统中，在文件或数据处理过程中一般先放到内存缓冲区中，等到适当的时候再写入磁盘，以提高系统的运行效率。sync命令则可用来强制将内存缓冲区中的数据立即写入磁盘中。用户通常不需执行sync命令，系统会自动执行update或bdflush操作，将缓冲区的数据写 入磁盘。只有在update或bdflush无法执行或用户需要非正常关机时，才需手动执行sync命令。  

## 4.cache内存与buffer内存区别
查看内存一般使用free 命令：  

```
xxx@xxx:~/xxx/code/shell/base$ free -m
1              total       used       free     shared    buffers     cached
2 Mem:         15929      11503       4425        991         35       1328
3 -/+ buffers/cache:      10139       5789
4 Swap:        16263          5      16258
```  

free的输出一共有四行，第四行为交换区的信息，分别是交换的总量（total），使用量（used）和有多少空闲的交换区（free），这个比较清楚，不说太多。  

free输出地第二行和第三行是比较让人迷惑的。这两行都是说明内存使用情况的。第一列是总量（total），第二列是使用量（used），第三列是可用量（free）.  

第二行的输出时从操作系统（OS）来看的。也就是说，从OS的角度来看。  
其中，Mem shared 表示被几个进程共享的内存的。Mem buffers表示被OS buffer住的内存，Mem cached 表示被OS cache的内存。buffers跟cached的区别如下：  

buffer是用于存放要输出到disk（块设备）的数据的，而cache是存放从disk上读出的数据。这二者是为了提高IO性能的，并由OS管理。  

Linux和其他成熟的操作系统（例如windows），为了提高IO read的性能，总是要多cache一些数据，所以总要多cache一些数据。  

第三行是从一个应用程序的角度看系统内存的使用情况。  
因为被系统cache和buffer占用的内存可以被快速回收，所以第三行对应free那一列的值会很大。  

最后总结ubuntu死机这个case来看，就是系统cache的内存太多，没有及时释放，导致系统死机！解决方案就是我们写个脚本定期释放cache内存，就可以避免死机的发生！  