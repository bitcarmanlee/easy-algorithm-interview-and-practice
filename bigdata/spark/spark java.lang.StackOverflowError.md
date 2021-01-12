## 1.遇到的问题
在实际分析数据过程中，需要拉取最近一年的数据进行统计，并且一年的数据按天分区。  

```
val ymdSet = TimeUtils.genYmdSet(beginYmd, endYmd) // 获取过去一年时间的日期
var rdd = SparkIo.readThriftParquetFile(spark.sparkContext, pathxxx, classOf[xxx]) 

for(eachYmd <- ymdSet) {
  val tmppath = PathUtils.xxx + eachYmd
  val tmprdd = SparkIo.readThriftParquetFile(spark.sparkContext, tmppath, classOf[xxx])

  rdd = rdd.union(tmprdd)
}

rdd
```  

上面的代码逻辑比较清晰：按照每天的数据生成一个临时的rdd，然后将该rdd不停union到最初的rdd上，得到最终一年的数据。  

当只选择过去7天的数据进行分析的时候，上面的代码没有问题可以正常运行。当代码读取的数据变为过去一整年时，会抛出异常  

```
ERROR executor.Executor: Exception in task 28.0 in stage 0.0 (TID 28)
java.lang.StackOverflowError
        at java.lang.Exception.<init>(Exception.java:102)
        at java.lang.ReflectiveOperationException.<init>(ReflectiveOperationException.java:89)
        at java.lang.reflect.InvocationTargetException.<init>(InvocationTargetException.java:72)
        at sun.reflect.GeneratedSerializationConstructorAccessor13.newInstance(Unknown Source)
        at java.lang.reflect.Constructor.newInstance(Constructor.java:526)
        at java.io.ObjectStreamClass.newInstance(ObjectStreamClass.java:967)
        at java.io.ObjectInputStream.readOrdinaryObject(ObjectInputStream.java:1782)
        at java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1350)
        at java.io.ObjectInputStream.defaultReadFields(ObjectInputStream.java:1990)
        at java.io.ObjectInputStream.readSerialData(ObjectInputStream.java:1915)
        at java.io.ObjectInputStream.readOrdinaryObject(ObjectInputStream.java:1798)
        at java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1350)
        at java.io.ObjectInputStream.defaultReadFields(ObjectInputStream.java:1990)
        at java.io.ObjectInputStream.readSerialData(ObjectInputStream.java:1915)
        at java.io.ObjectInputStream.readOrdinaryObject(ObjectInputStream.java:1798)
        at java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1350)
        at java.io.ObjectInputStream.readArray(ObjectInputStream.java:1706)
        at java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1344)
        at java.io.ObjectInputStream.defaultReadFields(ObjectInputStream.java:1990)
        at java.io.ObjectInputStream.readSerialData(ObjectInputStream.java:1915)
        at java.io.ObjectInputStream.readOrdinaryObject(ObjectInputStream.java:1798)
        at java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1350)
        at java.io.ObjectInputStream.defaultReadFields(ObjectInputStream.java:1990)
        at java.io.ObjectInputStream.readSerialData(ObjectInputStream.java:1915)
        ......
        
```  

## 2.原因分析
从异常来看，是使用java.io.ObjectInputStream序列化的时候出现了死循环导致。  
结合前面的现象，7天数据的时候没问题，而一年的数据会有异常，主要是一年的数据文件量太大，导致栈空间不足。不停的union过程，导致了rdd的lineage太长，最终导致栈空间的不足。因为每执行一次union操作，就会给lineage的步长加1。  


## 3.解决方案
既然定位到了问题，那解决方案就出来了，无非是两种方式  
1.加大栈空间。  
2.减少lineage的长度。  

加大栈空间是个治标不治本的方案，因为集群的资源始终是有限的，而且一次处理太大的数据，始终是个隐患，所以最终采取了第二种方案，减少lineage长度。  

具体实施也比较简单  

```
def genrdd(startYmd: String, endYmd: String) = {
	val ymdSet = TimeUtils.genYmdSet(beginYmd, endYmd) // 获取过去一段时间的日期
	var rdd = SparkIo.readThriftParquetFile(spark.sparkContext, pathxxx, classOf[xxx]) 

	for(eachYmd <- ymdSet) {
  	val tmppath = PathUtils.xxx + eachYmd
  	val tmprdd = SparkIo.readThriftParquetFile(spark.sparkContext,tmppath,classOf[xxx])
  	
  	rdd = rdd.union(tmprdd)
}

rdd
}
```  

首先将生成rdd的逻辑封装成一个方法，方法的参数为起止时间。  
然后，将一年的时间段拆开，比如拆成4段，每段3个月，分别得到起止时间。  
最后，将该方法调用4次，最后union到一起，就可以成功将一年的数据合并。  
