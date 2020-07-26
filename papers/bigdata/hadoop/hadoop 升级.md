1.停掉HDFS，备份关键数据  
  
2.需要备份的数据主要包括  
  配置文件：${hadoop_home}/conf目录下的所有配置文件  
  元数据文件：配置文件hdfs-site.xml中的属性“dfs.name.dir”指定的目录下的文件  

3.下载最新稳定版的hadoop 2.4.1版本，并解压到与现有hadoop同级的目录下。  
  说明:旧版的配置文件备份成功后，就不再需要和旧版的hadoop打交道了，下面的所有操作都是在新版的hadoop目录下进行的。  

4. 修改配置文件：  

core-site.xml
```
<configuration>
   <property>
         <name>fs.default.name</name>
         <value>hdfs://192.168.16.241:9000</value>
   </property>

    <property>
        <name>hadoop.tmp.dir</name>
        <value>/disk_c1/hadoop_base2/tmp</value>
        <final>true</final>
    </property>

    <property>
        <name>fs.trash.root</name>
        <value>/disk_c1/hadoop_base2/tmp/Trash</value>
    </property>
    <property>
        <name>io.compression.codecs</name>
        <value>org.apache.hadoop.io.compress.DefaultCodec,org.apache.hadoop.io.compress.GzipCodec,org.apache.hadoop.io.compress.BZip2Codec,com.hadoop.compression.lzo.LzopCodec</value>
    </property>

    <property>
        <name>io.compression.codec.lzo.class</name>
        <value>com.hadoop.compression.lzo.LzoCodec</value>
    </property>
</configuration>
```

hdfs-site.xml
```
<configuration>
     <property>
         <name>dfs.replication</name>
         <value>1</value>
     </property>

    <property>
        <name>dfs.name.dir</name>
        <value>/disk_c1/hadoop_base2/hdfs/name</value>
        <final>true</final>
    </property>

    <property>
        <name>dfs.data.dir</name>
        <value>/disk_c1/hadoop_base2/hdfs/data</value>
        <final>true</final>
    </property>

</configuration>
```

yarn-site.xml
```
<configuration>

<!-- Site specific YARN configuration properties -->
  <property>
     <name>yarn.nodemanager.aux-services</name>
     <value>mapreduce_shuffle</value>
  </property>
  <property>
     <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
     <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
</configuration>

mapred-site.xml
<configuration>
    <property>
       <name>mapreduce.framework.name</name>
       <value>yarn</value>
    </property>
</configuration>
```

设定hadoop-env.sh中的JAVA_HOME变量  

5.进行HDFS升级：sbin/start-dfs.sh –upgrade  
6.确定升级成功，可以使用：bin/hadoop dfsadmin –finalizeUpgrade 最终提交升级  
7.至此HDFS升级已经完成，MapReduce无需升级，只需要将原有的代码用2.4.1版本重新编译即可。  
8.启动Yarn服务: sbin/start-yarn.sh  
9.下面可以通过hadoop自带的例子验证安装是否正确。  
10.在hadoop-2.4.1的根目录下执行：  
```
  $mkdir input
  $ cp etc/hadoop/*.xml input
  $ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.4.1.jar grep input output 'dfs[a-z.]+'
  $ cat output/*   //如果文件中有内容,则认为升级成功.
```