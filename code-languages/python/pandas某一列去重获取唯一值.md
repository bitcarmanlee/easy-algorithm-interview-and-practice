去重获取唯一值是常见的需求，下面我们看看pandas里面如何实现去重。  
直接看代码  

```
import pandas as pd

def test():
    df = pd.DataFrame({"c1": [1, 1, 2, 3, 1], "c2": [10, 20, 30, 40, 50]})
    print(df)
    print()
    result = df['c1'].unique()
    print(result)
    print(type(result))
    print(result.tolist())
    print()

    ret = df[df['c1'] == 1]['c2'].unique()
    print(ret)
    print(type(ret))
```  

运行上面的代码，得到如下结果  

```
   c1  c2
0   1  10
1   1  20
2   2  30
3   3  40
4   1  50

[1 2 3]
<class 'numpy.ndarray'>
[1, 2, 3]

[10 20 50]
<class 'numpy.ndarray'>
```  

具体分析：  
1.如果要对某列去重获取谓一致，可以直接获取该列然后调用unique()方法即可。  
2.unique()方法得到的对象是numpy.ndarray类型，后续可以调用tolist方法转换为一个列表。  
3.如果我们想得到c1列值为1的情况下，c2列的去重置，可以先使用过滤逻辑df['c1'] == 1会返回True/False。 条件匹配时为真，条件不匹配时为假。 稍后它在df内传递并返回与True对应的所有行，然后按照前面的方法，取c2列再去重即可。  
