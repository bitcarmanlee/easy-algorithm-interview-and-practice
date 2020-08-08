## 求字符串长度：
```
$ x="a:b:c:"
方法一：
$ echo ${#x}
6
```  

```
方法二：用expr命令
$ expr length $x
6
```  

PS:expr属于外部命令，一般来说外部命令比内部命令要慢很多  
  
```
$ time for i in $(seq 1 10000);do len=${#x};done

real    0m0.087s
user    0m0.081s
sys    0m0.001s
```  

```
$ time for i in $(seq 1 10000);do len=$(expr length $x);done

real    0m13.313s
user    0m2.578s
sys    0m9.982s
```  


## 字符串拼接
```
$ echo $x"ddd"
a:b:c:ddd
```


## 查找字符串位置

返回的索引是从1开始, 失败则返回0  
```
$ expr index $x "a"
1
$ expr index $x "c"
5
expr index $x "d"
0
```


得到子字符串  
```
方法一：${x:pos:length},本人一般用这种方式，嘻嘻
$ echo ${x:0:4}
a:b:
$ echo ${x:0}
a:b:c:
$ echo ${x:2}
b:c:

方法二： expr substr <string> startpos length
$ expr substr "$x" 1 2
a:
$ expr substr "$x" 1 10
a:b:c:
```  

## 字符串替换  

非贪婪模式  
```
$ echo ${x/a/b}
b:b:c:
```  

贪婪模式  
```
$ xx="aaaaaa"
$ echo ${xx//a/b}
bbbbbb
```  

## 处理字符串的头尾  
```
$ zzz="this is a test"
```  

\# 表示去掉头，一个为非贪婪模式，两个为贪婪模式
```
$ echo ${zzz#t}
his is a test
$ echo ${zzz#t*h}
is is a test
$ echo ${zzz##t*s}
t
```  

%表示去掉尾，一个为非贪婪模式，两个为贪婪模式  
```
$ echo ${zzz%t}
this is a tes
$ echo ${zzz%s*t}
this is a te
$ echo ${zzz%e*t}
this is a t
$ echo ${zzz%%s*t}
thi
```  

## 去掉字符串最后一个字符
  
```
$ x='a:b:c:'
$ echo ${x%?}
a:b:c
```