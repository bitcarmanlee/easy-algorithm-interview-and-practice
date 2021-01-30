## 1.分组groupby
在日常数据分析过程中，经常有分组的需求。具体来说，就是根据一个或者多个字段，将数据划分为不同的组，然后进行进一步分析，比如求分组的数量，分组内的最大值最小值平均值等。在sql中，就是大名鼎鼎的groupby操作。  
pandas中，也有对应的groupby操作，下面我们就来看看pandas中的groupby怎么使用。  

## 2.groupby的数据结构
首先我们看如下代码  

```
def ddd():
    levels = ["L1", "L1", "L1", "L2", "L2", "L3", "L3"]
    nums = [10, 20, 30, 20, 15, 10, 12]
    df = pd.DataFrame({"level": levels, "num": nums})
    g = df.groupby('level')
    print(g)
    print()
    print(list(g))
```  

输出结果如下：  

```
<pandas.core.groupby.generic.DataFrameGroupBy object at 0x10f6f96d0>

[('L1',   level  num
0    L1   10
1    L1   20
2    L1   30), ('L2',   level  num
3    L2   20
4    L2   15), ('L3',   level  num
5    L3   10
6    L3   12)]
```  

做groupby操作以后，得到的是一个DataFrameGroupBy对象，直接打印该对象的话，显示的是其内存地址。  
为了方便地观察数据，我们使用list方法转换一下，发现其是一个元组，元组中的第一个元素，是level的值。元祖中的第二个元素，则是其组别下的整个dataframe。  

## 3.groupby的基本用法
```
def group1():
    levels = ["L1", "L1", "L1", "L2", "L2", "L3", "L3"]
    nums = [10, 20, 30, 20, 15, 10, 12]
    scores = [100, 200, 300, 200, 150, 100, 120]
    df = pd.DataFrame({"level": levels, "num": nums, "score": scores})
    result = df.groupby('level').agg({'num': 'sum', 'score': 'mean'})
    allnum = result['num'].sum()
    result['rate'] = result['num'].map(lambda x: x / allnum)
    print(result)
```  

最后输出：  

```
       num  score      rate
level                      
L1      60    200  0.512821
L2      35    175  0.299145
L3      22    110  0.188034
```  

上面的例子展示了groupby的基本用法。  
对dataframe按照level分组，然后对num列求和，对score列求平均值，可以得到result。  
同时，我们还希望得到每个分组中，num的和在所有num和中的占比。于是我们先求num的综合，然后在用map方法，给result添加一列，求得其占比！  

## 4.transform的用法

下面我们看一个更复杂的例子。  

```
def t10():
    levels = ["L1", "L1", "L1", "L2", "L2", "L3", "L3"]
    nums = [10, 20, 30, 20, 15, 10, 12]
    df = pd.DataFrame({"level": levels, "num": nums})
    ret = df.groupby('level')['num'].mean().to_dict()
    df['avg_num'] = df['level'].map(ret)
    print(ret)
    print(df)
```  

```
{'L1': 20.0, 'L2': 17.5, 'L3': 11.0}
  level  num  avg_num
0    L1   10     20.0
1    L1   20     20.0
2    L1   30     20.0
3    L2   20     17.5
4    L2   15     17.5
5    L3   10     11.0
6    L3   12     11.0
```  

上面的方法，我们对level分组以后，我们想给数据集添加一列，想给每行数据添加每个level对应的平均值。  
上面的解法是先求得每个分组的平均值，转成一个dict，然后再使用map方法将每组的平均值添加上去。  

```
def trans():
    levels = ["L1", "L1", "L1", "L2", "L2", "L3", "L3"]
    nums = [10, 20, 30, 20, 15, 10, 12]
    df = pd.DataFrame({"level": levels, "num": nums})
    df['avg_num'] = df.groupby('level')['num'].transform('mean')
    print(df)
```  
如果使用transform方法，代码可以更简单更直观，如上所示。  

transform方法的作用：调用函数在每个分组上产生一个与原df相同索引的dataFrame，整体返回与原来对象拥有相同索引且已填充了转换后的值的dataFrame，相当于就是给原来的dataframe添加了一列。  

