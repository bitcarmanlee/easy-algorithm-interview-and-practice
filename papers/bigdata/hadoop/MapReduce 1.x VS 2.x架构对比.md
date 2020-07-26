## 1.Hadoop 1.X架构  
Hadoop 1.X的组件主要有两个  
1.HDFS(HDFS V1)  
2.MapReduce(MR V1)   
其中HDFS是分布式文件存储系统，MapReduce是计算框架。  

MapReduce 1.X是Master/Slave家头，有全局唯一的Jobtracker与多个TaskTracker。其中Master是指唯一的Jobtracker，slave是指TaskTracker。具体框架图如下  

![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/1vs2/1.png)  

其中各个组件的作用是:  

### 1.1 JobTracker
JobTracker是全局唯一的，并且JobTracker做了很多事情：资源管理，作业调度，作业监控，重新调度作业等。JobTracker会对集群中所有的TaskTracker进行监控，一旦TaskTracker出现宕机、失败等情况，JobTracker中的调度器会将原来在这个TaskTracker上面执行的任务转移到其他的节点上面继续执行。当有新的作业进入到集群中时，调度器会根据资源的使用情况合理的分配这些作业。但是从上面的描述以及框架图不难看出，JobTracker做了太多的事情，并且存在单点情况，一旦JobTracker所在的机器搞了点什么幺蛾子，整个集群就凉凉。。。所以在Hadoop 2.X中，将JobTracker进行了拆解与优化。  

### 1.2 TaskTracker  
TaskTracker使用 “slot” 对本节点的资源（cpu、内存、磁盘等）进行划分，负责具体的作业执行工作。TaskTracker需要周期性向JobTracker汇报本节点的心跳信息，包括自身运行情况、作业执行情况等，JobTracker中的调度器会根据心跳信息对其分配“slot”，TaskTracker获得slot之后，就开始执行相应的工作。其中 slot 有两种： MapSlot 和 TaskSlot ，分别负责执行Map任务和Task任务，二者互不影响。  


### 1.3 Client

client相对来说比较简单，就是让用户将MR程序提交给JobTracker上。  

### 1.4 Task
Task里面就是大名鼎鼎的MapTask与ReduceTask了。MapReduce的输入数据会被切分成多个split，每个split会给一个Map Task去执行。之后的结果经过shuffle等过程，然后被切成多个partition，每个partition会有一个ReduceTask去执行。  

## 2.Hadoop 2.X架构
前面提到，1.X架构里主要的单点故障在JobTracker，同时JobTracker负责的事情太多，压力具体，很容易出现问题。因此在2.X架构中，对原有的MapReduce架构进行改造，使其成为在YARN上面运行的一个计算框架。  
  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/1vs2/2.png)  

YARN将MapReduce 1.X 中的JobTracker拆分成了两个独立的组件：  
1  ResourceManager  
全局资源管理器，全局唯一。负责整个集群的资源管理和分配，主要由负责资源调度分配的调度器和负责应用程序提交协商的应用程序管理器组成。一句话总结，ResourceManager是管理资源的。  
  
2 ApplicationMaster  
用户提交的每个应用程序 / 作业都会带有一个ApplicationMaster，负责与ResourceManager中的调度器通信获得资源，将得到的任务进行分配，监控作业的执行情况。一句话总结，ApplicationMaster是管理应用的。  

除了这两个组件以外，YARN还有如下的重要组件：  
NodeManager  
该进程位于从节点（和DataNode进程一同运行），用来管理和执行容器Container，监控资源使用情况（CPU，内存，网络等），并把情况报告返回给ResourceManager，同时周期性地发送心跳信息给ResourceManager，更新他的健康状态。  

Container  
一个很小的资源单元（CPU，内存，硬盘），位于从节点上。Scheduler 进程和ResourceManager 进程一起运行对容器进行资源分配，通过Yarn　执行一个Job的初始阶段，容器允许ApplicationMaster进程在集群的从节点上利用一些资源，Application通过在Yarn集群从节点的其他容器来来管理应用的执行。  

## 3.yarn提交任务的流程  
1.Job/Application(可以是MR，Java/Scala应用，spark的DAGs作业等)通过Yarn应用的客户端提交到ResourceManager，与此同时，在NodeManager的任何容器中启动ApplicationMaster  
2.在主节点上的ApplicationManager进程验证已提交的任务请求，并且通过Scheduler进行进行资源的分配  
3.Scheduler进程给在从节点上的ApplicationMaster分配一个容器  
4.NodeManager这个守护进程启动AppcationMaster服务，通过第一步的命令，在其中一个容器当中  
5.ApplicationMaster通过ResourceManger谈判协商其他的容器，来提供一些细节，诸如从节点的数据位置，请求的CPU，内存，核数等  
6.ResourceManger分配最合适的从节点资源，并且通过节点细节或是其他细节信息响应ApplicaionMaster  
7.ApplicationMaster 给NodeManager（建议的从节点上）发送请求，来启动容器  
8.当作业执行是，ApplicationMaster管理已经请求的容器的资源，并在执行完成后通知ResourceManger  
9.NodeManagers周期性的通知ResourceManger，节点的可用资源的当前状态信息，这个信息可以被scheduler 在集群中的其他应用所使用  
10.如果在从节点上有任何的失败，ResourceManager 将会试着在最合适的节点上分配新的容器，那样 ApplicationMaster 能够在新的容器中完成相应的处理操作  