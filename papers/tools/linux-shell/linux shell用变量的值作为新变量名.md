实例如下：  

```
path1="123abc"
i=1
pathstr=path$i
echo $pathstr
# 结果为path1
# 想将path1替换为123abc
path=`eval echo '$'"$pathstr"`
echo $path
```  

eval命令小结：  
eval命令将会首先扫描命令行进行所有的替换，憨厚再执行命令。该命令使用于那些一次扫描无法实现其功能的变量。该命令对变量进行两次扫描。这些需要进行两次扫描的变量有时候被称为复杂变量。  