假设有如下文件：  

```
#!/bin/sh

myPath="/home/xxx/path"
myFile="/home/xxx/xxx.log"
```  

-d 参数判断$myPath是否存在  

```
if [ ! -d "$myPath"]; then
mkdir "$myPath"
fi
```  

-f参数判断$myFile是否存在  

```
if [ ! -f "$myFile" ]; then
touch "$myFile"
fi
```  

-x 参数判断$myPath是否存在并且是否具有可执行权限  

```
if [ ! -x "$myPath"]; then
mkdir "$myPath"
fi
```  

判断字符串是否为空  

```
#!/bin/bash                                                                                                                                            

str1="123"
if [ -z "$str1" ] ; then
    str1="aaa"
    echo "EMPTY"
else
    echo "NO_EMPTY"
fi
```  

判断字符串是否相等  

```
#!/bin/bash                                                                                                                                            

if [ "$str1" = "$str2" ]
then
    echo "YES"
else
    echo "NO"
fi
```  