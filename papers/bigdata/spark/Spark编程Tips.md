1.尽量用 aggregateByKey 和 ReduceByKey和CombineByKey, 替代 groupByKey。这个开发过程中深有体会，groupByKey极易引发各种OOM。。。  

2.repartition 适用于 RDD[V], partitionBy 适用于 RDD[K, V].  

3.尽量避免在一个 transformation 中处理所有的逻辑, 尽量分解成 map, filter 等之类的操作  

4.如果有 RDD 复用, 特别是该 RDD 是需要花费比较长时间才能运算出来的, 建议对该 RDD 做 cache, 如果该 RDD 每个 partition 需要消耗很多的内存, 建议开启 Kryo 序列化机制(可节省2到5倍的空间) 如果还是有比较大的内存开销, 建议将该 RDD 的 storage level 设置成MEMORY_AND_DISK_SER    

5.用户程序打包时, 可以在 pom.xml 中将 spark 依赖, hbase 依赖, hadoop 依赖都设置成 provided  

6.选择了yarn-client模式, 因此是默认没有开启本地 Driver 的 gc log 的, 为了更好应对出错时 debug, 建议在本地 export SPARK_SUBMIT_OPTS=" -Xloggc:tmp/gc_log -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCDetails -XX:+PrintGCDateStamps -verbose:gc -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=10M "    

7.多个RDD union时, 避免使用rdd.union(rdd).union(rdd).union(rdd)的操作, rdd.union只适合两个rdd的操作, 多个RDD union时采用SparkContext.union(Array(RDD))，以此避免union操作嵌套层数太多，从而过程调用链路太长, 耗时甚至引发StackOverFlow  

8.Spark coGroup/join类/XXXByKey等操作中都可以指定partitions的个树, 不需要额外使用repartition操作和partitionBy操作.  

9.尽量保证每轮Stage里每个Task处理的数据量 > 128MB.  

10.读取的HDFS文件的如果是大量很小的, 使用Hadoop的combineinputformat读取.  

11.如果两个RDD做join, 其中一个数据量很小, 采用BroadcastJoin, 将小的RDD数据 Collect回Driver, 将其BroadCast到另一个RDD中.  

12.两个RDD做cartesian时, 数据小的RDD作为参数传入, 类似BigRDD.cartesian(smallRDD)  

13.如果需要broadcast一个大的对象到远端, 当作字典查询, 建议多executor-cores, 大executor-memory. executor-memory的值可以参考, 假设先将该大字典是放在一个外部存储系统时, executor-cores=1, executor-memory=m(g, 默认=2g)时可以正常运行, 当大字典的size=n(g)时, executor-memory=2n, 且executor-cores=n/m, (向上取整)  

14.如果实在无法broadcast到远端, 可采用一种zipPartitions方式实现的hash join的方式，前提是根据大RDD的的Key去Refer小RDD中的key,而不是根据大RDD中的value, 去Refer小RDD中的Key:  

```
val rdd1: RDD[(KeyType, ValueType)] =.... // BigOne, partitions = 1000
val rdd2: RDD[(keyType, ValueType)] = .... // SmallOne, partitions = 100

val rdd2Partioned = rdd2.partitionBy(new HashPartitioner(1000)) // 保持与大的rdd1的partitions大小一致.

val rdd2HashMapedPartioned = rdd2Partioned.mapPartitions { iter =>
  val mapData = new HashMap[KeyType, ValueType]()
  iter.map { case (key, value) =>
    mapData.put(key, value)
  }
  Iterator(mapData)
}

rdd1.zipPartitions(rdd2, preservesPartitioning = true)({ case (iter1, iter2) =>
  iter2.map { rdd2Map =>
    iter1.map { case (key, value) =>
      val rdd2KeyValue = rdd2Map.get(key)
      // 这里则可以根据Rdd1中的Key, Value, 和rdd2中对应的map去做相应的逻辑处理
    }
  }
})
```  

15.在编写程序时, 应时刻考虑处理过程中如何出来异常数据.  

16.有异常数据时, 存在单个Key的values过多, 在做aggregateByKey/groupByKey等操作时, 应该时刻关注是否需要保留过多的values, 是否可以判定values size超过某特定大小的(如1000)key为异常数据, 从而过滤或做异常处理比如截断, 或者可以考虑分段values, 例如key转化成key_1,key_2,key,3等, 或者可以key_value形式做相应处理。  

17.存在key层次的数据热点, 意味中不同key的hashcode shuffle到了同一节点上, 可以通过反转key来打散热点.  

