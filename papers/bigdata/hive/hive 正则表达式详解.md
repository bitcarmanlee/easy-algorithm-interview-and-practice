hive中的正则表达式还是很强大的。数据工作者平时也离不开正则表达式。对此，特意做了个hive正则表达式的小结。所有代码都经过亲测，正常运行。  

## 1.regexp
语法: A REGEXP B  
操作类型: strings  
描述: 功能与RLIKE相同  

```
select count(*) from olap_b_dw_hotelorder_f where create_date_wid not regexp '\\d{8}'
```  

与下面查询的效果是等效的：  

```
select count(*) from olap_b_dw_hotelorder_f where create_date_wid not rlike '\\d{8}';
```  

## 2.regexp_extract
语法: regexp_extract(string subject, string pattern, int index)  
返回值: string  
说明：将字符串subject按照pattern正则表达式的规则拆分，返回index指定的字符。  

```
hive> select regexp_extract('IloveYou','I(.*?)(You)',1) from test1 limit 1;
Total jobs = 1
...
Total MapReduce CPU Time Spent: 7 seconds 340 msec
OK
love
Time taken: 28.067 seconds, Fetched: 1 row(s)
```  

```
hive> select regexp_extract('IloveYou','I(.*?)(You)',2) from test1 limit 1;
Total jobs = 1
...
OK
You
Time taken: 26.067 seconds, Fetched: 1 row(s)
```  

```
hive> select regexp_extract('IloveYou','(I)(.*?)(You)',1) from test1 limit 1;
Total jobs = 1
...
OK
I
Time taken: 26.057 seconds, Fetched: 1 row(s)
```  

```
hive> select regexp_extract('IloveYou','(I)(.*?)(You)',0) from test1 limit 1;
Total jobs = 1
...
OK
IloveYou
Time taken: 28.06 seconds, Fetched: 1 row(s)
```  

```
hive> select regexp_replace("IloveYou","You","") from test1 limit 1;
Total jobs = 1
...
OK
Ilove
Time taken: 26.063 seconds, Fetched: 1 row(s)
```  

## 3.regexp_replace
语法: regexp_replace(string A, string B, string C)  
返回值: string  
说明：将字符串A中的符合java正则表达式B的部分替换为C。注意，在有些情况下要使用转义字符,类似oracle中的regexp_replace函数。  

```
hive> select regexp_replace("IloveYou","You","") from test1 limit 1;
Total jobs = 1
...
OK
Ilove
Time taken: 26.063 seconds, Fetched: 1 row(s)
```  

```
hive> select regexp_replace("IloveYou","You","lili") from test1 limit 1;
Total jobs = 1
...
OK
Ilovelili
```  

参考链接：  
1. https://www.iteblog.com/archives/1639.html  hive字符串处理函数，比较全  
