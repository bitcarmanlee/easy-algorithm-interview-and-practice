## 1.Map详解
hive里支持map的结构如下：  
(key1, value1, key2, value2, ...) Creates a map with the given key/value pairs  

建表语句：  
```
create table test_map(name string, score map<string,int>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
```  

测试数据
```
cat test
leilei 数学:99,语文:90,英语:96
lucy 数学:100,语文:85,英语:91
```  

将数据导入表中：  
```
LOAD DATA LOCAL INPATH '/home/webopa/lei.wang/datas_test/test_map' OVERWRITE INTO TABLE test_map;
```  

在表中查询：  
```
hive> select * from test_map;
OK
leilei {"数学":99,"语文":90,"英语":96}
lucy {"数学":100,"语文":85,"英语":91}
Time taken: 0.052 seconds, Fetched: 2 row(s)

hive> select ts.name,ts.score['数学'] from test_map ts;
Total jobs = 1
Launching Job 1 out of 1
...
Total MapReduce CPU Time Spent: 3 seconds 280 msec
OK
leilei 99
lucy 100
Time taken: 26.072 seconds, Fetched: 2 row(s)
```  

## 2.Struct
hive里支持的Struct结构：  
(val1, val2, val3, ...) Creates a struct with the given field values. Struct field names will be col1, col2, ...   

建表语句  
```
CREATE TABLE test_struct(name string,lable struct<price:string,pay:string,num:int>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
```  

测试数据  
```
cat test_struct
aaa cheap,imm,1
bbb high,imm,2
```  

将数据导入表中  
```
LOAD DATA LOCAL INPATH '/home/webopa/lei.wang/datas_test/test_struct' OVERWRITE INTO TABLE test_struct
```  

在表中查询  
```
hive> select * from test_struct;
OK
aaa {"price":"cheap","pay":"imm","num":1}
bbb {"price":"high","pay":"imm","num":2}
Time taken: 0.046 seconds, Fetched: 2 row(s)

hive> select name,lable.price from test_struct;
Total jobs = 1
Launching Job 1 out of 1
...
Total MapReduce CPU Time Spent: 1 seconds 270 msec
OK
aaa cheap
bbb high
Time taken: 20.054 seconds, Fetched: 2 row(s)
```