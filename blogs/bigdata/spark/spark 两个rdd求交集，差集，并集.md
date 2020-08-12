## 1.前言
spark中两个rdd，经常需要做交集，差集，并集等操作。好比任何一门编程语言中两个集合，交并差也是常见的需求。现在我们看看在spark中怎么实现两个rdd的这种操作。  
为了方便看到结果，在spark shell中测试如下代码。  

先生成两个rdd  

```
scala> val rdd1 = sc.parallelize(List("a", "b","c"))
rdd1: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[5] at parallelize at <console>:27

scala> val rdd2 = sc.parallelize(List("e", "d","c"))
rdd2: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[6] at parallelize at <console>:27
```  

生成了两个rdd，分别为rdd1与rdd2，然后开始测试。  

## 2.求并集，union操作
如果是要求并集，用union操作即可。  

```
scala> rdd1.union(rdd2).collect
...
res5: Array[String] = Array(a, b, c, e, d, c)
```  

可以看出，union的结果是没有去重的，就是将rdd1与rdd2的元素放一块。  
有的小伙伴说我就要去重，那怎么办。很简单，distinct嘛。  

```
scala> rdd1.union(rdd2).distinct.collect
...
res6: Array[String] = Array(a, b, c, d, e)
```  

## 3.求交集，intersection操作
求两个交集也是常见的需求。很简单，用intersection操作就可以了。  

```
scala> rdd1.intersection(rdd2).collect
...
res7: Array[String] = Array(c)

scala> rdd2.intersection(rdd1).collect
...
res9: Array[String] = Array(c)
```  

## 4.求差集，subtract
subtract的方法原型为：  

```
def subtract(other: RDD[T]): RDD[T]
```  

该函数类似于intersection，返回在RDD中出现，并且不在otherRDD中出现的元素，不去重。  

```
scala> rdd1.subtract(rdd2).collect
...
res10: Array[String] = Array(a, b)

scala> rdd2.subtract(rdd1).collect
...
res11: Array[String] = Array(d, e)
```  

这几个方法都很实用，使用起来也简单快捷，希望能对大家有所帮助。  