周末加班，拼一条hql花了40min，里面有许多小细节，特别记录下来方便以后使用。

## 1.表结构
hive表里存的是个thrift结构。我们关注的主要字段如下：  

```
struct UploadDataItem {
1:optional string channel;
2:optional string data;
...
}

struct UploadData {
1:required list<UploadDataItem > uploadDataItems;
}

struct XXX {
...
10:optional UploadData  uploadData 
}
```  

uploadData里面的数据格式如下：  

```
{"uploaddataitems":[{"channel":"xxx","data":"{\"xxx\":\"xxx\",\"time\":1489679985998}","name":"xxx","counter":0,"timestamp":0,"fromsdk":false,"category":"xxx","sourcepackage":null,"id":null,"bucket":0}]}
```  

现在我们的需求就是希望拿到每个bucket里对用的量分别有多少。    

## 2.最终的hql语句

```
SELECT regexp_extract(a.item.data, '"bucket":(\\d)', 1), COUNT(*)
FROM (SELECT explode(uploadData.uploaddataitems) AS item
	FROM push.xmpush_upload_data_internal tablesample(1 percent)
	WHERE date = 20170318
		AND deviceinfo.os = '7.3.15'
	) a
WHERE regexp_extract(a.item.data, '"bucket":(\\d)', 1) <> ''
GROUP BY regexp_extract(a.item.data, '"bucket":(\\d)', 1)
```  

## 3.explode注意事项
因为uploadDataItems里是个list，所以我们需要先用explode将一行变为多行，先生成一个中间虚拟表。explode里面有诸多的注意事项，具体参考之前的文章 http://blog.csdn.net/bitcarmanlee/article/details/51926530 。

## 4.解析json字符串
可能是因为json格式实在太过灵活，个人感觉hive对json的支持不是特别好。所以干脆直接用正则匹配的方式来得到bucket后面对应的具体值。hive正则相关的内容，请参考之前的文章 http://blog.csdn.net/bitcarmanlee/article/details/51106726  

## 5.空字符串的处理
因为data的类型是个string，而且bucket不一定每次都出现，所以经常出现正则匹配出来为空的情况。一则我们需要为空的情况，二来为空的情况多了以后特别容易造成数据倾斜，所以我们需要将这种情况排除掉。hive空值的底层存储比较复杂与混乱，具体可以参考本文  
http://blog.csdn.net/lsxy117/article/details/50387324。本例中空值的情况为''。

## 6.先对数据抽样
当表的数据比较大的时候，可以先对表进行抽样，得到数据的抽样结果，可以快速验证逻辑正确性。例子中的`tablesample(1 percent)`就是对表进行1%的抽样。  