在写项目相关的解释文档或者说明文档或者需求文档的时候，经常需要列出项目代码的树状结构。tree命令就能很好的满足我们这个小小的需求  

linux与mac中的tree都不是自带的，需要自行安装。如果不会安装，请自行google在linux或者mac中怎样安装软件即可。。。  

## 1.最简单的方式
最简单的使用方式就是直接输入`tree`命令了 ：  

```
$ tree
.
├── get_user_order.sh
├── mr.py
├── test
│   ├── mr.py
│   ├── subtest
│   │   └── a.txt
│   └── zzz.sh
├── zzzfile
└── zzz.sh

2 directories, 7 files
```  

会把当前目录中所有的文件夹以及文件都遍历出来。当然，大部分情况下我们还会有别的需求，请接着往下看。  

## 2.-L选项
-L选项是我实际中使用最多的参数。因为很多情况下可能文件夹的层数非常多，我不希望看到后面所有的文件夹，这个时候用-L选项即可搞定。  

```
$ tree -L 1
.
├── get_user_order.sh
├── mr.py
├── test
├── zzzfile
└── zzz.sh

1 directory, 4 files
```  

-L后面跟一个数字，比如现在指定为1，表示最多看当前目录下一层目录。  

## 3.-d选项

```
$ tree -d
.
└── test
    └── subtest

2 directories
```  

只看文件夹，不解释。  

## 4.-I选项
实际中还经常想忽略某些内容，这个时候-I就派上了用场。  

```
$ tree -I zzzfile
.
├── get_user_order.sh
├── mr.py
├── test
│   ├── mr.py
│   ├── subtest
│   │   └── a.txt
│   └── zzz.sh
└── zzz.sh

2 directories, 6 files
```  

如果要忽略多个，也很简单  

```
$ tree -I "zzzfile|a.txt"
.
├── get_user_order.sh
├── mr.py
├── test
│   ├── mr.py
│   ├── subtest
│   └── zzz.sh
└── zzz.sh

2 directories, 5 files
```