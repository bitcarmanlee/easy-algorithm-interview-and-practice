HBase是三维有序存储的，三维指的是：RowKey(行健)、column key(columnFamily和qualifier)、TimeStamp(时间戳)，通过这三个维度我们可以对HBase中的数据进行快速定位。下面我们主要来讨论RowKey的设计原则：  

HBase中RowKey可以唯一标识一条记录，在HBase查询的时候，我们有两种方式，第一种是通过get()方法指定RowKey条件后获取唯一一条记录，第二种方式是通过scan()方法设置诸如startRow和endRow的参数进行范围匹配查找。所以说RowKey的设计至关重要，严重影响着查询的效率， RowKey的设计 主要是遵循以下几个原则：  

1)、RowKey长度原则：RowKey是一个二进制码流，可以是任意字符串，最大长度为64KB，实际应用中一般为10~100bytes，存为byte[]字节数组，一般设计成定长。建议是越短越好，不要超过16个字节。原因一是数据的持久化文件HFile中是按照KeyValue存储的，如果RowKey过长比如100字节，1000万列数据光RowKey就要占用100*1000万=10亿个字节，将近1G数据，这会极大影响HFile的存储效率；原因二是memstore将缓存部分数据到内存，如果RowKey字段过长内存的有效利用率会降低，系统将无法缓存更多的数据，这会降低检索效率。因此RowKey的字节长度越短越好原因三是目前操作系统大都是64位，内存8字节对齐。控制在16个字节，8字节的整数倍利用操作系统的最佳特性。  

2)、RowKey散列原则：如果RowKey是按时间戳的方式递增，不要将时间放在二进制码的前面，建议将RowKey的高位作为散列字段，由程序循环生成，低位放时间字段，这样将提高数据均衡分布在每个RegionServer实现负载均衡的几率，如果没有散列字段，首字段直接是时间信息，将产生所有数据都在一个RegionServer上堆积的热点现象，这样在做数据检索的时候负载将会集中在个别RegionServer，降低查询效率。  

3)、RowKey唯一原则：必须在设计上保证其唯一性。  

RowKey是按照字典排序存储的，因此，设计RowKey时候，要充分利用这个排序特点，将经常一起读取的数据存储到一块，将最近可能会被访问的数据放在一块。  

举个例子：如果最近写入HBase表中的数据是最可能被访问的，可以考虑将时间戳作为RowKey的一部分，由于是字段排序，所以可以使用Long.MAX_VALUE-timeStamp作为RowKey，这样能保证新写入的数据在读取时可以别快速命中。  

案例分析：  

用户订单列表查询RowKey设计。  

## 需求场景

某用户根据查询条件查询历史订单列表  

## 查询条件

开始结束时间(orderTime)-----必选,  

订单号(seriaNum),  

状态(status)，游戏号(gameID)  

## 结果显示要求

结果按照时间倒序排列。    


## 解答

RowKey可以设计为：  
```
userNum$orderTime$seriaNum
```  

注：这样设计已经可以唯一标识一条记录了，订单详情都是可以根据订单号seriaNum来确定。在模糊匹配查询的时候startRow和endRow只需要设置到userNum$orderTime即可，如下：  

startRow=userNum$maxvalue-stopTime  

endRow=userNum$maxvalue-startTime  

其他字段用filter实现。  

本文转载自：
http://blog.csdn.net/lzm1340458776/article/details/44941953