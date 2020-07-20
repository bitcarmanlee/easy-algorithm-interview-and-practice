## 1.查看分区命令

1.show partitions xxx
```
hive> show partitions xxx;
OK
day=20150908
day=20151020
day=20151021
day=20151022

...

day=20160318
Time taken: 0.139 seconds, Fetched: 144 row(s)
```  

由此可见上述命令显示了基本的分区情况  


2.desc xxx partition(day=20160315)
```
hive> desc xxx partition(day=20160315);
OK
list_time               string
cookie                  string
device_id               string
os                      string
device_brand            string
search_id               string
search_guid             string
...
filter                  string
day                     string

# Partition Information
# col_name                data_type               comment

day                     string
Time taken: 0.359 seconds, Fetched: 36 row(s)
```  

此命令显示了表结构与partition information  



3.extended
```
hive>  desc extended ods_search_log_app partition(day=20160315);
OK
list_time               string
cookie                  string
device_id               string
os                      string
device_brand            string
search_id               string
search_guid             string
...
coupon                  string
filter                  string
day                     string

# Partition Information
# col_name                data_type               comment

day                     string

Detailed Partition Information    Partition(values:[20160315], dbName:xxx, tableName:xxx, ............. location:hdfs://mycluster/data/hive/warehouse/xxx/xxx/day=20160315, inputFormat:org.apache.hadoop.mapred.TextInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat, compressed:false, numBuckets:-1, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, parameters:{serialization.format=1}), bucketCols:[], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), parameters:{transient_lastDdlTime=1458083053})
Time taken: 0.369 seconds, Fetched: 38 row(s)
```  

多了个Detailed Partition Information，最初使用这条命令的初衷，是查找分区对应的location，使用这条命令可以找到   


## 4.hive建分区表
```
create external table if not exists cheap_hotel_user(device string, booking_freq int, book_price string)
partitioned by (day string)
row format delimited fields terminated by '\t'
location '/data/output/search/stage/daily/cheap_hotel_user'
```  

注意的是partition需要在row format之前指定  


## 5.添加分区
```
ALTER TABLE table_name ADD PARTITION (partCol = 'value1') location 'loc1';

ALTER TABLE table_name ADD IF NOT EXISTS PARTITION (dt='20130101') LOCATION '/user/hadoop/warehouse/table_name/dt=20130101'; //一次添加一个分区

ALTER TABLE page_view ADD PARTITION (dt='2008-09-01', country='jp') location '/path/to/us/part080901 PARTITION (dt='2008-09-01', country='jp') location '/path/to/us/part080901';  //一次添加多个分区
```    

## 6.删除分区

```
ALTER TABLE login DROP IF EXISTS PARTITION (dt='2008-09-01');
ALTER TABLE page_view DROP IF EXISTS PARTITION (dt='2008-09-01', country='jp');

修改分区
ALTER TABLE table_name PARTITION (dt='2008-08-08') SET LOCATION "new location";
ALTER TABLE table_name PARTITION (dt='2008-08-08') RENAME TO PARTITION (dt='20080808’);
```