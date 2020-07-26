## 1.问题描述
往集群提交任务的时候，需要在hdfs上面读取一个资源文件。在读取该资源文件的时候，代码爆出如下异常：  

```
Error: java.io.IOException: Filesystem closed
	at org.apache.hadoop.hdfs.DFSClient.checkOpen(DFSClient.java:823)
	at org.apache.hadoop.hdfs.DFSInputStream.readWithStrategy(DFSInputStream.java:846)
	at org.apache.hadoop.hdfs.DFSInputStream.read(DFSInputStream.java:907)
	at java.io.DataInputStream.readFully(DataInputStream.java:195)
	at java.io.DataInputStream.readFully(DataInputStream.java:169)
	at org.apache.parquet.hadoop.ParquetFileReader$ConsecutiveChunkList.readAll(ParquetFileReader.java:756)
	at org.apache.parquet.hadoop.ParquetFileReader.readNextRowGroup(ParquetFileReader.java:494)
	at org.apache.parquet.hadoop.InternalParquetRecordReader.checkRead(InternalParquetRecordReader.java:127)
	at org.apache.parquet.hadoop.InternalParquetRecordReader.nextKeyValue(InternalParquetRecordReader.java:208)
	at org.apache.parquet.hadoop.ParquetRecordReader.nextKeyValue(ParquetRecordReader.java:201)
	at org.apache.hadoop.mapreduce.lib.input.DelegatingRecordReader.nextKeyValue(DelegatingRecordReader.java:89)
...
```  

## 2.问题的原因
一般读取hdfs上文件的api是这样写的：  

```
public void initPackageNameTypeMap {
	Configuration conf = new Configuration();
	FileSystem fs = FileSystem.get(conf);
	Path file = new Path("filePath");
	...
}
```  

当任务提交到集群上面以后，多个datanode在getFileSystem过程中，由于Configuration一样，会得到同一个FileSystem。如果有一个datanode在使用完关闭连接，其它的datanode在访问就会出现上述异常。  

## 3.解决方案
解决的方法其实很简单，在代码中加入如下配置就好：  

```
conf.setBoolean("fs.hdfs.impl.disable.cache", true);
```  

FileSytem类内部有一个static CACHE，用来保存每种文件系统的实例集合，FileSystem类中可以通过"fs.%s.impl.disable.cache"来指定是否缓存FileSystem实例(其中%s替换为相应的scheme，比如hdfs、local、s3、s3n等)，即一旦创建了相应的FileSystem实例，这个实例将会保存在缓存中，此后每次get都会获取同一个实例。所以设为true以后，就能解决上面的异常。  


## 参考链接：  
1.http://stackoverflow.com/questions/23779186/ioexception-filesystem-closed-exception-when-running-oozie-workflow  
2.http://stackoverflow.com/questions/20057881/hadoop-filesystem-closed-exception-when-doing-bufferedreader-close  
3.http://shift-alt-ctrl.iteye.com/blog/2108760  
