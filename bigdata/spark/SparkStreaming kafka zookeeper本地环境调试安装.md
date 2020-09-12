## 1.需求
线上需要使用流式数据实时反馈CTR，因此想用spark streaming计算相关数据。之前一直没有在本地配置streaming的调试环境，因此在本地安装一下streaming的调试环境并记录。  

## 2.需要安装的组件
spark streaming一般会接消息队列作为数据源，以kafka为例，所以需要在本地安装kafka。kafka又依赖zookeeper，所以还需要安装zookeeper。  

## 3. 安装zookeeper
### 3.1 下载zk
先去zookeeper官网下载zookeeper对应的.bin.tar.gz包，我下载的版本为apache-zookeeper-3.5.8-bin.tar.gz。  

下载完毕以后解压。  

### 3.2 配置环境变量
编辑~/.bashrc文件，加上环境变量  

```
export ZOOKEEPER_HOME=/opt/zookeeper
export PATH=$PATH:$ZOOKEEPER_HOME/bin
```  

其中ZOOKEEPER_HOME为解压的地址。    

### 3.3  修改zoo.cfg
需要将 $ZOOKEEPER_HOME/conf 目录下的 zoo_sample.cfg 重命名为 zoo.cfg, zoo.cfg。    
默认配置为  

```
# The number of milliseconds of each 
ticktickTime=2000
# The number of ticks that the initial 
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between 
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just 
# example sakes.dataDir=/tmp/zookeeper
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the 
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1

```  

将其修改为  

```
ticketTime=2000
clientPort=2181
dataDir=/home/mi/wanglei/zkdata
dataLogDir=/home/mi/wanglei/zklogs
```  

其中,dataDir, dataLogDir自己配置。  


## 3.4 启动zk  

```
sh zkServer.sh start
```  

输出信息为  

```
ZooKeeper JMX enabled by default
Using config: /home/mi/wanglei/soft/apache-zookeeper-3.5.8-bin/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
```  
说明启动成功  

## 3.5 验证zk信息
在另外终端中输入  

```
telnet 127.0.0.1 2181
```  

```
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
```  

然后输入stat，会报错  

```
stat is not executed because it is not in the whitelist. connection closed by foreign host
```  
可以修改zkServer.sh  

```
...
    ZOOMAIN="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=$JMXPORT -Dcom.sun.management.jmxremote.authenticate=$JMXAUTH -Dcom.sun.management.jmxremote.ssl=$JMXSSL -Dzookeeper.jmx.log4j.disable=$JMXLOG4J org.apache.zookeeper.server.quorum.QuorumPeerMain"
  fi
else
    echo "JMX disabled by user request" >&2
    ZOOMAIN="org.apache.zookeeper.server.quorum.QuorumPeerMain"
fi

```  

在后面加上一行  

```
ZOOMAIN="-Dzookeeper.4lw.commands.whitelist=* ${ZOOMAIN}"
```  

此时再执行  

```
telnet 127.0.0.1 2181
```  
输入stat  

```
Zookeeper version: 3.5.8-f439ca583e70862c3068a1f2a7d4d068eec33315, built on 05/04/2020 15:07 GMT
Clients:
 /127.0.0.1:47452[1](queued=0,recved=1992,sent=1995)
 /127.0.0.1:50060[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/1/62
Received: 2081
Sent: 2087
Connections: 2
Outstanding: 0
Zxid: 0xa1
Mode: standalone
Node count: 134
Connection closed by foreign host.
```  

## 4.安装kafka
### 4.1 下载并解压
去kafka官网下载并解压kafka到本地  

### 4.2 创建topic
```
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```  
### 4.3启动生产者

```
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```  
注意kafka依赖zookeeper，需要保证zookeeper正常运行。


## 5.streaming代码
终于到最后写streaming的环节了。可以在IDE中新建一个maven项目，具体的pom.xml配置如下  

## 5.1.配置pom.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>spark-streaming-local</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <scala.version>2.11.2</scala.version>
        <!--<spark.version>2.1.0</spark.version>-->
        <spark.version>2.1.0</spark.version>
        <spark.kafka.version>1.6.3</spark.kafka.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <gjson.version>2.8.0</gjson.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-core_2.11</artifactId>
            <version>${spark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-sql_2.11</artifactId>
            <version>${spark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-streaming_2.11</artifactId>
            <version>${spark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-streaming-kafka-0-10_2.11</artifactId>
            <version>${spark.version}</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.5.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <fork>true</fork>
                    <verbose>true</verbose>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.scala-tools</groupId>
                <artifactId>maven-scala-plugin</artifactId>
                <version>2.15.2</version>
                <configuration>
                    <scalaVersion>2.11.8</scalaVersion>
                </configuration>
                <executions>
                    <execution>
                        <id>scala-compile-first</id>
                        <phase>process-resources</phase>
                        <goals>
                            <goal>compile</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>
```  

### 5.2.写一个wordcount demo

```
import org.apache.kafka.common.serialization.{IntegerDeserializer, StringDeserializer}
import org.apache.spark.SparkConf
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.{Seconds, StreamingContext}

object KafkaWordCount {

  def main(args: Array[String]): Unit = {
    val zkQuorum = "xxx:9092"
    val topics = Array("test")
    val kafkaMap = Map[String, Object](
      "bootstrap.servers" -> zkQuorum,
      "key.deserializer" -> classOf[IntegerDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "test",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean),
      "session.timeout.ms" -> "30000"
    )
    val conf = new SparkConf()
      .setAppName(KafkaWordCount.getClass.getSimpleName)
      .setMaster("local[4]")

    val ssc = new StreamingContext(conf, Seconds(20))
    val consumer = ConsumerStrategies.Subscribe[String, String](topics, kafkaMap)

    val lines = KafkaUtils.createDirectStream(
      ssc,
      LocationStrategies.PreferConsistent,
      consumer
    )
      .map(_.value())

    val wordCount = lines.flatMap(_.split(" "))
      .map(key => (key, 1L))
      .reduceByKey(_ + _)

    wordCount.print()
    ssc.start()
    ssc.awaitTermination()
  }
}
```  

在IDE里启动，可以看到IDE里的输出

```
20/05/12 15:16:40 INFO ShuffleBlockFetcherIterator: Started 0 remote fetches in 0 ms
20/05/12 15:16:40 INFO TaskSetManager: Finished task 0.0 in stage 19.0 (TID 22) in 5 ms on localhost (executor driver) (1/3)
20/05/12 15:16:40 INFO TaskSetManager: Finished task 1.0 in stage 19.0 (TID 23) in 4 ms on localhost (executor driver) (2/3)
20/05/12 15:16:40 INFO Executor: Finished task 2.0 in stage 19.0 (TID 24). 1718 bytes result sent to driver
20/05/12 15:16:40 INFO TaskSetManager: Finished task 2.0 in stage 19.0 (TID 24) in 5 ms on localhost (executor driver) (3/3)
20/05/12 15:16:40 INFO TaskSchedulerImpl: Removed TaskSet 19.0, whose tasks have all completed, from pool 
20/05/12 15:16:40 INFO DAGScheduler: ResultStage 19 (print at KafkaWordCount.scala:40) finished in 0.006 s
20/05/12 15:16:40 INFO DAGScheduler: Job 9 finished: print at KafkaWordCount.scala:40, took 0.011706 s
20/05/12 15:16:40 INFO JobScheduler: Finished job streaming job 1589267800000 ms.0 from job set of time 1589267800000 ms
20/05/12 15:16:40 INFO JobScheduler: Total delay: 0.088 s for time 1589267800000 ms (execution: 0.064 s)
20/05/12 15:16:40 INFO ShuffledRDD: Removing RDD 19 from persistence list
20/05/12 15:16:40 INFO BlockManager: Removing RDD 19
20/05/12 15:16:40 INFO MapPartitionsRDD: Removing RDD 18 from persistence list
20/05/12 15:16:40 INFO BlockManager: Removing RDD 18
20/05/12 15:16:40 INFO MapPartitionsRDD: Removing RDD 17 from persistence list
20/05/12 15:16:40 INFO BlockManager: Removing RDD 17
20/05/12 15:16:40 INFO MapPartitionsRDD: Removing RDD 16 from persistence list
20/05/12 15:16:40 INFO BlockManager: Removing RDD 16
20/05/12 15:16:40 INFO KafkaRDD: Removing RDD 15 from persistence list
20/05/12 15:16:40 INFO BlockManager: Removing RDD 15
20/05/12 15:16:40 INFO ReceivedBlockTracker: Deleting batches: 
20/05/12 15:16:40 INFO InputInfoTracker: remove old batch metadata: 1589267760000 ms
-------------------------------------------
Time: 1589267800000 ms
-------------------------------------------
```  

然后在kafka producer中输入  

```
a b c ab a b c d e
```  

输出：  

```
(d,1)
(e,1)
(a,2)
(ab,1)
(b,2)
(c,2)
```  

实现了wordcount的功能！