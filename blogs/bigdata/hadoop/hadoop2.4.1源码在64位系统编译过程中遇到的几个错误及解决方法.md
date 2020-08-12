hadoop2.4.1源码在64位系统编译过程中遇到的几个错误及解决方法  
操作系统：Ubuntu 14.04.2 LTS \n \l  
源码：hadoop-2.4.1-src.tar.gz（apache官网下载）  

## 错误1：
```
[ERROR] Failed to execute goal org.apache.hadoop:hadoop-maven-plugins:2.2.0:protoc (compile-protoc) on project hadoop-common: org.apache.maven.plugin.MojoExecutionException: protoc version is 'libprotoc 2.4.1', expected version is '2.5.0' -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
[ERROR]
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <goals> -rf :hadoop-common
```

解决方法：  
安装protoc wget https://protobuf.googlecode.com/files/protobuf-2.5.0.tar.gz  
（此处下载https://code.google.com/p/protobuf/downloads/list）  
（网址被墙了，下载需翻墙）  
解压， 进入根目录执行 sudo ./configure --prefix=/usr（注意指定prefix）  

遇到protoc: error while loading shared libraries: libprotoc.so.8: cannot open shared object file: No such file or directory时，如ubuntu系统，默认安装在/usr/local/lib下，需要指定/usr。sudo ./configure --prefix=/usr 必须加上--prefix参数，重新编译和安装。  

## 错误2：
```
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-antrun-

    plugin:1.6:run (make) on project hadoop-common: An Ant BuildException has

    occured: Execute failed: java.io.IOException: Cannot run program "cmake" (in

    directory "/home/wyf/hadoop-2.0.2-alpha-src/hadoop-common-project/hadoop-

    common/target/native"): java.io.IOException: error=2, No such file or directory

    -> [Help 1]
    [ERROR]
    [ERROR] To see the full stack trace of the errors, re-run Maven with the -e

    switch.
    [ERROR] Re-run Maven using the -X switch to enable full debug logging.
    [ERROR]
    [ERROR] For more information about the errors and possible solutions, please

    read the following articles:
    [ERROR] [Help 1]

    http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
```

解决方法：  
安装Cmake  
sudo apt-get install cmake  

## 错误3：
```
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-antrun-plugin:1.7:run (make) on project hadoop-common: An Ant BuildException has occured: exec returned: 1  
[ERROR] around Ant part …<exec dir=”/home/linuxidc/workplace/hadoop/hadoop-2.6.0-src/hadoop-common-project/hadoop-common/target/native” executable=”cmake” failonerror=”true”>… @ 4:152 in /home/linuxidc/workplace/hadoop/hadoop-2.6.0-src/hadoop-common-project/hadoop-common/target/antrun/build-main.xml
```  

解决方法：  
这时候需要安装下面两个库，如下：  
sudo apt-get install zlib1g-dev  
sudo apt-get install libssl-dev  

## 错误4：
```
main:
    [mkdir] Skipping /home/hadoop/hadoop-2.4.1-src/hadoop-hdfs-project/hadoop-hdfs-httpfs/downloads because it already exists.
      [get] Getting: http://archive.apache.org/dist/tomcat/tomcat-6/v6.0.36/bin/apache-tomcat-6.0.36.tar.gz
      [get] To: /home/hadoop/hadoop-2.4.1-src/hadoop-hdfs-project/hadoop-hdfs-httpfs/downloads/apache-tomcat-6.0.36.tar.gz
      [get] Error getting http://archive.apache.org/dist/tomcat/tomcat-6/v6.0.36/bin/apache-tomcat-6.0.36.tar.gz to /home/hadoop/hadoop-2.4.1-src/hadoop-hdfs-project/hadoop-hdfs-httpfs/downloads/apache-tomcat-6.0.36.tar.gz
```

解决方法：  
原因是网站被墙，无法连接到上述网址  
解决方案：手动下载tomcat放入对应的路径即可  

最后编译成功：
```
[INFO] Apache Hadoop Main ................................ SUCCESS [0.961s]
[INFO] Apache Hadoop Project POM ......................... SUCCESS [0.866s]
[INFO] Apache Hadoop Annotations ......................... SUCCESS [1.851s]
[INFO] Apache Hadoop Assemblies .......................... SUCCESS [0.201s]
[INFO] Apache Hadoop Project Dist POM .................... SUCCESS [1.771s]
[INFO] Apache Hadoop Maven Plugins ....................... SUCCESS [2.496s]
[INFO] Apache Hadoop MiniKDC ............................. SUCCESS [1.911s]
[INFO] Apache Hadoop Auth ................................ SUCCESS [2.156s]
[INFO] Apache Hadoop Auth Examples ....................... SUCCESS [1.603s]
[INFO] Apache Hadoop Common .............................. SUCCESS [51.069s]
[INFO] Apache Hadoop NFS ................................. SUCCESS [3.985s]
[INFO] Apache Hadoop Common Project ...................... SUCCESS [0.023s]
[INFO] Apache Hadoop HDFS ................................ SUCCESS [1:30.010s]
[INFO] Apache Hadoop HttpFS .............................. SUCCESS [10.351s]
[INFO] Apache Hadoop HDFS BookKeeper Journal ............. SUCCESS [3:02.918s]
[INFO] Apache Hadoop HDFS-NFS ............................ SUCCESS [2.426s]
[INFO] Apache Hadoop HDFS Project ........................ SUCCESS [0.056s]
[INFO] hadoop-yarn ....................................... SUCCESS [0.061s]
[INFO] hadoop-yarn-api ................................... SUCCESS [45.453s]
[INFO] hadoop-yarn-common ................................ SUCCESS [1:25.526s]
[INFO] hadoop-yarn-server ................................ SUCCESS [0.022s]
[INFO] hadoop-yarn-server-common ......................... SUCCESS [5.669s]
[INFO] hadoop-yarn-server-nodemanager .................... SUCCESS [5:38.132s]
[INFO] hadoop-yarn-server-web-proxy ...................... SUCCESS [1.918s]
[INFO] hadoop-yarn-server-applicationhistoryservice ...... SUCCESS [15.800s]
[INFO] hadoop-yarn-server-resourcemanager ................ SUCCESS [8.591s]
[INFO] hadoop-yarn-server-tests .......................... SUCCESS [0.478s]
[INFO] hadoop-yarn-client ................................ SUCCESS [3.026s]
[INFO] hadoop-yarn-applications .......................... SUCCESS [0.020s]
[INFO] hadoop-yarn-applications-distributedshell ......... SUCCESS [1.648s]
[INFO] hadoop-yarn-applications-unmanaged-am-launcher .... SUCCESS [1.265s]
[INFO] hadoop-yarn-site .................................. SUCCESS [0.101s]
[INFO] hadoop-yarn-project ............................... SUCCESS [2.474s]
[INFO] hadoop-mapreduce-client ........................... SUCCESS [0.036s]
[INFO] hadoop-mapreduce-client-core ...................... SUCCESS [13.362s]
[INFO] hadoop-mapreduce-client-common .................... SUCCESS [10.981s]
[INFO] hadoop-mapreduce-client-shuffle ................... SUCCESS [1.915s]
[INFO] hadoop-mapreduce-client-app ....................... SUCCESS [5.923s]
[INFO] hadoop-mapreduce-client-hs ........................ SUCCESS [5.442s]
[INFO] hadoop-mapreduce-client-jobclient ................. SUCCESS [25.624s]
[INFO] hadoop-mapreduce-client-hs-plugins ................ SUCCESS [1.048s]
[INFO] Apache Hadoop MapReduce Examples .................. SUCCESS [3.532s]
[INFO] hadoop-mapreduce .................................. SUCCESS [2.165s]
[INFO] Apache Hadoop MapReduce Streaming ................. SUCCESS [39.201s]
[INFO] Apache Hadoop Distributed Copy .................... SUCCESS [35.119s]
[INFO] Apache Hadoop Archives ............................ SUCCESS [1.774s]
[INFO] Apache Hadoop Rumen ............................... SUCCESS [3.939s]
[INFO] Apache Hadoop Gridmix ............................. SUCCESS [2.597s]
[INFO] Apache Hadoop Data Join ........................... SUCCESS [1.668s]
[INFO] Apache Hadoop Extras .............................. SUCCESS [1.795s]
[INFO] Apache Hadoop Pipes ............................... SUCCESS [6.558s]
[INFO] Apache Hadoop OpenStack support ................... SUCCESS [2.982s]
[INFO] Apache Hadoop Client .............................. SUCCESS [4.679s]
[INFO] Apache Hadoop Mini-Cluster ........................ SUCCESS [0.315s]
[INFO] Apache Hadoop Scheduler Load Simulator ............ SUCCESS [12.558s]
[INFO] Apache Hadoop Tools Dist .......................... SUCCESS [3.653s]
[INFO] Apache Hadoop Tools ............................... SUCCESS [0.019s]
[INFO] Apache Hadoop Distribution ........................ SUCCESS [17.143s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 17:50.583s
[INFO] Finished at: Thu Oct 08 10:45:03 CST 2015
[INFO] Final Memory: 150M/805M
[INFO] ------------------------------------------------------------------------
```

最后我们需要的包位于./hadoop-2.4.1-src/hadoop-dist/target下  
hadoop@artemis-02:~/wanglei/hadoop-2.4.1-src/hadoop-dist/target$ ls  
antrun  dist-layout-stitching.sh  dist-tar-stitching.sh  hadoop-2.4.1  hadoop-2.4.1.tar.gz  hadoop-dist-2.4.1.jar  hadoop-dist-2.4.1-javadoc.jar  javadoc-bundle-options  maven-archiver  test-dir