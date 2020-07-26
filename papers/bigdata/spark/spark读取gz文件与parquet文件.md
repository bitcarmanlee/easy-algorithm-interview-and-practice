## 1.spark读取hdfs gz的压缩文件
spark1.5以后的版本支持直接读取gz格式的文件，与读取其他纯文本文件没区别。  
启动spark shell的交互界面，按读取普通文本文件的方式读取gz文件：  

```
sc.textFile("/your/path/*.gz").map{...}
```  

以上的代码就能搞定读取gz压缩文件的需求。  

## 2.spark读取parquet格式文件
spark天然就支持parquet格式的文件。  
同样进入spark shell的交互界面，然后执行以下操作：  

```
val parquetFile = sqlContext.parquetFile("/your/path/*.parquet")
```  

打印parquet文件的schema：  

```
 parquetFile.printSchema()
```  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/readgz/1.jpeg)  

查看具体内容：  

```
parquetFile.take(2).foreach(println)
```  

就可以查看文件中的具体内容。  

## 3.使用Parquet-Tools
https://github.com/apache/parquet-mr/tree/master/parquet-tools  

首先下载相应的jar包。  
然后在本地执行：  

```
alias parquetview='hadoop jar /path/to/your/downloaded/parquet-tools-1.8.1.jar'
```  

接下来使用 meta查看schema，head查看数据  

```
parquetview meta /hdfs/path/single/file/faster
parquetview head /hdfs/path/single/file/faster
```  