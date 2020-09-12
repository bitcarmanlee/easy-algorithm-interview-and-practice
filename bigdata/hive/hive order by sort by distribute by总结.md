mysql中有order by函数，而且是使用频率相当高的一个函数。之前看过一个数据，说计算机25%的工作量都用在排序上面（数据的真伪性没有考证）。从这也就不难看出为什么数据库里order by的操作这么重要了。  


hive中除了order by以外，还有sort by。这两有什么区别，跟mysql里的order by又有些什么不同，本博主结合实际使用场景，跟大家稍微絮叨絮叨。  

## 1.order by的使用方式
order by的使用上与mysql最大的不同，请看以下sql语句：  

```
select cardno,count(*)
from tableA
group by idA
order by count(*) desc limit 10
```  

这个语句在mysql中查询的时候，肯定是没有问题的，而且我们实际上也经常这么干。但是如果将上述语句提交给hive，会报以下错误：  

```
FAILED: SemanticException [Error 10128]: Line 4:9 Not yet supported place for UDAF 'count'
```  

怎么样可以呢？将count(*)给一个别名就好：  

```
select cardno,count(*) as num
from tableA
group by idA
order by num desc limit 10
```  

这样就可以了。本博主没查源码，估计是因为hive查询的时候起的是mr任务，mr任务里排序的时候，不认得count(*)是什么东东，所以给个别名就好。  

## 2.order by处理大数据量时候的无力

```
select col1,col2...
from tableA
where condition
order by col1,col2 desc(or asc)
```  

上述sql按col1,col2排序。不过order by是做全局排序，全局排序就意味着在reduce端进行操作的时候，只能有一个reduce。不管如何配置，只能有一个reduce。那当数据量很大的时候，这个reduce就成为了单点，速度会很慢很慢。。。  

## 3.distribute by sort by配合select top N
distribute by，顾名思义，是起分散数据作用的。distribute by col，则是按照col列为key分散到不同的reduce里去，默认采取的是hash算法。  

看到这里，大家有没有似曾相识的感觉？是不是跟group by很像呢？其实他两是很像的。唯一的区别，是distribute by只是分发数据到reduce，而group by将数据分发完以后，后面必须只能跟count,sum,avg等聚合操作。  

sort by是局部排序，只确保每个reduce上输出的数据为有序。当然如果只有一个reduce的时候，跟order by是一样的。。。  
如果我们想取top 10，完全可以用sort by代替order by。请看:  

```
select idA from tableA sort by idA limit 10
```  

将代码提交上去，首先会有如下输出：  

```
Total jobs = 2
Launching Job 1 out of 2
Number of reduce tasks not specified. Defaulting to jobconf value of: 5
```  

由此可见，reduce的数量不是编译sql时候确定的，而是根据我们之前指定的reduce数确定的。如果没指定，则是根据输入文件大小动态确定。  

对比order by  

```
select idA from tableA order by idA limit 10
```  
输出如下：  

```
Total jobs = 1
Launching Job 1 out of 1
Number of reduce tasks determined at compile time: 1
```  
由此可见，order by的reduce数是在编译期间就确定为1了。  

再看看sort by 的执行计划：  

```
explain select idA from tableA sort by idA limit 10
```

```
STAGE DEPENDENCIES:
  Stage-1 is a root stage
  Stage-2 depends on stages: Stage-1
  Stage-0 is a root stage

STAGE PLANS:
  Stage: Stage-1
    Map Reduce
      Map Operator Tree:
          TableScan
            alias: memberaddress
            Statistics: Num rows: 48553436 Data size: 388427488 Basic stats: COMPLETE Column stats: NONE
            Select Operator
              expressions: cardno (type: bigint)
              outputColumnNames: _col0
              Statistics: Num rows: 48553436 Data size: 388427488 Basic stats: COMPLETE Column stats: NONE
              Reduce Output Operator
                key expressions: _col0 (type: bigint)
                sort order: +
                Statistics: Num rows: 48553436 Data size: 388427488 Basic stats: COMPLETE Column stats: NONE
                value expressions: _col0 (type: bigint)
      Reduce Operator Tree:
        Extract
          Statistics: Num rows: 48553436 Data size: 388427488 Basic stats: COMPLETE Column stats: NONE
          Limit
            Number of rows: 10
            Statistics: Num rows: 10 Data size: 80 Basic stats: COMPLETE Column stats: NONE
            File Output Operator
              compressed: false
              table:
                  input format: org.apache.hadoop.mapred.SequenceFileInputFormat
                  output format: org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat
                  serde: org.apache.hadoop.hive.serde2.lazybinary.LazyBinarySerDe

Stage: Stage-2
    Map Reduce
      Map Operator Tree:
          TableScan
            Reduce Output Operator
              key expressions: _col0 (type: bigint)
              sort order: +
              Statistics: Num rows: 10 Data size: 80 Basic stats: COMPLETE Column stats: NONE
              value expressions: _col0 (type: bigint)
      Reduce Operator Tree:
        Extract
          Statistics: Num rows: 10 Data size: 80 Basic stats: COMPLETE Column stats: NONE
          Limit
            Number of rows: 10
            Statistics: Num rows: 10 Data size: 80 Basic stats: COMPLETE Column stats: NONE
            File Output Operator
              compressed: false
              Statistics: Num rows: 10 Data size: 80 Basic stats: COMPLETE Column stats: NONE
              table:
                  input format: org.apache.hadoop.mapred.TextInputFormat
                  output format: org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat
                  serde: org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe

  Stage: Stage-0
    Fetch Operator
      limit: 10
```  

根据执行计划很容易看出：相对于order by的一个job，sort by起了有两个job。第一个job现在每个reduce内部做局部排序，取top10。假设job1起了M个reduce，则第二个job再对M个reduce的输出做排序，但此时输入的数据量只有M*10条，最后取前10条，就得到了我们要的top10。这样与order by的全局排序相比，如果数据量很大的话，效率将大大提高。  


## 4.distribute by 与sort by配合使用

```
hive (test)> select * from sort_by_test;
OK
1	10
1	20
2	10
2	20
2	30
3	10
3	15
3	40
3	20
```  

```
hive (test)> desc sort_by_test;
OK
id                  	string
age                 	string
```  

表中有id与age两个字段。  

```
hive (test)> set mapred.reduce.tasks=2;
hive (test)> select * from sort_by_test
           > sort by id;
```  

结果如下：  

```
1	10
2	30
2	20
2	10
3	40
1	20
3	20
3	15
3	10
```  

```
hive (test)> set mapred.reduce.tasks=2;
hive (test)> select * from sort_by_test
           > distribute by id
           > sort by id;
```  

```
2	30
2	20
2	10
1	20
1	10
3	20
3	40
3	15
3	10
```  

两个语句对比，很容易看出，加上distribute by以后，distribute by后面的col相同的值都被分配到了同一个reduce里。  