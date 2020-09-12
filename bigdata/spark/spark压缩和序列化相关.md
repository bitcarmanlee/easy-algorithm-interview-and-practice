## 1.spark.serializer
默认为org.apache.spark.serializer.JavaSerializer, 可选 org.apache.spark.serializer.KryoSerializer, 实际上只要是org.apache.spark.serializer的子类就可以了,不过如果只是应用,大概你不会自己去实现一个的。  

序列化对于spark应用的性能来说,还是有很大影响的,在特定的数据格式的情况下,KryoSerializer的性能可以达到JavaSerializer的10倍以上,当然放到整个Spark程序中来考量,比重就没有那么大了,但是以Wordcount为例，通常也很容易达到30%以上的性能提升。而对于一些Int之类的基本类型数据，性能的提升就几乎可以忽略了。KryoSerializer依赖Twitter的Chill库来实现，相对于JavaSerializer，主要的问题在于不是所有的Java Serializable对象都能支持。  

需要注意的是，这里可配的Serializer针对的对象是Shuffle数据，以及RDD Cache等场合，而Spark Task的序列化是通过spark.closure.serializer来配置，但是目前只支持JavaSerializer，所以等于没法配置啦。  

更多Kryo序列化相关优化配置,可以参考 http://spark.apache.org/docs/latest/tuning.html#data-serialization 一节  

## 2.spark.rdd.compress
这个参数决定了RDD Cache的过程中，RDD数据在序列化之后是否进一步进行压缩再储存到内存或磁盘上。当然是为了进一步减小Cache数据的尺寸，对于Cache在磁盘上而言，绝对大小大概没有太大关系，主要是考虑Disk的IO带宽。而对于Cache在内存中，那主要就是考虑尺寸的影响，是否能够Cache更多的数据，是否能减小Cache数据对GC造成的压力等。  

这两者，前者通常不会是主要问题，尤其是在RDD Cache本身的目的就是追求速度，减少重算步骤，用IO换CPU的情况下。而后者，GC问题当然是需要考量的，数据量小，占用空间少，GC的问题大概会减轻，但是是否真的需要走到RDD Cache压缩这一步，或许用其它方式来解决可能更加有效。  

所以这个值默认是关闭的，但是如果在磁盘IO的确成为问题或者GC问题真的没有其它更好的解决办法的时候，可以考虑启用RDD压缩。  

## 3.spark.broadcast.compress
是否对Broadcast的数据进行压缩，默认值为True。  

Broadcast机制是用来减少运行每个Task时，所需要发送给TASK的RDD所使用到的相关数据的尺寸，一个Executor只需要在第一个Task启动时，获得一份Broadcast数据，之后的Task都从本地的BlockManager中获取相关数据。在1.1最新版本的代码中，RDD本身也改为以Broadcast的形式发送给Executor（之前的实现RDD本身是随每个任务发送的），因此基本上不太需要显式的决定哪些数据需要broadcast了。    

因为Broadcast的数据需要通过网络发送，而在Executor端又需要存储在本地BlockMananger中，加上最新的实现，默认RDD通过Boradcast机制发送，因此大大增加了Broadcast变量的比重，所以通过压缩减小尺寸，来减少网络传输开销和内存占用，通常都是有利于提高整体性能的。  

什么情况可能不压缩更好呢，大致上个人觉得同样还是在网络带宽和内存不是问题的时候，如果Driver端CPU资源很成问题（毕竟压缩的动作基本都在Driver端执行），那或许有调整的必要。  

## 4.spark.io.compression.codec
RDD Cache和Shuffle数据压缩所采用的算法Codec，默认值曾经是使用LZF作为默认Codec，最近因为LZF的内存开销的问题，默认的Codec已经改为Snappy。    

LZF和Snappy相比较，前者压缩率比较高（当然要看具体数据内容了，通常要高20%左右），但是除了内存问题以外，CPU代价也大一些（大概也差20%~50%？）  

在用于Shuffle数据的场合下，内存方面，应该主要是在使用HashShuffleManager的时候有可能成为问题，因为如果Reduce分区数量巨大，需要同时打开大量的压缩数据流用于写文件，进而在Codec方面需要大量的buffer。但是如果使用SortShuffleManager，由于shuffle文件数量大大减少，不会产生大量的压缩数据流，所以内存开销大概不会成为主要问题。  

剩下的就是CPU和压缩率的权衡取舍，和前面一样，取决于CPU/网络/磁盘的能力和负载，个人认为CPU通常更容易成为瓶颈。所以要调整性能，要不不压缩，要不使用Snappy可能性大一些？  

对于RDD Cache的场合来说，绝大多数场合都是内存操作或者本地IO，所以CPU负载的问题可能比IO的问题更加突出，这也是为什么 spark.rdd.compress 本身默认为不压缩，如果要压缩，大概也是Snappy合适一些？  

原文链接地址：http://spark-config.readthedocs.io/en/latest/compress.html  