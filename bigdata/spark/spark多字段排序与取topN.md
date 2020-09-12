## 1.多字段排序
前面介绍了[k,v]结构的rdd排序方法，下面来看更为复杂的情况，如果有更为复杂的多字段排序需求该怎么处理？  
比如有如下数据  

```
1 2
1 3
1 1
1 6
1 4
2 5
2 8
2 3
```  
我们现在想先对第一列逆序排，如果第一列相同再按第二列逆序排，该怎么办呢？  
以下两种方式都可以满足上面的需求  

### 1.1　定义SecondSortKey来实现  
首先我们定义一个SecondSortKey  
```
    class SecondSortKey(val first: Int, val second: Int) extends Ordered[SecondSortKey] with Serializable {
        override def compare(that: SecondSortKey): Int = {
            if (this.first -that.first == 0) {
                this.second - that.second
            } else {
                this.first - that.first
            }
        }
    }
```  

然后按如下方式即可实现：  

```
        val lines = sc.parallelize(Array((1, 2), (1, 3), (1, 1), (1, 6), (1, 4), (2, 5), (2, 8), (2, 3)))
        lines.map { x => (new SecondSortKey(x._1, x._2), x) }
            .sortByKey(ascending = false)
            .map(_._2)
            .collect()
```  

### 2.不新建对象，通过自定义Ordering来实现
首先我们在方法中定义隐变量ordering:  
```
        implicit val ordering = new Ordering[(Int, Int)] {
            override def compare(a: (Int, Int), b: (Int, Int)) = {
                var result = 0
                if (a._1 == b._1) {
                    result = a._2 - b._2
                } else {
                    result = a._1 - b._1
                }
                result
            }
        }
```  

然后按如下方式使用即可  

```
        val a = sc.parallelize(Array((1, 2), (1, 3), (1, 1), (1, 6), (1, 4), (2, 5), (2, 8), (2, 3)))
        a.map { x => (x, x) }.sortByKey(ascending = false).map(_._2).collect()
```  

## 2.取topN
还是上面的例子，比如我们要按第二列取top3  

```
a.sortBy(_._2, ascending = false).take(3)
```  


