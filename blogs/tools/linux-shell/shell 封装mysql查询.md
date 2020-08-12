有时候需要将sql查询封装在shell脚本中，然后将查询结果导出存入文本后续再做进一步处理。对于这种常见需求，特意做了个实例，代码已经通过测试，同学们可以大胆使用。  

```
#!/bin/bash

host=xxx
user=xxx
password=xxx
port=xxx
dbname=xxx

sql_conn_str="-h${host} -P${port} -u${user} -p${password} $dbname"

function select_from_mysql()
{
	sql="xxxxxx"
	echo "$sql" | mysql -s $sql_conn_str >resultfile
}

select_from_mysql
```  

上面的代码就可以满足我们的需求。注意的几个小点：  
1.实际使用时候，将数据库各配置项，以及具体的sql查询语句替换成实际配置项即可。  
2.mysql -s选项表示查询输出的结果不带字段名称，如果不加-s选项会输出字段名称。  
3.将resultfile换成你最终结果文件存储的地址。  