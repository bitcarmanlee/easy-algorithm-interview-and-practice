## 1.什么是窗口函数
在明白窗口函数的用途之前，我们先稍微提一下聚合函数，比如sum, count等常用的聚合函数，作用是将一列中多行的值合并为一行。与之对应的是，窗口函数完成的功能是本行内运算，得到多行的运算结果，即每一行的结果对应的多行的结果。一般窗口函数的语法为  
```
function() over (partition by column1, column2 order by column3)
```  

## 2.窗口函数的类型
1.聚合型，像sum,count,avg等操作。  
2.分析型，像rank, row_number, dense_rank等常见的排序窗口函数。  
3.取值型窗口函数, lag, lead等。  

## 3.例子  
### 3.1 取分组以后的最大值  

```
select * from 
( 
select *,ROW_NUMBER() OVER(PARTITION BY idtype ORDER BY id DESC) as num 
from tablexxx 
) t 
where t.num = 1
```  
上面的代码，先按照idtype进行分组partition，然后取每个分组中最大的那个id。  

### 3.2 按某个字段分组以后将另外的字段聚合  
```
select collect_set(b) over(distribute by a order by c) from tablexxx
```  

按字段a分组，按字段c排序，然后将字段b聚合在一起。如果是collect_list表示字段不去重，collect_set表示字段去重。  

如果需要对字段b里的内容进行排序，可以用sort_array。  

```
select sort_array(collect_set(b) over(distribute by a)) from tablexxx
```  

### 3.3 与group by做对比
假设有以下数据  

```
zs	classA	80
ls	classB	83
ww	classA	88
xl	classC	92
wl	classB	79
lu	classC	85
```  

字段名分别为name, grade, score，表名为table_test_data。现在想获取每个grade的最大score，我们可以这么写  

```
select grade, max(score) from table_test_data where date=20200409 group by grade
```  

当然，我们还可以用窗口函数写  
```
select grade, score from (select *, row_number() over (partition by grade order by score desc) as num from browser.table_test_data where date=20200409)t where t.num = 1;
```  

上面两个语句跑出来的结果相同  

```
grade	score
classA	88
classB	83
classC	92
```  

当然直接用group by比窗口函数要简单很多。但是如果我们还想获取name咋办？  
这个时候group by就无能为力了，窗口函数可以。  

```
select name, grade, score from (select *, row_number() over (partition by grade order by score desc) as num from browser.table_test_dta where date=20200409)t where t.num = 1;
```  

结果为  

```
name	grade	score
ww	classA	88
ls	classB	83
xl	classC	92
```  

总结一下就是  
如果要select出不在group by语句中的字段，而且该字段不在聚合函数里，则应该使用row_number() over(partition by)，如果需要select的字段全在group by中，则可以直接使用group by语句。  