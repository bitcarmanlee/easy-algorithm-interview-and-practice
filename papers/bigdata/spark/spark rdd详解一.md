## 1.rdd简介
与许多专有的大数据处理平台不同，Spark建立在统一抽象的RDD之上，使得它可以以基本一致的方式应对不同的大数据处理场景，包括MapReduce，Streaming，SQL，Machine Learning以及Graph等。这即Matei Zaharia所谓的“设计一个通用的编程抽象（Unified Programming Abstraction）。  

RDD的全称为Resilient Distributed Datasets，是一个并行的，容错的数据结构，方便让用户显式地存储于内存中(当内存不够只有存储在磁盘上)，并且方便用户控制数据的分区。  

RDD是spark中的核心概念，是一个只读的分布式内存数据集。与hadoop不一样的地方在于这个数据集是缓存在内存之中，特别方便于数据的迭代计算。在用户访问RDD时，指针只会指向与操作相关的部分，这样就避免了对整个数据集进行全局扫描。  


## 2.transformation与action
RDD中提供了两种类型的操作：transformation与action。  
首先需要明确的一点是：rdd无论执行了多少次的transformation操作，rdd都没有真正执行运算，只是从一个rdd转换成另一个rdd而已。只有当某一个action操作被执行后，才真正触发运算。这就是所谓的transformation采取的是懒加载策略(lazy)。  

transformation，顾名思义，是得到一个新的rdd。生成一个rdd有两种方法：1.从数据源生成一个rdd。2.由一个rdd生成一个新的rdd。  
常见的transformation有map,filter,flatMap,union,join,reduceByKey等操作，后续再进行详细的介绍。  
action，是得到一个值，或者得到一个结果直接cache到内存中。  
常见的action操作有take,count,collect,reduce,foreach,saveAsTextFile,saveAsSequenceFile等。  

## 3.窄依赖与宽依赖
RDD作为数据结构，本质上是一个只读的分区记录集合。一个RDD可以包含多个分区，每个分区就是一个dataset片段。RDD可以相互依赖。如果RDD的每个分区最多只能被一个Child RDD的一个分区使用，则称之为窄依赖narrow dependency；若多个Child RDD分区都可以依赖，则称之为宽依赖wide dependency。不同的操作依据其特性，可能会产生不同的依赖。例如map操作会产生narrow dependency，而join操作则产生wide dependency。    

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/rdd/1.png)    

Spark之所以将依赖分为narrow与wide，基于两点原因：一个结点上得管道化执行与更好地处理失败恢复。  

首先，narrow dependencies可以支持在同一个cluster node上以管道形式执行多条命令，例如在执行了map后，紧接着执行filter。相反，wide dependencies需要所有的父分区都是可用的，可能还需要调用类似MapReduce之类的操作进行跨节点传递。      

其次，则是从失败恢复的角度考虑。narrow dependencies的失败恢复更有效，因为它只需要重新计算丢失的parent partition即可，而且可以并行地在不同节点进行重计算。而wide dependencies牵涉到RDD各级的多个Parent Partitions。（此部分内容摘自于网络）      

## 4.容错
一般来说，分布式数据集的容错性有两种方式：数据检查点和记录数据的更新。    
面向大规模数据分析，数据检查点操作成本很高，需要通过数据中心的网络连接在机器之间复制庞大的数据集，而网络带宽往往比内存带宽低得多，同时还需要消耗更多的存储资源。    

因此，Spark选择记录更新的方式。但是，如果更新粒度太细太多，那么记录更新成本也不低。Spark RDD只支持粗粒度的操作，对一个RDD的操作都会被作用于该RDD的所有数据；为了保证RDD的高可用性RDD通过使用Lineage（血统）记录了RDD演变流程（从其他RDD到当前RDD所做的操作） 当RDD分区数据丢失时可以通过Lineage的信息重新计算与恢复分区数据，或进行RDD的重建。    

