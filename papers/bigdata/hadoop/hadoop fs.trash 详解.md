linux系统里，我觉得最大的不方便之一就是没有回收站的概念。由rm -rf引发的血案，估计每个写代码的同学都遇到过。在hadoop或者说hdfs里面，有trash相关的概念，可以使得数据被误删以后，还可以找回来。

## 1.打开trash相关选项
hadoop里的trash选项默认是关闭的。所以如果要生效，需要提前将trash选项打开。修改conf里的core-site.xml即可。我们集群的相关配置如下：  

```
    <!--Enabling Trash-->
    <property>
        <name>fs.trash.interval</name>
        <value>1440</value>
    </property>
    <property>
        <name>fs.trash.checkpoint.interval</name>
        <value>1440</value>
    </property>
```  

fs.trash.interval是在指在这个回收周期之内，文件实际上是被移动到trash的这个目录下面，而不是马上把数据删除掉。等到回收周期真正到了以后，hdfs才会将数据真正删除。默认的单位是分钟，1440分钟=60*24，刚好是一天。  
fs.trash.checkpoint.interval则是指垃圾回收的检查间隔，应该是小于或者等于fs.trash.interval。  

## 2.实际测试

```
xxx@hadoop-back lei.wang]$ hadoop fs -ls /tmp/wanglei/sqoop1
Found 2 items
-rw-r--r--   3 xxx supergroup          0 2016-03-11 14:44 /tmp/wanglei/sqoop1/_SUCCESS
-rw-r--r--   3 xxx supergroup         15 2016-03-11 14:44 /tmp/wanglei/sqoop1/part-m-00000
```  

可以看到hdfs上有这么一个文件夹，然后我们先把他干掉  

```
xxx@hadoop-back lei.wang]$ hadoop fs -rm -r /tmp/wanglei/sqoop1
16/05/20 21:38:18 INFO fs.TrashPolicyDefault: Namenode trash configuration: Deletion interval = 1440 minutes, Emptier interval = 1440 minutes.
Moved: 'hdfs://mycluster/tmp/wanglei/sqoop1' to trash at: hdfs://mycluster/user/xxx/.Trash/Current
```    

同学们看到没有，这个时候，将这部分数据move到了hdfs上的一个地方，并没有真正删掉这部分数据。  

```
[xxx@hadoop-back lei.wang]$ hadoop fs -ls /user/xxx/.Trash/Current/tmp/wanglei
Found 1 items
drwxr-xr-x   - xxx supergroup          0 2016-03-11 14:44 /user/xxx/.Trash/Current/tmp/wanglei/sqoop1
```  

此时数据到了.Trash下面的某个路径。  
如果我们刚才的操作是一时手残，想把数据弄回去，执行mv命令即可  

```
hadoop fs -mv /user/xxx/.Trash/Current/tmp/wanglei/sqoop1 /tmp/wanglei/sqoop1
```  

再查看一下，发现这部分数据又回来了  

```
[xxx@hadoop-back lei.wang]$ hadoop fs -ls /tmp/wanglei/sqoop1
Found 2 items
-rw-r--r--   3 xxx supergroup          0 2016-03-11 14:44 /tmp/wanglei/sqoop1/_SUCCESS
-rw-r--r--   3 xxx supergroup         15 2016-03-11 14:44 /tmp/wanglei/sqoop1/part-m-00000
```  

怎么样，很不错吧。有了Trash，再也不怕误删除了。个人感觉还是蛮好的。  