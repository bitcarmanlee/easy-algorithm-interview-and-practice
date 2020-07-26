在hadoop的MR相关代码中，经常需要获得mapper输入的文件名，从而针对不同的文件进行不同的操作。下面简单地介绍一下如果在MR代码中获取文件名  

## 1.在streaming中获取文件名
实际中经常用python开发streaming程序，在python代码中可以用如下方式获得文件名：  

```
import os

filepath = os.environ["mapreduce_map_input_file"]
```  

通过上面的代码即可达到获取文件名的目的，通过代码也很容易看出，文件名保存在名为mapreduce_map_input_file的环境变量中。  

需要稍微注意的地方有两点：  
1.filepath保存的是文件在hdfs上的完整路径。  
2.新版本的api为mapreduce_map_input_file，老版本的api为map_input_file，在集群上尝试了老版本的api，代码会报错。  

## 2.在java代码中获取文件名
在java代码中获取文件名，需要得到input split 所在的文件名，需要从map函数中的context参数着手。  

```
// 获取 input split 所在的文件名
private String getFileName(MapContext context) {
    return ((FileSplit) context.getInputSplit()).getPath().getName();
}
```  

如果需要获得在hdfs上的绝对路径，可以用以下代码实现：  

```
String filepath = ((FileSplit)context.getInputSplit()).getPath().toString();
```  

获取文件名的大致流程为：Context(map函数里) → InputSplit → FileSplit → Path → String(file name)。  