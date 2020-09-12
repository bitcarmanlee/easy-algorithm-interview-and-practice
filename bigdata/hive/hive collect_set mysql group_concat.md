## 1.hive中collect_set用法
hive表有两列，其中一列为id，另外一列为channel。现在想把相同id的channel聚合到一块并去重。  
比如表中如下数据  
id1 c1  
id2 c2  
id1 c2  
id1 c1  
id1 c3  
id1 c3  
id2 c4  
输出结果如下  
id1 c1,c2,c3  
id2 c2,c4  

用collect_set函数可以满足上面的要求  

```
select id, concat_ws(',', collect_set(channel)) from tablexxx group by id
```  

如果channel不要求去重，将collect_set改为collect_list即可。  

## 2.mysql中group_concat

在mysql中也有类似的函数group_concat  
假设mysql表同样有两列:id,name。现在将相同id的name聚合在一起，假设表中数据为  
id1 a  
id1 b  
id1 c  
id1 a  
id2 e  
id2 f  

默认的分隔符是","  
```
select id,group_concat(name separator ';') from tablexxx group by id;
```  

如果要对name去重  


```
select id,group_concat(distinct name) from tablexxx group by id;
```  

如果还想对name排序  
 

```
select id,group_concat(name order by name desc) from tablexxx group by id;  
```
