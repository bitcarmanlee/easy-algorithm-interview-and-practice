日常工作中，排序是道绕过不过去的侃，我们每天都会面对各种各样的排序需求。那么在spark中如何排序呢？我们来看一些很有代表性的例子。

## 1.最简单的排序
假设有个`RDD[Int]`类型的数据，需要按数据大小进行排序，那这个排序算最简单的：  

```
sc.parallelize(Array(1,3,2,4,6,5)).sortBy(x => x).collect()
```  

代码运行的结果：  

```
 Array[Int] = Array(1, 2, 3, 4, 5, 6)
```  

## 2.kv结构的排序
在kv结构的数据中，按value排序是常见的需求：  

```
sc.parallelize(Array(("a", 1), ("c", 3), ("b", 2), ("d", 4))).sortBy(_._2)
```  
代码运行的结果：  

```
Array[(String, Int)] = Array((a,1), (b,2), (c,3), (d,4))
```  

## 3.定制排序规则
有如下结构的数据：  

```
<10 6094308
<100 234975
<20 2286079
<200 1336431
```  

希望按照<后面的数字大小排序，得到如下结果：  

```
<10 6094308
<20 2286079
<100 234975
<200 1336431
```  
代码如下：  

```
val array = Array(("<10",6094308), ("<100",234975), ("<20",2286079),("<200",1336431));
sc.parallelize(array).sortBy({item => item._1.substring(1, item._1.length).toInt}).collect()
```  

要理解上述代码的原理，我们需要分析一下`sortBy`的源码。  

```
  /**
   * Return this RDD sorted by the given key function.
   */
  def sortBy[K](
      f: (T) => K,
      ascending: Boolean = true,
      numPartitions: Int = this.partitions.length)
      (implicit ord: Ordering[K], ctag: ClassTag[K]): RDD[T] = withScope {
    this.keyBy[K](f)
        .sortByKey(ascending, numPartitions)
        .values
  }
```  

`sortBy`必需传入的一个参数为`f: (T) => K`，`T`为array中的元素类型。  

```
  /**
   * Creates tuples of the elements in this RDD by applying `f`.
   */
  def keyBy[K](f: T => K): RDD[(K, T)] = withScope {
    val cleanedF = sc.clean(f)
    map(x => (cleanedF(x), x))
  }
```  

传入的`f: (T) => K`作用在`keyBy`方法上，生成了一个`RDD[(K, T)]`的数据。  
然后调用`sortByKey`，最后取出里面的`T`，得到的就是原始array中的类型！  

## 4.用sortByKey实现上面的功能
我们再来看看`sortByKey`的源码   

```
  /**
   * Sort the RDD by key, so that each partition contains a sorted range of the elements. Calling
   * `collect` or `save` on the resulting RDD will return or output an ordered list of records
   * (in the `save` case, they will be written to multiple `part-X` files in the filesystem, in
   * order of the keys).
   */
  // TODO: this currently doesn't work on P other than Tuple2!
  def sortByKey(ascending: Boolean = true, numPartitions: Int = self.partitions.length)
      : RDD[(K, V)] = self.withScope
  {
    val part = new RangePartitioner(numPartitions, self, ascending)
    new ShuffledRDD[K, V, V](self, part)
      .setKeyOrdering(if (ascending) ordering else ordering.reverse)
  }
```  

大家看到`sortByKey`的源码可能会有疑惑，难道`sortByKey`不能指定排序方式么？不能像`sortBy`那样传入一个函数么？  
其实是可以的。`sortByKey`位于`OrderedRDDFunctions`类中，`OrderedRDDFunctions`中有一个隐藏变量：  

```
private val ordering = implicitly[Ordering[K]]
```  

我们重写这个变量以后，就可以改变排序规则。  
以第三部分的需求为例，我们用`sortByKey`可以这么做：  

```
implicit val sortByNum = new Ordering[String] { override def compare(x: String, y: String): Int = x.substring(1, x.length).toInt.compareTo(y.substring(1, y.length).toInt)};
val array = Array(("<10",6094308), ("<100",234975), ("<20",2286079),("<200",1336431));
sc.parallelize(array).sortByKey().collect()
```  
最后的输出结果为：  

```
Array[(String, Int)] = Array((<10,6094308), (<20,2286079), (<100,234975), (<200,1336431))
```  

同样达到了我们的目的！  