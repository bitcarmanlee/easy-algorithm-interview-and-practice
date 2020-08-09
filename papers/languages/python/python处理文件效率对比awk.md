有如下三文件：

```
wc -l breakfast_all cheap_all receptions_all
   3345271 breakfast_all
   955890 cheap_all
   505504 receptions_all
  4806665 总用量

head -3 cheap_all
a    true
b    true
c    true
```  

三个文件的结构都类似，第一列为uid。现在想统计三个文件中总共有多少不重复的uid。特意用python与awk分别写了代码，测试两者处理文本的速度。  

python代码：  


```
#!/usr/bin/env python
#coding:utf-8

import time

def t1():
    dic = {}
    filelist = ["breakfast_all","receptions_all","cheap_all"]
    start = time.clock()
    for each in filelist:
        f = open(each,'r')
        for line in f.readlines():
            key = line.strip().split()[0]
            if key not in dic:
                dic[key] = 1

    end = time.clock()
    print len(dic)
    print 'cost time is: %f' %(end - start)

def t2():
    uid_set = set()
    filelist = ["breakfast_all","receptions_all","cheap_all"]
    start = time.clock()
    for each in filelist:
        f = open(each,'r')
        for line in f.readlines():
            key = line.strip().split()[0]
            uid_set.add(key)

    end = time.clock()
    print len(uid_set)
    print 'cost time is: %f' %(end - start)

t1()
t2()
```  

用awk处理  

```
#!/bin/bash

function handle()
{
    start=$(date +%s%N)
    start_ms=${start:0:16}
    awk '{a[$1]++} END{print length(a)}' breakfast_all receptions_all cheap_all
    end=$(date +%s%N)
    end_ms=${end:0:16}
    echo "cost time is:"
    echo "scale=6;($end_ms - $start_ms)/1000000" | bc
}

handle
```  


运行python脚本  
```
./test.py
3685715
cost time is: 4.890000
3685715
cost time is: 4.480000
```  


运行sh脚本  

```
./zzz.sh
3685715
cost time is:
4.865822
```  

由此可见，python里头的set结构比dic稍微快一点点。整体上，awk的处理速度与python的处理速度大致相当！

