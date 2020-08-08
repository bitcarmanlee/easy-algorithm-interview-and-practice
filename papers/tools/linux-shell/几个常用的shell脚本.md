## 1.选择文件大小大于某个值的文件
有一个文件夹里有若干文件，打印文件大小大于300B的文件名。  

```
#!/bin/bash

for file in `ls -l | awk '$5>300 {print $9}'`
do
    echo $file
done
```  

## 2.某个文件夹中找到.py结尾的文件取10个，并取所有文件的第一行

```
#!/bin/bash

for file in `find dir -type f -name "*.py" | head -n 10`
do
    sed -n '1p' $file >> result_file
done
```  

稍微接一下：dir表示要查找的路径，-type表示查找的是file，-name表示名称。sed -n '1p'表示取第一行。  

## 3.打印fileB中有fileA中没有的行
方法1:用awk的方法  

```
awk 'NR==FNR{a[$0]++} NR>FNR{if(!($0 in a)) print $0}' file1 file2
```  

方法2:使用grep  

```
grep -vxFf file1 file2
```  

grep选取-v表示不选择匹配的行，-x表示只打印整行匹配的行，-F表示匹配的模式按行分割，-f a表示匹配模式来自文件file1，最后表示目标文件file2  