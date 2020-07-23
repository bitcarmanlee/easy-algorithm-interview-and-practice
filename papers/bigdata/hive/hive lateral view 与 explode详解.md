## 1.explode
hive wiki对于expolde的解释如下：  

explode() takes in an array (or a map) as an input and outputs the elements of the array (map) as separate rows. UDTFs can be used in the SELECT expression list and as a part of LATERAL VIEW.  

As an example of using explode() in the SELECT expression list, consider a table named myTable that has a single column (myCol) and two rows:  


![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hive/explode/1.jpeg)

Then running the query:  

```
SELECT explode(myCol) AS myNewCol FROM myTable;
```  

will produce:  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hive/explode/2.jpeg)
  
The usage with Maps is similar:  

```
SELECT explode(myMap) AS (myMapKey, myMapValue) FROM myMapTable;
```  

总结起来一句话：explode就是将hive一行中复杂的array或者map结构拆分成多行。  

使用实例：  
xxx表中有一个字段mvt为string类型，数据格式如下：  

[{"eid":"38","ex":"affirm_time_Android","val":"1","vid":"31","vr":"var1"},{"eid":"42","ex":"new_comment_Android","val":"1","vid":"34","vr":"var1"},{"eid":"40","ex":"new_rpname_Android","val":"1","vid":"1","vr":"var1"},{"eid":"19","ex":"hotellistlpage_Android","val":"1","vid":"1","vr":"var01"},{"eid":"29","ex":"bookhotelpage_Android","val":"0","vid":"1","vr":"var01"},{"eid":"17","ex":"trainMode_Android","val":"1","vid":"1","vr":"mode_Android"},{"eid":"44","ex":"ihotelList_Android","val":"1","vid":"36","vr":"var1"},{"eid":"47","ex":"ihotelDetail_Android","val":"0","vid":"38","vr":"var1"}]  

用explode小试牛刀一下：  

```
select explode(split(regexp_replace(mvt,'\\[|\\]',''),'\\},\\{')) from ods_mvt_hourly where day=20160710 limit 10;
```  

最后出来的结果如下：  
```
{"eid":"38","ex":"affirm_time_Android","val":"1","vid":"31","vr":"var1"
"eid":"42","ex":"new_comment_Android","val":"1","vid":"34","vr":"var1"
"eid":"40","ex":"new_rpname_Android","val":"1","vid":"1","vr":"var1"
"eid":"19","ex":"hotellistlpage_Android","val":"1","vid":"1","vr":"var01"
"eid":"29","ex":"bookhotelpage_Android","val":"0","vid":"1","vr":"var01"
"eid":"17","ex":"trainMode_Android","val":"1","vid":"1","vr":"mode_Android"
"eid":"44","ex":"ihotelList_Android","val":"1","vid":"36","vr":"var1"
"eid":"47","ex":"ihotelDetail_Android","val":"0","vid":"38","vr":"var1"}
{"eid":"38","ex":"affirm_time_Android","val":"1","vid":"31","vr":"var1"
"eid":"42","ex":"new_comment_Android","val":"1","vid":"34","vr":"var1"
```


## 2.lateral view
hive wiki 上的解释如下：  
### Lateral View Syntax

lateralView: LATERAL VIEW udtf(expression) tableAlias AS columnAlias (',' columnAlias)*    
fromClause: FROM baseTable (lateralView)*  

### Description

Lateral view is used in conjunction with user-defined table generating functions such as explode(). As mentioned in Built-in Table-Generating Functions, a UDTF generates zero or more output rows for each input row. A lateral view first applies the UDTF to each row of base table and then joins resulting output rows to the input rows to form a virtual table having the supplied table alias.  


### Example
Consider the following base table named pageAds. It has two columns: pageid (name of the page) and adid_list (an array of ads appearing on the page)  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hive/explode/3.jpeg)  

An example table with two rows:  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hive/explode/4.jpeg)  

and the user would like to count the total number of times an ad appears across all pages.  
A lateral view with explode() can be used to convert adid_list into separate rows using the query:  

```
SELECT pageid, adid
FROM pageAds LATERAL VIEW explode(adid_list) adTable AS adid;
```  

The resulting output will be  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hive/explode/5.jpeg)  

Then in order to count the number of times a particular ad appears, count/group by can be used:  

```
SELECT adid, count(1)
FROM pageAds LATERAL VIEW explode(adid_list) adTable AS adid
GROUP BY adid;
```  

The resulting output will be  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hive/explode/6.jpeg)  

lateral view用于和split, explode等UDTF一起使用，它能够将一行数据拆成多行数据，在此基础上可以对拆分后的数据进行聚合。lateral view首先为原始表的每行调用UDTF，UDTF会把一行拆分成一或者多行，lateral view再把结果组合，产生一个支持别名表的虚拟表。  

由此可见，lateral view与explode等udtf就是天生好搭档，explode将复杂结构一行拆成多行，然后再用lateral view做各种聚合。  

## 3.实例
还是第一部分的例子，上面我们explode出来以后的数据，不是标准的json格式，我们通过lateral view与explode组合解析出标准的json格式数据:  

```
SELECT ecrd, CASE WHEN instr(mvtstr,'{')=0
    AND instr(mvtstr,'}')=0 THEN concat('{',mvtstr,'}') WHEN instr(mvtstr,'{')=0
    AND instr(mvtstr,'}')>0 THEN concat('{',mvtstr) WHEN instr(mvtstr,'}')=0
    AND instr(mvtstr,'{')>0 THEN concat(mvtstr,'}') ELSE mvtstr END AS mvt
      FROM ods.ods_mvt_hourly LATERAL VIEW explode(split(regexp_replace(mvt,'\\[|\\]',''),'\\},\\{')) addTable AS mvtstr
        WHERE DAY='20160710' and ecrd is not null limit 10
```  

查询出来的结果：  
```
xxx
{"eid":"38","ex":"affirm_time_Android","val":"1","vid":"31","vr":"var1"}
xxx
{"eid":"42","ex":"new_comment_Android","val":"1","vid":"34","vr":"var1"}
xxx
{"eid":"40","ex":"new_rpname_Android","val":"1","vid":"1","vr":"var1"}
xxx
{"eid":"19","ex":"hotellistlpage_Android","val":"1","vid":"1","vr":"var01"}
xxx
{"eid":"29","ex":"bookhotelpage_Android","val":"0","vid":"1","vr":"var01"
xxx
{"eid":"17","ex":"trainMode_Android","val":"1","vid":"1","vr":"mode_Android"}
xxx
{"eid":"44","ex":"ihotelList_Android","val":"1","vid":"36","vr":"var1"}
xxx
{"eid":"47","ex":"ihotelDetail_Android","val":"1","vid":"38","vr":"var1"}
xxx
{"eid":"38","ex":"affirm_time_Android","val":"1","vid":"31","vr":"var1"}
xxx
{"eid":"42","ex":"new_comment_Android","val":"1","vid":"34","vr":"var1"}
```

## 4.Ending
Lateral View通常和UDTF一起出现，为了解决UDTF不允许在select字段的问题。  
Multiple Lateral View可以实现类似笛卡尔乘积。  
Outer关键字可以把不输出的UDTF的空结果，输出成NULL，防止丢失数据。  

## 参考内容：    
1.http://blog.csdn.net/oopsoom/article/details/26001307  lateral view的用法实例  
2.https://my.oschina.net/leejun2005/blog/120463 复合函数的用法，比较详细  
3.http://blog.csdn.net/zhaoli081223/article/details/46637517 udtf的介绍  