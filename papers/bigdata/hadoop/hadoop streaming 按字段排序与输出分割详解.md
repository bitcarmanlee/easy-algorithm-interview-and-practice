## 1.默认情况
在hadoop streaming的默认情况下，是以"\t"作为分隔符的。对于标准输入来说，每行的第一个"\t" 以前的部分为key，其他部分为对应的value。如果一个"\t"字符没有，则整行都被当做key。这个<key,value>即是map阶段的输出，也是reduce阶段的输入。  

## 2.map阶段的sort与partition
map阶段很重要的阶段包括sort与partition。排序是按照key来进行的。咱们之前讲了默认的key是由"\t"分隔得到的。我们能不能自己控制相关的sort与partition呢？答案是可以的。  

先看以下几个参数：  
map.output.key.field.separator： map中key内部的分隔符  
num.key.fields.for.partition： 分桶时，key按前面指定的分隔符分隔之后，用于分桶的key占的列数。通俗地讲，就是partition时候按照key中的前几列进行划分，相同的key会被打到同一个reduce里。  
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner 前两个参数，要配合partitioner选项使用！  

stream.map.output.field.separator： map中的key与value分隔符  
stream.num.map.output.key.fields： map中分隔符的位置  
stream.reduce.output.field.separator： reduce中key与value的分隔符  
stream.num.reduce.output.key.fields： reduce中分隔符的位置  

## 3.分桶测试实例
准备数据：  

```
$ cat tmp
1,2,1,1,1
1,2,2,1,1
1,3,1,1,1
1,3,2,1,1
1,3,3,1,1
1,2,3,1,1
1,3,1,1,1
1,3,2,1,1
1,3,3,1,1
```  

上传到hdfs中。  

```
cat mapper.sh
#!/bin/bash

cat
```  

```
$ cat reducer.sh
#!/bin/bash

sort
```  

```
#!/bin/bash

streaming=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.5.0-cdh5.2.0.jar

output=/tmp/wanglei/part_out

if hadoop fs -test -d $output
then
    hadoop fs -rm -r $output
fi

hadoop jar $streaming \
    -D map.output.key.field.separator=, \
    -D num.key.fields.for.partition=2 \
    -D stream.reduce.output.field.separator=, \
    -D stream.num.reduce.output.key.fields=4 \
    -D mapred.reduce.tasks=2 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -input /tmp/wanglei/partition \
    -output $output \
    -mapper "sh mapper.sh" \
    -reducer "sh reducer.sh" \
    -file mapper.sh \
    -file reducer.sh
```  

代码最后的运行结果：  

```
$ hadoop fs -cat /tmp/wanglei/part_out/part-00000
1,3,1,1	1
1,3,1,1	1
1,3,2,1	1
1,3,2,1	1
1,3,3,1	1
1,3,3,1	1


$ hadoop fs -cat /tmp/wanglei/part_out/part-00001
1,2,1,1	1
1,2,2,1	1
1,2,3,1	1
```  

稍微解释一下输出：  
1.map阶段，key是按逗号分隔的，partition的阶段取前两个字段，所以前两个字段相同的key都被打到同一个reduce里。这一点从reduce的两个文件结果中就能看出来。  

2.reduce阶段通过stream.reduce.output.field.separator指定分隔符为","，通过stream.num.reduce.output.key.fields指定前4个字段为key，所以才会有最终的结果。  

需要注意的几个小点：  
1.之前写的代码，当分发的文件有多个的时候，可以用-files指定。但是加了上面的参数以后，再用-files会报错。具体原因未知。  
2.-file 参数必须写在最后面。如果写在-input前面，代码也会报错。具体原因暂时也未知。  
3.-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner参数必须指定，否则代码没法输出预期结果。  

## 4.map阶段输出测试实例
stream.map.output.field.separator与stream.num.map.output.key.fields与上面partition一组参数指定map输出格式是一致的。不一样的地方在stream这组参数是真正用于map端的输出，而partition那组参数是用于分桶！  

看下测试代码就清楚了：  

```
#!/bin/bash

streaming=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.5.0-cdh5.2.0.jar

output=/tmp/wanglei/part_out_map

if hadoop fs -test -d $output
then
    hadoop fs -rm -r $output
fi

hadoop jar $streaming \
    -D stream.map.output.field.separator=, \
    -D stream.num.map.output.key.fields=2 \
    -input /tmp/wanglei/partition \
    -output $output \
    -mapper "sh mapper.sh" \
    -file mapper.sh
```  

```
$ hadoop fs -cat /tmp/wanglei/part_out_map/*
1,2	3,1,1
1,2	2,1,1
1,2	1,1,1
1,3	3,1,1
1,3	2,1,1
1,3	1,1,1
1,3	3,1,1
1,3	2,1,1
1,3	1,1,1
```  

将reducer部分去掉，只输出mapper的结果。可以看出：  
1.mapper阶段输出的k,v以"\t"分隔（框架默认)  
2.mapper阶段以","分隔，key占了两个字段。  
3.mapper阶段按key排序，所以1,2开头的数据在前，1,3开头的数据在后！  