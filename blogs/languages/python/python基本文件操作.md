获取当前路径  
```
>>> import os
>>> os.getcwd()
'/home/lei.wang/merge_user_labels'
>>> os.path.abspath('.')
'/home/lei.wang/merge_user_labels'
>>> os.path.abspath(os.curdir)
'/home/lei.wang/merge_user_labels'
```

获取上层路径    
```
>>> os.path.abspath('..')
'/home/lei.wang'
```  

将path分割成目录和文件名二元组返回。  
```
>>> os.path.split('/home/webopa/lei.wang/datas/datas_stable/good_rate')
('/home/webopa/lei.wang/datas/datas_stable', 'good_rate')
```  

返回path的目录。其实就是os.path.split(path)的第一个元素。  
```
>>> os.path.dirname('/home/webopa/lei.wang/datas/datas_stable/good_rate')
'/home/webopa/lei.wang/datas/datas_stable'
```  

返回path最后的文件名。如何path以／或\结尾，那么就会返回空值。即os.path.split(path)的第二个元素。  
```
>>> os.path.basename('/home/webopa/lei.wang/datas/datas_stable/good_rate')
'good_rate'
```  

改变路径  
```
>>> os.chdir('/home/lei.wang/datas')
>>> os.getcwd()
'/home/lei.wang/datas'
```  
这样大部分的文件操作现在是相对于 /home/lei.wang/datas 来了，例如fobj = open('Hello.txt')，实际上打开的是/home/lei.wang/datas/Hello.txt  


判断是否是文件  
```
>>> os.path.isfile('/home/webopa/lei.wang/datas/datas_stable/good_rate')
True
>>> os.path.isfile('/home/webopa/lei.wang/datas/datas_stable')
False
```  

判断是否是文件夹  
```
>>> os.path.isdir('/home/webopa/lei.wang/datas/datas_stable/good_rate')
False
>>> os.path.isdir('/home/webopa/lei.wang/datas/datas_stable')
True
```  

判断路径是否存在（包括文件以及文件夹）  
```
>>> os.path.exists('/home/webopa/lei.wang/datas/datas_stable/good_rate')
True
>>> os.path.exists('/home/webopa/lei.wang/datas/datas_stable')
True
```  

返回文件的大小  
```
>>> os.path.getsize('/home/webopa/lei.wang/datas/datas_stable/good_rate')
751
```  

返回path所指向的文件或者目录的最后存取时间    
```
>>> os.path.getatime('/home/webopa/lei.wang/datas/datas_stable')
1458617090.3319671
```  

返回path所指向的文件或者目录的最后修改时间  
```
>>> os.path.getmtime('/home/webopa/lei.wang/datas/datas_stable/good_rate')
1457424457.9110916
```