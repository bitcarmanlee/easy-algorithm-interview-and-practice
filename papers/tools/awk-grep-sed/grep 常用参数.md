grep的基本使用方式：  

```
grep 'xxx' file
grep 'xxx1 xxx2' file
cat file | grep 'xxx'
pip | grep 'xxx'
```  

测试文本111  
```
$ cat 111
abc
Abc
ABC
abc123
123
```

不加任何参数  
```
$ grep 'abc' 111
abc
abc123
```  

忽略大小写  
```
$ grep -i 'abc' 111
abc
Abc
ABC
abc123
```  

输出匹配行号  
```
$ grep -n 'abc' 111
1:abc
4:abc123
```  

输出匹配行数  
```
$ grep -c 'abc' 111
2
```  

输出不匹配行  
```
$ grep -v 'abc' 111
Abc
ABC
123
```  

在指定目录下递归查找  
```
$ grep -r 'abc' dir
```  

正则匹配  
```
$ grep -E '[Aa]bc' 111
abc
Abc
abc123
```  

单词匹配  
```
$ grep -w 'abc' 111
abc
```  

用颜色高亮匹配  
```
$ grep --color 'abc' 111
abc
abc123
```  
上面两行中的'abc'会以彩色显示  



