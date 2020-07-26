想put文件到hdfs上，遇到org.apache.hadoop.fs.ChecksumException: Checksum error的问题  

```
hadoop fs -put cheap_all /tmp/wanglei/cheap  

16/03/24 09:27:52 INFO fs.FSInputChecker: Found checksum error: b[0, 4096]=31303030323037333809747275650a313030303730313939...
org.apache.hadoop.fs.ChecksumException: Checksum error: file:/home/lei.wang/datas/datas_user_label/cheap_all at 0 exp: 1966038764 got: 1549100153
    at org.apache.hadoop.fs.FSInputChecker.verifySums(FSInputChecker.java:323)
    at org.apache.hadoop.fs.FSInputChecker.readChecksumChunk(FSInputChecker.java:279)
    at org.apache.hadoop.fs.FSInputChecker.read1(FSInputChecker.java:228)
    at org.apache.hadoop.fs.FSInputChecker.read(FSInputChecker.java:196)
    at java.io.DataInputStream.read(DataInputStream.java:83)
    at org.apache.hadoop.io.IOUtils.copyBytes(IOUtils.java:78)
    at org.apache.hadoop.io.IOUtils.copyBytes(IOUtils.java:52)
    at org.apache.hadoop.io.IOUtils.copyBytes(IOUtils.java:112)
    at org.apache.hadoop.fs.shell.CommandWithDestination$TargetFileSystem.writeStreamToFile(CommandWithDestination.java:456)
    at org.apache.hadoop.fs.shell.CommandWithDestination.copyStreamToTarget(CommandWithDestination.java:382)
    at org.apache.hadoop.fs.shell.CommandWithDestination.copyFileToTarget(CommandWithDestination.java:319)
    at org.apache.hadoop.fs.shell.CommandWithDestination.processPath(CommandWithDestination.java:254)
    at org.apache.hadoop.fs.shell.CommandWithDestination.processPath(CommandWithDestination.java:239)
    at org.apache.hadoop.fs.shell.Command.processPaths(Command.java:306)
    at org.apache.hadoop.fs.shell.Command.processPathArgument(Command.java:278)
    at org.apache.hadoop.fs.shell.CommandWithDestination.processPathArgument(CommandWithDestination.java:234)
    at org.apache.hadoop.fs.shell.Command.processArgument(Command.java:260)
    at org.apache.hadoop.fs.shell.Command.processArguments(Command.java:244)
    at org.apache.hadoop.fs.shell.CommandWithDestination.processArguments(CommandWithDestination.java:211)
    at org.apache.hadoop.fs.shell.CopyCommands$Put.processArguments(CopyCommands.java:263)
    at org.apache.hadoop.fs.shell.Command.processRawArguments(Command.java:190)
    at org.apache.hadoop.fs.shell.Command.run(Command.java:154)
    at org.apache.hadoop.fs.FsShell.run(FsShell.java:287)
    at org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:70)
    at org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:84)
    at org.apache.hadoop.fs.FsShell.main(FsShell.java:340)
put: Checksum error: file:/home/xxx/cheap_all at 0 exp: 1966038764 got: 1549100153
```

经过一番查找，找出问题所在。  

Hadoop客户端将本地文件cheap_all上传到hdfs上时，hadoop会通过fs.FSInputChecker判断需要上传的文件是否存在.crc校验文件。如果存在.crc校验文件，则会进行校验。如果校验失败，自然不会上传该文件。  

cd到文件所在路径，ls -a查看，果然存在.cheap_all.crc文件  
```
$ ls -a
.  ..  breakfast_all  cheap_all  .cheap_all.crc  hive_data  receptions_all  .receptions_all.crc
```

问题就很简单了，删除.crc文件
```  
$ rm .cheap_all.crc
```  

再上传，搞定收工。  