## 1.前言
pandas可以将读取到的数据(不一定是csv或者txt)转换成dataframe，然后后面可以方便地对dataframe进行操作，进行各种数据分析工作。下面我们对pandas里常用的一些IO操作进行详细的分析。  

## 2.read_csv
read_csv最常用的方式是从文件中读取数据，read_csv默认的分隔符号是逗号  
示例数据:  

```
57647:0.059819,26223:0.048002,100295:0.055268,60232:0.049508
35824:0.04753,57776:0.055802,40677:0.049119,14445:0.040235
102136:0.052933,3736:0.07613,21681:0.10266,44816:0.058018
```  

不指定列名称  

```
def read11():
    data = pd.read_csv("../data/tt3", header=None)
    print data
```  

```
                 0               1                2               3
0   57647:0.059819  26223:0.048002  100295:0.055268  60232:0.049508
1    35824:0.04753  57776:0.055802   40677:0.049119  14445:0.040235
2  102136:0.052933    3736:0.07613    21681:0.10266  44816:0.058018
```  

指定列名称  

```
def read12():
    data = pd.read_csv("../data/tt3", header=None, names=['c1', 'c2', 'c3', 'c4'])
    print data
```  

```
                c1              c2               c3              c4
0   57647:0.059819  26223:0.048002  100295:0.055268  60232:0.049508
1    35824:0.04753  57776:0.055802   40677:0.049119  14445:0.040235
2  102136:0.052933    3736:0.07613    21681:0.10266  44816:0.058018
```  
上面的数据都不带表头，所以设置header=None  

## 3.read_table
read_csv默认的分隔符是逗号，如果想改变分隔符，可以用read_table指定分隔符  

数据  

```
8803b236442fed8a37a5beb04556f684	54530	1	0
f4afa2b8f50e8aacf967628b3dc11bff	102017	1	0
4077bb0001ba73f4dd966a7f6fb46075	50276	1	0
```  

代码  

```
def read21():
    data = pd.read_table("../data/tt1", header=None, sep='\t')
    print data


def read22():
    data = pd.read_table("../data/tt1", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4'])
    print data


read21()
read22()
```  

```
 FutureWarning: read_table is deprecated, use read_csv instead.
  data = pd.read_table("../data/tt1", header=None, sep='\t')
                                  0       1  2  3
0  8803b236442fed8a37a5beb04556f684   54530  1  0
1  f4afa2b8f50e8aacf967628b3dc11bff  102017  1  0
2  4077bb0001ba73f4dd966a7f6fb46075   50276  1  0
FutureWarning: read_table is deprecated, use read_csv instead.
  data = pd.read_table("../data/tt1", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4'])
                                 c1      c2  c3  c4
0  8803b236442fed8a37a5beb04556f684   54530   1   0
1  f4afa2b8f50e8aacf967628b3dc11bff  102017   1   0
2  4077bb0001ba73f4dd966a7f6fb46075   50276   1   0

```  

根据提示来看，read_table方法后面会被废弃，统一用read_csv方法。  

## 4.设置索引

```
def read31():
    data = pd.read_csv("../data/tt3", header=None, names=['c1', 'c2', 'c3', 'c4'], index_col='c2')
    print data


read31()
```

```
                             c1               c3              c4
c2                                                              
26223:0.048002   57647:0.059819  100295:0.055268  60232:0.049508
57776:0.055802    35824:0.04753   40677:0.049119  14445:0.040235
3736:0.07613    102136:0.052933    21681:0.10266  44816:0.058018
```  

跟之前的结果对比，如果设置了index_col来设置列索引，原来默认从0开始的整数索引不见了。之前没设置索引的时候，默认是按行号从0开始设置索引的。  


```
def read32():
    data = pd.read_csv("../data/tt3", header=None, names=['c1', 'c2', 'c3', 'c4'], index_col=['c2', 'c1'])
    print data

```  

```
                                             c3              c4
c2             c1                                              
26223:0.048002 57647:0.059819   100295:0.055268  60232:0.049508
57776:0.055802 35824:0.04753     40677:0.049119  14445:0.040235
3736:0.07613   102136:0.052933    21681:0.10266  44816:0.058018
```  

上面的例子为指定多个列为索引  

## 5.缺失值删除
实际数据肯定会比较脏，不会特别干净，有缺失值的情况很常见，填充缺失值就成了数据预处理中一项很重要的工作。  
pandas在读取文件时，默认会将NA, NULL等特殊字符串当成缺失值，默认会使用NaN进行替换。  

数据如下  
```
8803b236442fed8a37a5beb04556f684	54530	1	0	abc	NULL
f4afa2b8f50e8aacf967628b3dc11bff	102017	1	0	NULL	NULL
4077bb0001ba73f4dd966a7f6fb46075	50276	1	0	NULL	NULL
4077bb0001ba73f4dd966a7f6fb46075	50276	1	0	456	123
```  

```
def read41():
    data = pd.read_table("../data/tt2", header=None, sep='\t')
    print data
```  

```
                                  0       1  2  3    4      5
0  8803b236442fed8a37a5beb04556f684   54530  1  0  abc    NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017  1  0  NaN    NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276  1  0  NaN    NaN
3  4077bb0001ba73f4dd966a7f6fb46075   50276  1  0  456  123.0
```  

### 5.1删除含有缺失值的行与列  

```
def read42():
    data = pd.read_table("../data/tt2", header=None, sep='\t')
    print data.dropna()
```  

```
                                  0      1  2  3    4      5
3  4077bb0001ba73f4dd966a7f6fb46075  50276  1  0  456  123.0
```  

dropna删除含有缺失值的行。如果想删除含有缺失值的列，可以指定axis=1  

```
def read42():
    data = pd.read_table("../data/tt2", header=None, sep='\t')
    print data.dropna(axis=1)
```  

```
                                  0       1  2  3
0  8803b236442fed8a37a5beb04556f684   54530  1  0
1  f4afa2b8f50e8aacf967628b3dc11bff  102017  1  0
2  4077bb0001ba73f4dd966a7f6fb46075   50276  1  0
3  4077bb0001ba73f4dd966a7f6fb46075   50276  1  0
```  

### 5.2删除全为NaN的行或者列
数据如下  

```
8803b236442fed8a37a5beb04556f684	54530	1	0	abc	NULL
f4afa2b8f50e8aacf967628b3dc11bff	102017	1	0	NULL	NULL
4077bb0001ba73f4dd966a7f6fb46075	50276	1	0	NULL	NULL
NULL	NaN	NULL	NULL	NULL	NULL
```  

```
def read43():
    data = pd.read_table("../data/tt2", header=None, sep='\t')
    print data.dropna(how='all')
    print data.dropna(how='all', axis=1)
```  

```
                                  0         1    2    3    4   5
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  NaN NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  NaN NaN
                                  0         1    2    3    4
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  NaN
3                               NaN       NaN  NaN  NaN  NaN
```  

## 6.缺失值填充
更多的时候，我们是需要对缺失值进行填充而不是删除，下面看看怎么填充缺失值。    

数据  

```
8803b236442fed8a37a5beb04556f684	54530	1	0	abc	NULL
f4afa2b8f50e8aacf967628b3dc11bff	102017	1	0	NULL	NULL
4077bb0001ba73f4dd966a7f6fb46075	50276	1	0	NULL	NULL
NULL	NaN	NULL	NULL	NULL	NULL
```  

### 6.1 所有缺失值按相同值填充

```
def read51():
    data = pd.read_table("../data/tt2", header=None, sep='\t')
    print data.fillna(0)
```  

```
                                  0         1    2    3    4    5
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc  0.0
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0    0  0.0
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0    0  0.0
3                                 0       0.0  0.0  0.0    0  0.0
```  


### 6.2 不同列填充不同值
上面的填充方式太过简单粗暴，实际中我们一般不会这么干，而是会按照不同列填充会比较多。  

```
def read52():
    data = pd.read_table("../data/tt2", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4', 'c5', 'c6'])
    print data.fillna({'c3': 'c3default', 'c4': 'c4default'})
```  

```
                                 c1        c2         c3         c4   c5  c6
0  8803b236442fed8a37a5beb04556f684   54530.0          1          0  abc NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0          1          0  NaN NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0          1          0  NaN NaN
3                               NaN       NaN  c3default  c4default  NaN NaN
```  

## 6.3 前向填充与后向填充

```
def read53():
    data = pd.read_table("../data/tt2", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4', 'c5', 'c6'])
    print data.fillna(method='ffill')
    print data.fillna(method='bfill')
```  

```
                                 c1        c2   c3   c4   c5  c6
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  abc NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  abc NaN
3  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  abc NaN
                                 c1        c2   c3   c4   c5  c6
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  NaN NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  NaN NaN
3                               NaN       NaN  NaN  NaN  NaN NaN
```  

ffill为前向填充，使用默认是上一行的值,设置axis=1可以使用列进行填充  
bfill为后向填充，使用下一行的值,不存在的时候就不填充  


## 6.4 使用列均值填充

```
def read54():
    data = pd.read_table("../data/tt2", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4', 'c5', 'c6'])
    print data.fillna(data.mean())
```  

```
                                 c1        c2   c3   c4   c5  c6
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  NaN NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  NaN NaN
3                               NaN   68941.0  1.0  0.0  NaN NaN
```  

## 7.跳过某些行

```
8803b236442fed8a37a5beb04556f684	54530	1	0	abc	NULL
test
f4afa2b8f50e8aacf967628b3dc11bff	102017	1	0	NULL	NULL
test
4077bb0001ba73f4dd966a7f6fb46075	50276	1	0	NULL	NULL
NULL	NaN	NULL	NULL	NULL	NULL
```  

```
def read61():
    data1 = pd.read_table("../data/tt2", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4', 'c5', 'c6'])
    print data1
    data2 = pd.read_table("../data/tt2", header=None, sep='\t', names=['c1', 'c2', 'c3', 'c4', 'c5', 'c6'], skiprows=[1, 3])
    print data2
```  

```
                                 c1        c2   c3   c4   c5  c6
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc NaN
1                              test       NaN  NaN  NaN  NaN NaN
2  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  NaN NaN
3                              test       NaN  NaN  NaN  NaN NaN
4  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  NaN NaN
5                               NaN       NaN  NaN  NaN  NaN NaN

                                 c1        c2   c3   c4   c5  c6
0  8803b236442fed8a37a5beb04556f684   54530.0  1.0  0.0  abc NaN
1  f4afa2b8f50e8aacf967628b3dc11bff  102017.0  1.0  0.0  NaN NaN
2  4077bb0001ba73f4dd966a7f6fb46075   50276.0  1.0  0.0  NaN NaN
3                               NaN       NaN  NaN  NaN  NaN NaN
```  

## 8.读取json
数据为  

```
{
  "apples": {
      "June": 3,
      "Robert": 2,
      "Lily": 0,
      "David": 1
  },
  "oranges": {
      "June": 0,
      "Robert": 3,
      "Lily": 7,
      "David": 2
  }
}
```  

```
def read71():
    data = pd.read_json("../data/tt2")
    print data
```  

```
        apples  oranges
David        1        2
June         3        0
Lily         0        7
Robert       2        3
```  

