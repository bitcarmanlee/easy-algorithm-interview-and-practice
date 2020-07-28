## 1.求key的平均值
k,v结构的数据中，求每个key对应的平均值，在spark中怎么应该怎么求？  
例如有如下的数据:  

```
("a",10)
("b",4)
("a",10)
("b",20)
```  

想求a,b对应的平均值。  
直接上代码  

```
sc.parallelize(List(("a",10),("b",4),("a",10),("b",20))).mapValues(x => (x, 1)).reduceByKey((x, y) => (x._1 + y._1, x._2 + y._2)).mapValues(x => (x._1, x._2, x._1.toDouble / x._2.toDouble)).collect()
```  

在spark-shell中运行上述的代码以后，输出如下：  

```
Array[(String, (Int, Int, Double))] = Array((a,(20,2,10.0)), (b,(24,2,12.0)))
```  

简单分析一下上面的代码逻辑：  
`mapValues`是`PairRDDFunctions`中的方法，顾名思义，是对kv结构的rdd的value进行map的操作。  
然后进行`reduceByKey`操作，此时将value中的值累加，对应出现的次数也累加。  
最后再调用`mapValues`方法，求每个key的平均值即可。  

## 2.求key对应的value值的占比
同样是上面的数据，我们想求a,b对应的value值分别占比是多少，该怎么计算？  

```
val array = sc.parallelize(List(("a",10),("b",4),("a",10),("b",20))).reduceByKey(_ + _).collect()
val sum = array.foldLeft(0)({ (z, f) => z + f._2 })
array.map(x =>  println("%s\t%s\t%s".format(x._1, x._2, x._2.toDouble / sum)))
```  

在spark-shell中运行上述的代码以后，输出如下：  

```
a	20	0.45454545454545453
b	24	0.5454545454545454
```  

上面代码的逻辑如下：  
1.先用`reduceByKey`根据key聚合。  
2.用`foldLeft`方法算出所有key的总和。  
3.对包含所有key的数组进行遍历，得到各个key的占比。  

## 3.foldLeft的简单讲解
上面用到了`foldLeft`函数。从本质上来讲，fold函数是将一种格式的输入数据转化为另外一种格式返回。  
`foldLeft`的原型如下：  

```
  override /*TraversableLike*/
  def foldLeft[B](z: B)(op: (B, A) => B): B =
    foldl(0, length, z, op)
```  
`foldLeft`有两个输入参数：初始值以及一个函数。而这个函数也包含有两个输入参数：累加值z与`TraversableLike`的当前item。  
`foldLeft`方法开始运行以后，步骤如下：  
1.初始值0作为第一个参数传入foldLeft，array中的第一个item作为第二个参数f传入foldLeft中。  
2.foldLeft对两个参数进行计算，上面的例子是将参数相加并返回。  
3.foldLeft将上一步返回的值作为输入函数的第一个参数，并且把array的下面一个item作为第二个参数传入继续计算。  
4.重复上面的步骤，直到遍历完array中的所有item。  