我们在做数据统计与分析的时候，经常会遇到K-V结构的数据，所以处理这种K-V结构的数据也是非常常见的需求。在Spark中，除了原生的RDD天然有这种K,V结构，API中也包含有javaPairRdd,PairwiseRdd等对应的接口。而对于KV结构的数据处理就有很多种情况了，例如像数据库的group by操作等。今天我们就来说说在spark中一个常用的操作：combineByKey  

## 1.combineByKey函数原型

```
  /**
   * Simplified version of combineByKeyWithClassTag that hash-partitions the resulting RDD using the
   * existing partitioner/parallelism level. This method is here for backward compatibility. It
   * does not provide combiner classtag information to the shuffle.
   *
   * @see [[combineByKeyWithClassTag]]
   */
  def combineByKey[C](
      createCombiner: V => C,
      mergeValue: (C, V) => C,
      mergeCombiners: (C, C) => C): RDD[(K, C)] = self.withScope {
    combineByKeyWithClassTag(createCombiner, mergeValue, mergeCombiners)(null)
  }
```  

可以看出，combineByKey是典型的K-V类型的算子，而且是一个transformation操作。与其他transformation操作一样，combineByKey也不会触发作业的提交。combineByKey函数主要有三个参数，而且这三个参数都是函数：  
```
createCombiner: V => C 产生一个combiner的函数，将RDD[K,V]中的V转换成一个新的值C1
mergeValue: (C, V) => C 合并value的函数，将一个C1类型的值与一个V合并成一个新的C类型的值，假设这个新的C类型的值为C2
mergeCombiners: (C, C) => C) 将两个C类型的值合并为一个C类型的值
```

整个函数最后的输出为RDD[(K, C)]  

## 2.看个实际例子
假设hdfs上有个文本，文本有两列：第一列为city城市名，第二列为用户标识uuid，现在想统计每个城市有多少UV并排序，用combineByKey就可以实现上述需求。源码如下：    

```
    def t1(sc: SparkContext) = {
        val inputpath = "XXX"
        sc.textFile(inputpath).
            filter { x =>
                val lines = x.split("\t")
                lines.length == 2 && lines(1).length > 0
            }
            .map { x =>
                val lines = x.split("\t")
                val (city, uuid) = (lines(0), lines(1))
                (city, uuid)
            }
            .combineByKey((v: String) => {
                val set = new java.util.HashSet[String]()
                set.add(v)
                set
            },
                (x: java.util.HashSet[String], v: String) => {
                    x.add(v)
                    x
                },
                (x: java.util.HashSet[String], y: java.util.HashSet[String]) => {
                    x.addAll(y)
                    x
                })
            .map(x => (x._1, x._2.size()))
            .sortBy(_._2, false)
            .take(10)
            .foreach(println)
    }
```  

代码详解：  

1.

```
(v: String) => {
                val set = new java.util.HashSet[String]()
                set.add(v)
                set
```  
这个函数表示对于每一个city第一次出现的时候，先new一个hashset，并把此时的uuid加入到hashset中。  

2.  

```
(x: java.util.HashSet[String], v: String) => {
                    x.add(v)
                    x
                }
```  
这个表示将每一个uuid都merge到已有的combiner中。  

3.  

```
 (x: java.util.HashSet[String], y: java.util.HashSet[String]) => {
                    x.addAll(y)
                    x
                }
```  
最后一个函数表示将所有city对应的uuid的hashset合并，得到的就是每个city的所有uuid集合，达到了我们最终的目的！  