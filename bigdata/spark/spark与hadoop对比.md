## 1.hadoop解决了什么问题
Hadoop就是解决了大数据（大到一台计算机无法进行存储，一台计算机无法在要求的时间内进行处理）的可靠存储和处理。  
HDFS，在由普通PC组成的集群上提供高可靠的文件存储，通过将块保存多个副本的办法解决服务器或硬盘坏掉的问题。  
MapReduce，通过简单的Mapper和Reducer的抽象提供一个编程模型，可以在一个由几十台上百台的PC组成的不可靠集群上并发地，分布式地处理大量的数据集，而把并发、分布式（如机器间通信）和故障恢复等计算细节隐藏起来。而Mapper和Reducer的抽象，又是各种各样的复杂数据处理都可以分解为的基本元素。这样，复杂的数据处理可以分解为由多个Job（包含一个Mapper和一个Reducer）组成的有向无环图（DAG）,然后每个Mapper和Reducer放到Hadoop集群上执行，就可以得出结果。  

在MapReduce中，Shuffle是一个非常重要的过程，正是有了看不见的Shuffle过程，才可以使在MapReduce之上写数据处理的开发者完全感知不到分布式和并发的存在。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/hadoopvsspark/1.png)  
广义的Shuffle是指图中在Map和Reuce之间的一系列过程。  
yarn，之前mrv1版本是用的jobtracker进行任务调度，mrv2的版本重构替换为yarn。重构根本的思想是将 JobTracker 两个主要的功能分离成单独的组件，这两个功能是资源管理和任务调度 / 监控。新的资源管理器全局管理所有应用程序计算资源的分配，每一个应用的 ApplicationMaster 负责相应的调度和协调。一个应用程序无非是一个单独的传统的 MapReduce 任务或者是一个 DAG( 有向无环图 ) 任务。ResourceManager 和每一台机器的节点管理服务器能够管理用户在那台机器上的进程并能对计算进行组织。  

## 2.hadoop的局限与不足
但是，MapRecue存在以下局限，使用起来比较困难。  
1.抽象层次低，需要手工编写代码来完成，使用上难以上手。  
2.只提供两个操作，Map和Reduce，表达力欠缺。  
3.一个Job只有Map和Reduce两个阶段（Phase），复杂的计算需要大量的Job完成，Job之间的依赖关系是由开发者自己管理的。  
4.处理逻辑隐藏在代码细节中，没有整体逻辑  
5.中间结果也放在HDFS文件系统中  
6.ReduceTask需要等待所有MapTask都完成后才可以开始。时延高，只适用Batch数据处理，对于交互式数据处理，实时数据处理的支持不够    
7.对于迭代式数据处理性能比较差  

比如说，用MapReduce实现两个表的Join都是一个很有技巧性的过程，如下图所示：  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/hadoopvsspark/2.png)  

mr中的join就是个相当费劲的操作，只要是写过mr代码的同学都能体会到。  

## 3.spark的优势之一
Apache Spark是一个新兴的大数据处理的引擎，主要特点是提供了一个集群的分布式内存抽象，以支持需要工作集的应用。  

这个抽象就是RDD（Resilient Distributed Dataset），RDD就是一个不可变的带分区的记录集合，RDD也是Spark中的编程模型。Spark提供了RDD上的两类操作，转换和动作。转换是用来定义一个新的RDD，包括map, flatMap, filter, union, sample, join, groupByKey, cogroup, ReduceByKey, cros, sortByKey, mapValues等，动作是返回一个结果，包括collect, reduce, count, save, lookupKey。  

Spark的API非常简单易用，Spark的WordCount的示例如下所示：  

```
val spark = new SparkContext(master, appName, [sparkHome], [jars])
val file = spark.textFile("hdfs://...")
val counts = file.flatMap(line => line.split(" "))
                 .map(word => (word, 1))
                 .reduceByKey(_ + _)
counts.saveAsTextFile("hdfs://...")
```  

其中的file是根据HDFS上的文件创建的RDD，后面的flatMap，map，reduceByKe都创建出一个新的RDD，一个简短的程序就能够执行很多个转换和动作。  

在Spark中，所有RDD的转换都是是惰性求值的。RDD的转换操作会生成新的RDD，新的RDD的数据依赖于原来的RDD的数据，每个RDD又包含多个分区。那么一段程序实际上就构造了一个由相互依赖的多个RDD组成的有向无环图（DAG）。并通过在RDD上执行动作将这个有向无环图作为一个Job提交给Spark执行。  

例如，上面的WordCount程序就会生成如下的DAG  

```
scala> counts.toDebugString
res0: String =
MapPartitionsRDD[7] at reduceByKey at <console>:14 (1 partitions)
  ShuffledRDD[6] at reduceByKey at <console>:14 (1 partitions)
    MapPartitionsRDD[5] at reduceByKey at <console>:14 (1 partitions)
      MappedRDD[4] at map at <console>:14 (1 partitions)
        FlatMappedRDD[3] at flatMap at <console>:14 (1 partitions)
          MappedRDD[1] at textFile at <console>:12 (1 partitions)
            HadoopRDD[0] at textFile at <console>:12 (1 partitions)
```  

Spark对于有向无环图Job进行调度，确定阶段（Stage），分区（Partition），流水线（Pipeline），任务（Task）和缓存（Cache），进行优化，并在Spark集群上运行Job。RDD之间的依赖分为宽依赖（依赖多个分区）和窄依赖（只依赖一个分区），在确定阶段时，需要根据宽依赖划分阶段。根据分区划分任务。  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/hadoopvsspark/3.png)  

Spark支持故障恢复的方式也不同，提供两种方式，Linage，通过数据的血缘关系，再执行一遍前面的处理，Checkpoint，将数据集存储到持久存储中。  

Spark为迭代式数据处理提供更好的支持。每次迭代的数据可以保存在内存中，而不是写入文件。  

Spark的性能相比Hadoop有很大提升，2014年10月，Spark完成了一个Daytona Gray类别的Sort Benchmark测试，排序完全是在磁盘上进行的，与Hadoop之前的测试的对比结果如表格所示：  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/hadoopvsspark/4.png)    

从表格中可以看出排序100TB的数据（1万亿条数据），Spark只用了Hadoop所用1/10的计算资源，耗时只有Hadoop的1/3。  


## 4.spark优势之二
Spark的优势不仅体现在性能提升上的，Spark框架为批处理（Spark Core），交互式（Spark SQL），流式（Spark Streaming），机器学习（MLlib），图计算（GraphX）提供一个统一的数据处理平台，这相对于使用Hadoop有很大优势。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/hadoopvsspark/5.png)  
按照Databricks的连城的说法是One Stack To Rule Them All  

特别是在有些情况下，你需要进行一些ETL工作，然后训练一个机器学习的模型，最后进行一些查询，如果是使用Spark，你可以在一段程序中将这三部分的逻辑完成形成一个大的有向无环图（DAG），而且Spark会对大的有向无环图进行整体优化。  

例如下面的程序：  

```
val points = sqlContext.sql(   “SELECT latitude, longitude FROM historic_tweets”)  

val model = KMeans.train(points, 10)  

sc.twitterStream(...)   .map(t => (model.closestCenter(t.location), 1))   .reduceByWindow(“5s”, _ + _)

```  

这段程序的第一行是用Spark SQL 查寻出了一些点，第二行是用MLlib中的K-means算法使用这些点训练了一个模型，第三行是用Spark Streaming处理流中的消息，使用了训练好的模型。  