hive中的窗口函数，功能非常强大，使用也比较方便，可以给我们的查询提供相当多的遍历。下面就结合具体的需求与实例，一一为大家讲解窗口函数的使用方法。

## 1.数据准备
先在hive数据库中建一张表，表的结构如下：  

```
hive (tmp)> desc phone_test;
OK
calling_num         	string
called_num          	string
```  

准备测试文件：  

```
vim phone
130,131
130,131
130,131
130,131
130,131
130,131
130,132
130,132
130,133
130,133
130,134
132,130
132,130
132,130
132,130
132,130
132,131
132,131
132,131
132,133
132,133
132,133
134,135
134,135
134,135
134,135
134,136
134,136
134,136
138,137
138,137
138,137
138,136
138,136
135,130
135,130
135,130
135,130
135,132
135,132
```  

将文件put到hdfs中hive表对应的位置：  

```
hadoop fs -put phone /data/hive/warehouse/tmp.db/phone_test
```  

至此，数据准备工作完毕。  

## 2.row_num()方法，最有用的窗口函数，或许没有之一
表phone_test的第一列为主叫电话，第二列为被叫电话，我们经常有这种需求：对于同一主叫电话，按通话次数的多少（即被叫电话）进行排序。这个时候row_num()方法就派上了用场。请看：  

```
select a.calling_num,called_num,count,
row_number() OVER (distribute BY calling_num sort BY count DESC) rn
from
(select calling_num,called_num,count(*) as count
from phone_test group by calling_num,called_num)a

130	131	6	1
130	133	2	2
130	132	2	3
130	134	1	4
132	130	5	1
132	133	3	2
132	131	3	3
134	135	4	1
134	136	3	2
138	137	3	1
138	136	2	2
135	130	4	1
135	132	2	2
```  

最后一列，就是在同一主叫电话中，被叫电话与主叫电话通话次数的排序。怎么样，很方便吧。      
如果要取通话最多的那个，在此基础上稍作改动:  

```
select b.calling_num,called_num,count
from
(select a.calling_num,called_num,count,
row_number() OVER (distribute BY calling_num sort BY count DESC) rn
from
(select calling_num,called_num,count(*) as count
from phone_test group by calling_num,called_num)a)b
where b.rn = 1

130	131	6
132	130	5
134	135	4
138	137	3
135	130	4
```  

这样就把每组中rn=1的那一行给选了出来。  

换一种写法，还可以这么写：  

```
select b.calling_num,called_num,count
from
(select a.calling_num,called_num,count,
row_number() OVER (partition BY calling_num order BY count DESC) rn
from
(select calling_num,called_num,count(*) as count
from phone_test group by calling_num,called_num)a)b
where b.rn = 1

130	131	6
132	130	5
134	135	4
138	137	3
135	130	4
```  

效果与前面是一样一样滴！  

##3.rank() dense_rank()
rank，顾名思义，就是排序啦。这个比排序更高级一点的是，返回的数据项是在分组中的排名，排名相等的会在名词中留下对应的空位。而dense_rank与rank唯一的不同，就是排名相等的时候不会留下对应的空位。
看例子：  

```
select a.calling_num,called_num,count,
rank() over (partition by calling_num order by count desc) rank,
dense_rank() over (partition by calling_num order by count desc) drank,
row_number() OVER (distribute BY calling_num sort BY count DESC) rn
from
(select calling_num,called_num,count(*) as count
from phone_test group by calling_num,called_num)a

对应结果的列为：calling_num called_num count rank drank rn
130	131	6	1	1	1
130	133	2	2	2	2
130	132	2	2	2	3
130	134	1	4	3	4
132	130	5	1	1	1
132	133	3	2	2	2
132	131	3	2	2	3
134	135	4	1	1	1
134	136	3	2	2	2
138	137	3	1	1	1
138	136	2	2	2	2
135	130	4	1	1	1
135	132	2	2	2	2
```  

聪明的你，是不是已经明白这两个函数的用法了？  

## 4.ntile()
ntile是按层次查询。其作用是将数据分成几部分，例如我们想把数据总共分为十份，我们想取前10%来做分析。请看:  

```
select calling_num,called_num,count(*),ntile(5) over(order by count(*) desc) til
from phone_test group by calling_num,called_num
130	131	6	1
132	130	5	1
135	130	4	1
134	135	4	2
138	137	3	2
132	133	3	2
132	131	3	3
134	136	3	3
138	136	2	3
130	132	2	4
135	132	2	4
130	133	2	5
130	134	1	5
```  

我们先将所有数据分为了5部分。如果只想查看其中某一部分：  

```
select a.calling_num,a.called_num,count,til from
(select calling_num,called_num,count(*) count,ntile(5) over(order by count(*) desc) til
from phone_test group by calling_num,called_num)a
where til = 1

130	131	6	1
132	130	5	1
135	130	4	1
```  

## 5.一定范围内的聚合
实际应用场景中，我们有各种数据聚合的要求，而且还比一般的计算要复杂。例如对与电商来说，经常需要看当月与今年之前所有月的累计订单量。对于销售人员来说，也经常需要看当月与今年之前或这个季度之前的累计销售额。对于本文中的例子，我们想计算当前号码的通话总和，以及与之前所有号码通话总和的累计：  

```
select calling_num,sum(num),
sum(sum(num)) over(order by calling_num ROWS between unbounded preceding and current row) as cumulative_sum
from
(select calling_num,called_num,count(*) as num
from phone_test group by calling_num,called_num)a
group by calling_num

130	11	11
132	11	22
134	7	29
135	6	35
138	5	40
```  

sum(sum(num))这种写法中，里面的sum(num)表示需要累加的和。  
重点看下over里面的内容：  
order by calling_num表示按主叫电话排序  
ROWS between unbounded preceding and current row 肯定就是表示聚合的起始位置与终止位置了。unbounded preceding是起点，表示从第一行开始；current row为默认值，表示到当前行。
以下写法，能达到同样的效果：  

```
select calling_num,sum(num),
sum( sum(num)) over(order by calling_num ROWS unbounded preceding) as cumulative_sum
from
(select calling_num,called_num,count(*) as num
from phone_test group by calling_num,called_num)a
group by calling_num

130	11	11
132	11	22
134	7	29
135	6	35
138	5	40
```  

如果只想在当前行对前两行聚合，总共计算前两行+当前行=3行的值，可以这样写：  

```
select calling_num,sum(num),
sum( sum(num)) over(order by calling_num ROWS between 2 preceding and current row) as cumulative_sum
from
(select calling_num,called_num,count(*) as num
from phone_test group by calling_num,called_num)a
group by calling_num

130	11	11
132	11	22
134	7	29
135	6	24
138	5	18
```  

也可以这么写：  

```
select calling_num,sum(num),
sum( sum(num)) over(order by calling_num ROWS 2 preceding) as cumulative_sum
from
(select calling_num,called_num,count(*) as num
from phone_test group by calling_num,called_num)a
group by calling_num

130	11	11
132	11	22
134	7	29
135	6	24
138	5	18
```  

如果想对之前一行后面一行进行聚合，总共前面一行+当前行+后面一行=3行计算结果，可以这么写：  

```
select calling_num,sum(num),
sum(sum(num)) over(order by calling_num ROWS between 1 preceding and 1 following) as cumulative_sum
from
(select calling_num,called_num,count(*) as num
from phone_test group by calling_num,called_num)a
group by calling_num

130	11	22
132	11	29
134	7	24
135	6	18
138	5	11
```  