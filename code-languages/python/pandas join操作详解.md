## 1.前言
join操作是关系型数据库中最核心没有之一的操作，实际中最容易出问题，经常需要优化的点也是join操作。如果我们将dataframe类比为一张表，自然也会涉及到join操作，而且非常非常常见。下面我们就来仔细看看pandas中的join用法。  

## 2.join方法原型
pandas源码中join方法的签名如下  

```
    def join(
        self, other, on=None, how="left", lsuffix="", rsuffix="", sort=False
    ) -> "DataFrame":
        """
        Join columns of another DataFrame.

        Join columns with `other` DataFrame either on index or on a key
        column. Efficiently join multiple DataFrame objects by index at once by
        passing a list.

        Parameters
        ----------
        other : DataFrame, Series, or list of DataFrame
            Index should be similar to one of the columns in this one. If a
            Series is passed, its name attribute must be set, and that will be
            used as the column name in the resulting joined DataFrame.
        on : str, list of str, or array-like, optional
            Column or index level name(s) in the caller to join on the index
            in `other`, otherwise joins index-on-index. If multiple
            values given, the `other` DataFrame must have a MultiIndex. Can
            pass an array as the join key if it is not already contained in
            the calling DataFrame. Like an Excel VLOOKUP operation.
        how : {'left', 'right', 'outer', 'inner'}, default 'left'
            How to handle the operation of the two objects.

            * left: use calling frame's index (or column if on is specified)
            * right: use `other`'s index.
            * outer: form union of calling frame's index (or column if on is
              specified) with `other`'s index, and sort it.
              lexicographically.
            * inner: form intersection of calling frame's index (or column if
              on is specified) with `other`'s index, preserving the order
              of the calling's one.
        lsuffix : str, default ''
            Suffix to use from left frame's overlapping columns.
        rsuffix : str, default ''
            Suffix to use from right frame's overlapping columns.
        sort : bool, default False
            Order result DataFrame lexicographically by the join key. If False,
            the order of the join key depends on the join type (how keyword).

        Returns
        -------
        DataFrame
            A dataframe containing columns from both the caller and `other`.

```  

 def join(self, other, on=None, how="left", lsuffix="", rsuffix="", sort=False)   
 其中  
 other：DataFrame, Series, or list of DataFrame，另外一个dataframe, series，或者dataframe list。  
 on: 参与join的列，与sql中的on参数类似。  
 how:  {'left', 'right', 'outer', 'inner'}, default 'left'， 与sql中的join方式类似。  
 lsuffix: 左DataFrame中重复列的后缀  
 rsuffix: 右DataFrame中重复列的后缀  
 sort: 按字典序对结果在连接键上排序  

## 3.按指定列进行join
实际中最常见的join方式为按某个相同列进行join。我们先来尝试一个简单的join实例  

```
import pandas as pd

def joindemo():
    age_df = pd.DataFrame({'name': ['lili', 'lucy', 'tracy', 'mike'],
                           'age': [18, 28, 24, 36]})
    score_df = pd.DataFrame({'name': ['tony', 'mike', 'akuda', 'tracy'],
                             'score': ['A', 'B', 'C', 'B']})

    result = age_df.join(score_df, on='name')
    print(result)
```  

上面的代码会报如下错误：  

```
ValueError: You are trying to merge on object and int64 columns. If you wish to proceed you should use pd.concat
```  

原因在于，join的时候会根据dataframe的索引进行。如果不理解，下面看一段测试代码就明白  

```
def joindemo2():
    age_df = pd.DataFrame({'name': ['lili', 'lucy', 'tracy', 'mike'],
                           'age': [18, 28, 24, 36]})
    score_df = pd.DataFrame({'name': ['tony', 'mike', 'akuda', 'tracy'],
                             'score': ['A', 'B', 'C', 'B']})
    print(age_df)
    age_df.set_index('name', inplace=True)
    print(age_df)
```  

上面这段代码运行的结果如下  

```
    name  age
0   lili   18
1   lucy   28
2  tracy   24
3   mike   36
       age
name      
lili    18
lucy    28
tracy   24
mike    36
```  

dataframe默认的index是从0开始递增的整数，前面的数字0,1,2,3表示的就是index。如果我们指定index为name，输出的dataframe结构就发生了改变，前面递增的数字就没有了。  


如果要实现最开始的join需求，可以按如下代码  

```
def joindemo():
    age_df = pd.DataFrame({'name': ['lili', 'lucy', 'tracy', 'mike'],
                           'age': [18, 28, 24, 36]})
    score_df = pd.DataFrame({'name': ['tony', 'mike', 'akuda', 'tracy'],
                             'score': ['A', 'B', 'C', 'B']})

    age_df.set_index('name', inplace=True)
    score_df.set_index('name', inplace=True)
    result = age_df.join(score_df, on='name')
    print(result)
```  

代码的输出结果为  

```
       age score
name            
lili    18   NaN
lucy    28   NaN
tracy   24     B
mike    36     B
```  

默认的为left join，这就实现了我们上面的需求。  

## 4.按默认自增index进行join

如果想按默认的自增index进行join，我们接下来进行尝试。  

```
def joindemo():
    age_df = pd.DataFrame({'name': ['lili', 'lucy', 'tracy', 'mike'],
                           'age': [18, 28, 24, 36]})
    score_df = pd.DataFrame({'name': ['tony', 'mike', 'akuda', 'tracy'],
                             'score': ['A', 'B', 'C', 'B']})

    result = age_df.join(score_df)
    print(result)
```  

上面的代码也会报错  

```
ValueError: columns overlap but no suffix specified: Index(['name'], dtype='object')
```  

这个时候，就需要lsuffix,rsuffix参数了  

```
def joindemo():
    age_df = pd.DataFrame({'name': ['lili', 'lucy', 'tracy', 'mike'],
                           'age': [18, 28, 24, 36]})
    score_df = pd.DataFrame({'name': ['tony', 'mike', 'akuda', 'tracy'],
                             'score': ['A', 'B', 'C', 'B']})

    result = age_df.join(score_df, lsuffix='_left', rsuffix='_right')
    print(result)
```

```
  name_left  age name_right score
0      lili   18       tony     A
1      lucy   28       mike     B
2     tracy   24      akuda     C
3      mike   36      tracy     B
```  

## 5.与merge的区别
pandas中还有merge方法，也能实现join的功能。他们的具体区别，可以参考如下链接：  
https://stackoverflow.com/questions/22676081/what-is-the-difference-between-join-and-merge-in-pandas
