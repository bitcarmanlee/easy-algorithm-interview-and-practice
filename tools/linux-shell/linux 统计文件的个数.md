统计文件夹下的文件个数（当前目录与子目录）  

```
find ./ -type f | wc -l
ls -lR | grep "^-" | wc -l
```  

如果只是查找当前文件夹不递归  

```
find . -maxdepth 1 -type d | wc -l
```  