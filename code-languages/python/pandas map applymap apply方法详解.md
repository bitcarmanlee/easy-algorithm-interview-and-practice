## 0 前言

pandas的基本数据结构是Series与DataFrame。在数据处理过程中，对每个元素，或者每行/每列进行操作是尝尽的需求。而在pandas中，就内置了map,applymap,apply方法，可以满足上面的需求。接下来结合实际的例子，看看一些基本/常规/高大上的操作。  

## 1.map方法
map方法在数据处理中属于基本操作，重要性无须多言。map方法一般是对元素进行逐个操作，下面来看看几个例子。  

首先明确一点：map方法只能作用再Series上，不能作用在DataFrame上。换句话说，DataFrame没有map方法。  

Series中map方法的部分源码如下  
```
    def map(self, arg, na_action=None):
        """
        Map values of Series according to input correspondence.

        Used for substituting each value in a Series with another value,
        that may be derived from a function, a ``dict`` or
        a :class:`Series`.

        Parameters
        ----------
        arg : function, collections.abc.Mapping subclass or Series
            Mapping correspondence.
        na_action : {None, 'ignore'}, default None
            If 'ignore', propagate NaN values, without passing them to the
            mapping correspondence.

        Returns
        -------
        Series
            Same index as caller.

        See Also
        --------
        Series.apply : For applying more complex functions on a Series.
        DataFrame.apply : Apply a function row-/column-wise.
        DataFrame.applymap : Apply a function elementwise on a whole DataFrame.

        Notes
        -----
        When ``arg`` is a dictionary, values in Series that are not in the
        dictionary (as keys) are converted to ``NaN``. However, if the
        dictionary is a ``dict`` subclass that defines ``__missing__`` (i.e.
        provides a method for default values), then this default is used
        rather than ``NaN``.
```  

map方法的主要参数是arg，arg是一个方法或者字典，作用在每个元素上。  

看个例子：  

```
import numpy as np
import pandas as pd

def test():
    genders = ["male", "male", "female", "unknown", "female"]
    levels = ["L1", "L2", "L1", "L1", "L2"]
    df = pd.DataFrame({"gender": genders, "level": levels})

    gender_dic = {"male": "男", "female": "女", "unknown": "未知"}
    print(df)
    print("\n\n")
    df["gender"] = df["gender"].map(gender_dic)
    print(df)
```  

输出如下：  

```
    gender level
0     male    L1
1     male    L2
2   female    L1
3  unknown    L1
4   female    L2



  gender level
0      男    L1
1      男    L2
2      女    L1
3     未知    L1
4      女    L2
```  

上面的代码，是将gender这一列里的male映射成男，female映射成女，unknown映射成未知。  

```
def test():
    x = [i for i in range(1, 11)]
    y = [2*i + 0.5 for i in x]
    df = pd.DataFrame({'x': x, 'y': y})
    x2 = df['x']
    print(x2.map(lambda i: "%.2f" % i))
    print(x2.map(lambda i: "{:.2f}".format(i)))
```  

```
0     1.00
1     2.00
2     3.00
3     4.00
4     5.00
5     6.00
6     7.00
7     8.00
8     9.00
9    10.00
Name: x, dtype: object
0     1.00
1     2.00
2     3.00
3     4.00
4     5.00
5     6.00
6     7.00
7     8.00
8     9.00
9    10.00
Name: x, dtype: object
```  

上面的方法，则是将x变成带两位小数的浮点数。  

不论是利用字典还是函数进行映射，map方法都是把对应的数据逐个当作参数传入到字典或函数中，得到映射后的值。  

## 2.applymap方法
上面提到，dataframe没有map方法。要对dataframe中的元素实现类似map的功能，可以使用applymap方法。    

```
def t8():
    x = [i for i in range(1, 11)]
    y = [2*i + 0.5 for i in x]
    df = pd.DataFrame({'x': x, 'y': y})
    print(df)
    print()
    print(df.applymap(lambda i: "%.2f" % i))
```  

```
    x     y
0   1   2.5
1   2   4.5
2   3   6.5
3   4   8.5
4   5  10.5
5   6  12.5
6   7  14.5
7   8  16.5
8   9  18.5
9  10  20.5

       x      y
0   1.00   2.50
1   2.00   4.50
2   3.00   6.50
3   4.00   8.50
4   5.00  10.50
5   6.00  12.50
6   7.00  14.50
7   8.00  16.50
8   9.00  18.50
9  10.00  20.50

```  

前面的例子，是对x这一列做map操作，将x中的数值变成带两位小数的浮点数。如果我们想将dataframe中的x,y同时变成带两位小数的浮点数，可以使用applymap方法。  


## 3.apply方法
apply方法与map的功能类似，主要区别在于apply能传入功能更为复杂的函数。  

```
    def apply(self, func, convert_dtype=True, args=(), **kwds):
        """
        Invoke function on values of Series.

        Can be ufunc (a NumPy function that applies to the entire Series)
        or a Python function that only works on single values.

        Parameters
        ----------
        func : function
            Python function or NumPy ufunc to apply.
        convert_dtype : bool, default True
            Try to find better dtype for elementwise function results. If
            False, leave as dtype=object.
        args : tuple
            Positional arguments passed to func after the series value.
        **kwds
            Additional keyword arguments passed to func.

        Returns
        -------
        Series or DataFrame
            If func returns a Series object the result will be a DataFrame.

        See Also
        --------
        Series.map: For element-wise operations.
        Series.agg: Only perform aggregating type operations.
        Series.transform: Only perform transforming type operations.

```  

我们看一下apply方法的源码，首先方法签名为  

```
    def apply(self, func, convert_dtype=True, args=(), **kwds):
```  

与map的源码相比，apply除了可以输入func，还可以以元组的方式输入参数，这样能够输入功能更加复杂的函数。  

下面来看几个例子  

```
def square(x):
    return x**2

def test():
    s = pd.Series([20, 21, 12], index = ['London', 'New York', 'Helsinki'])
    s1 = s.apply(lambda x: x**2)
    s2 = s.apply(square)
    s3 = s.apply(np.log)

    print(s1)
    print()
    print(s2)
    print()
    print(s3)
```  

输出为  

```
London      400
New York    441
Helsinki    144
dtype: int64

London      400
New York    441
Helsinki    144
dtype: int64

London      2.995732
New York    3.044522
Helsinki    2.484907
dtype: float64
```  

上面的用法比较简单，跟map方法是一样的。  

再看一个复杂一些的例子

```
def BMI(series):
    weight = series['weight']
    height = series['height'] / 100
    BMI_Rate = weight / height**2
    return BMI_Rate

def test():
    heights = [180, 175, 169, 158, 185]
    weights = [75, 72, 68, 60, 76]
    age = [30, 18, 26, 42, 34]
    df = pd.DataFrame({"height": heights, "weight": weights, "age": age})
    print(df)
    print()
    df['BMI'] = df.apply(BMI, axis=1)
    print(df)
```  

输出结果为

```
   height  weight  age
0     180      75   30
1     175      72   18
2     169      68   26
3     158      60   42
4     185      76   34

   height  weight  age        BMI
0     180      75   30  23.148148
1     175      72   18  23.510204
2     169      68   26  23.808690
3     158      60   42  24.034610
4     185      76   34  22.205990
```  

数据中包括身高体重，然后计算BMI指数=体重/身高的平方。  
上面的apply方法在调用的时候，指定了axis=1，就是对每行进行操作。如果不容易的理解的同学可以这么想:axis=1要消除的是列的维度，保留行的维度，所以是对每行的数据进行操作。apply方法在运行时，实际上就是调用BMI方法对每行数据进行操作。  

```
def subtract_custom_value(x, custom_value):
    return x - custom_value

def test():
    s = pd.Series([20, 21, 12], index = ['London', 'New York', 'Helsinki'])
    print(s)
    print()
    s1 = s.apply(subtract_custom_value, args=(5,))
    print(s1)
```  

输出结果为  

```
London      20
New York    21
Helsinki    12
dtype: int64

London      15
New York    16
Helsinki     7
dtype: int64
```  

上面代码运行的时候，就是将每个值减去5，因为要传入参数5，所以map方法此时就无能为力。  

## 4.总结
1.map方法是针对Series的基本操作，dataframe无map方法。  
2.dataframe如果要针对每个元素做map操作，可以使用applymap。  
3.apply方法更为灵活，可以同时作用于series与dataframe。同时可以以元组的形式传入参数。  