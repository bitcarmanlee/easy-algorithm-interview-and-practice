like与rlike的区别：  
like不是正则，而是通配符。这个通配符可以看一下SQL的标准，例如%代表任意多个字符。  
rlike是正则，正则的写法与java一样。'\'需要使用'\\',例如'\w'需要使用'\\w'  

```
hive> select "aaaaa" like "%aaa%" from test_struct limit 10;
Total jobs = 1
...
OK
true
true
Time taken: 22.056 seconds, Fetched: 2 row(s)

hive> select "aaaaa" rlike "%aaa%" from test_struct limit 10;
Total jobs = 1
...
OK
false
false
Time taken: 26.065 seconds, Fetched: 2 row(s)
```

注意这两者区别：%是sql中的通配符，所以用like的输出为true。而正则里没有%的表示方式，所以输出false  

rlike的话，用相应的正则表达式即可  

```
hive> select "aaaaa" rlike ".*aaa.*" from test_struct limit 10;
Total jobs = 1
...
OK
true
true
Time taken: 24.168 seconds, Fetched: 2 row(s)

select "aaaaa" rlike "^aaa" from test_struct limit 10;
Total jobs = 1
...
OK
true
true
Time taken: 22.059 seconds, Fetched: 2 row(s)

hive> select "aaa" rlike "aa\\w" from test_struct limit 2;
Total jobs = 1
Launching Job 1 out of 1
...
OK
true
true
Time taken: 22.055 seconds, Fetched: 2 row(s)

hive> select "aaa" rlike "aa\\w+" from test_struct limit 2;
Total jobs = 1
Launching Job 1 out of 1
...
OK
true
true
Time taken: 22.055 seconds, Fetched: 2 row(s)
```  


以上几种方式的正则都可以  

rp_name_cn like '%不含早%' 与rp_name_cn rlike '不含早'的效果一致  