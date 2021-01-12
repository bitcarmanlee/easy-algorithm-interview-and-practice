## 1.loc用法

loc是基于行的index，可以选择特定的行，同时还可以根据列名称选定指定列。  
iloc是基于行/列的位置(position)来进行选择  

```
def select_test():
    a = [i for i in range(10)]
    b = [2*x + 0.1 for x in a]
    data = {"x": a, "y": b}
    tmp = pd.DataFrame(data, index=["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"])
    print(tmp.index)
    print(tmp.columns)
    print()
    return tmp
```  

方法的输出结果为  

```
Index(['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10'], dtype='object')
Index(['x', 'y'], dtype='object')
```  

用loc方法选择第一行  

```
tmp = select_test()
print(tmp.loc["r1"])
```  

输出结果  

```
x    0.0
y    0.1
Name: r1, dtype: float64
```  

用loc方法选择前三行，并只选择x列：  

```
print(tmp.loc[["r1", "r2", "r3"], "x"])
```  

```
r1    0
r2    1
r3    2
Name: x, dtype: int64
```  

如果用loc[1]方法，会报错  

```
TypeError: cannot do label indexing on <class 'pandas.core.indexes.base.Index'> with these indexers [1] of <class 'int'>
```  


## 2.iloc用法  
选择前五行  

```
print(tmp.iloc[0:5])
```  

```
    x    y
r1  0  0.1
r2  1  2.1
r3  2  4.1
r4  3  6.1
r5  4  8.1
```  

选择前五行的第二列(第一列的索引为0):  

```
print(tmp.iloc[0:5, 1:2])
```  

```
      y
r1  0.1
r2  2.1
r3  4.1
r4  6.1
r5  8.1
```  

```
print(tmp.iloc[0:5, "x"])
```  

上面这行代码会报错:  

```
ValueError: Location based indexing can only have [integer, integer slice (START point is INCLUDED, END point is EXCLUDED), listlike of integers, boolean array] types
```  

原因很简单，iloc只能用行列的起始位置进行选择，不能使用行列名。  

## 3.ix
ix在旧版本中，是loc与iloc的混合体，既支持位置选择也支持列名选择。  
在新版本中，该方法已经被废弃。个人觉得，也应该被废弃。API太灵活带来的必然后果就是代码不规范，可读性差。  

## 4.索引快速选择
还有快速选择行/列的方式  

```
print(tmp[0:5])
print(tmp[['x', 'y']])
```  

```
    x    y
r1  0  0.1
r2  1  2.1
r3  2  4.1
r4  3  6.1
r5  4  8.1
     x     y
r1   0   0.1
r2   1   2.1
r3   2   4.1
r4   3   6.1
r5   4   8.1
r6   5  10.1
r7   6  12.1
r8   7  14.1
r9   8  16.1
r10  9  18.1
```  

其中，第一行代码选择前5行数据，第二行代码选择x,y两列数据。  

## 5.at/iat方法
at可以根据行index及列名，快速选择dataframe中的某个元素：  

```
print(tmp.at["r3", "x"])
```  

输出为  

```
2
```  
如果使用如下代码会报错  

```
print(tmp.at[3, "x"])
```  

```
ValueError: At based indexing on an non-integer index can only have non-integer indexers
```  

与iloc类似，iat也是通过位置(position)定位元素  

```
print(tmp.iat[0, 0])
```  

输出为  

```
0
```  
