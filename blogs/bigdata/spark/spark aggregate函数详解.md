aggregate算是spark中比较常用的一个函数，理解起来会比较费劲一些，现在通过几个详细的例子带大家来着重理解一下aggregate的用法。  

## 1.先看看aggregate的函数签名
在spark的源码中，可以看到aggregate函数的签名如下：  

```
def aggregate[U: ClassTag](zeroValue: U)(seqOp: (U, T) => U, combOp: (U, U) => U): U
```  

可以看出，这个函数是个柯里化的方法，输入参数分为了两部分：`(zeroValue: U)`与`(seqOp: (U, T) => U, combOp: (U, U) => U)`  

## 2.aggregate的用法
函数签名比较复杂，可能有的小伙伴看着就晕菜了。别捉急，我们再来看看函数前面的注释，关于此函数的用法我们就会比较清楚。  

```
  /**
   * Aggregate the elements of each partition, and then the results for all the partitions, using
   * given combine functions and a neutral "zero value". This function can return a different result
   * type, U, than the type of this RDD, T. Thus, we need one operation for merging a T into an U
   * and one operation for merging two U's, as in scala.TraversableOnce. Both of these functions are
   * allowed to modify and return their first argument instead of creating a new U to avoid memory
   * allocation.
   *
   * @param zeroValue the initial value for the accumulated result of each partition for the
   *                  `seqOp` operator, and also the initial value for the combine results from
   *                  different partitions for the `combOp` operator - this will typically be the
   *                  neutral element (e.g. `Nil` for list concatenation or `0` for summation)
   * @param seqOp an operator used to accumulate results within a partition
   * @param combOp an associative operator used to combine results from different partitions
   */
```  

翻译过来就是：aggregate先对每个分区的元素做聚集，然后对所有分区的结果做聚集，聚集过程中，使用的是给定的聚集函数以及初始值"zero value"。这个函数能返回一个与原始RDD不同的类型U，因此，需要一个合并RDD类型T到结果类型U的函数，还需要一个合并类型U的函数。这两个函数都可以修改和返回他们的第一个参数，而不是重新新建一个U类型的参数以避免重新分配内存。  

参数zeroValue：`seqOp`运算符的每个分区的累积结果的初始值以及`combOp`运算符的不同分区的组合结果的初始值 - 这通常将是初始元素（例如“Nil”表的列表 连接或“0”表示求和）  
参数seqOp： 每个分区累积结果的聚集函数。  
参数combOp： 一个关联运算符用于组合不同分区的结果  

## 3.求平均值

看来了上面的原理介绍，接下来我们看干货。  
首先可以看网上最多的一个例子：  

```
val list = List(1,2,3,4,5,6,7,8,9)
val (mul, sum, count) = sc.parallelize(list, 2).aggregate((1, 0, 0))(
	(acc, number) => (acc._1 * number, acc._2 + number, acc._3 + 1),
	(x, y) => (x._1 * y._1, x._2 + y._2, x._3 + y._3)
        )
    (sum / count, mul)
```  

在常见的求均值的基础上稍作了变动，sum是求和，count是累积元素的个数，mul是求各元素的乘积。  
解释一下具体过程：  
1.初始值是(1, 0 ,0)  
2.number是函数中的T，也就是List中的元素，此时类型为Int。而acc的类型为(Int, Int, Int)。acc._1 * num是各元素相乘(初始值为1)，acc._2 + number为各元素相加。  
3.sum / count为计算平均数。  

## 4.另外的例子
为了加深理解，看另外一个的例子。  

```
		val raw = List("a", "b", "d", "f", "g", "h", "o", "q", "x", "y")
        val (biggerthanf, lessthanf) = sc.parallelize(raw, 1).aggregate((0, 0))(
            (cc, str) => {
                var biggerf = cc._1
                var lessf = cc._2
                if (str.compareTo("f") >= 0) biggerf = cc._1 + 1
                else if(str.compareTo("f") < 0) lessf = cc._2 + 1
                (biggerf, lessf)
            },
            (x, y) => (x._1 + y._1, x._2 + y._2)
        )
```  

这个例子中，我们想做的就是统计一下在raw这个list中，比"f"大与比"f"小的元素分别有多少个。代码本身的逻辑也比较简单，就不再更多解释。  

## 5.aggregateByKey与combineByKey的比较
aggregate是针对序列的操作，aggregateByKey则是针对k,v对的操作。顾名思义，aggregateByKey则是针对key做aggregate操作。spark中函数的原型如下：  

```
  def aggregateByKey[U: ClassTag](zeroValue: U)(seqOp: (U, V) => U,
      combOp: (U, U) => U): RDD[(K, U)] = self.withScope {
    aggregateByKey(zeroValue, defaultPartitioner(self))(seqOp, combOp)
  }
```  

都是针对k,v对的操作，spark中还有一个combineByKey的操作：  

```
  def combineByKey[C](
      createCombiner: V => C,
      mergeValue: (C, V) => C,
      mergeCombiners: (C, C) => C): RDD[(K, C)] = self.withScope {
    combineByKeyWithClassTag(createCombiner, mergeValue, mergeCombiners)(null)
  }
```  

为了看清楚两个的联系，我们再看看 aggregateByKey里面的真正实现：  

```
  def aggregateByKey[U: ClassTag](zeroValue: U, partitioner: Partitioner)(seqOp: (U, V) => U,
      combOp: (U, U) => U): RDD[(K, U)] = self.withScope {
    // Serialize the zero value to a byte array so that we can get a new clone of it on each key
    val zeroBuffer = SparkEnv.get.serializer.newInstance().serialize(zeroValue)
    val zeroArray = new Array[Byte](zeroBuffer.limit)
    zeroBuffer.get(zeroArray)

    lazy val cachedSerializer = SparkEnv.get.serializer.newInstance()
    val createZero = () => cachedSerializer.deserialize[U](ByteBuffer.wrap(zeroArray))

    // We will clean the combiner closure later in `combineByKey`
    val cleanedSeqOp = self.context.clean(seqOp)
    combineByKeyWithClassTag[U]((v: V) => cleanedSeqOp(createZero(), v),
      cleanedSeqOp, combOp, partitioner)
  }
```  

从上面这段源码可以清晰看出，aggregateByKey调用的就是combineByKey方法。seqOp方法就是mergeValue，combOp方法则是mergeCombiners，cleanedSeqOp(createZero(), v)是createCombiner, 也就是传入的seqOp函数, 只不过其中一个值是传入的zeroValue而已！  

因此, 当createCombiner和mergeValue函数的操作相同, aggregateByKey更为合适！  