## 1.测试数据

```
1457822940      0       0       44      36
422692440       0       0       3       3
1460826600      0       0       7       6
1410115140      -1      3       25      7
1161370800      0       0       18      14
996746700       0       0       30      25
1115896320      0       0       441     123
64954980        0       0       7       7
2307334696      0       0       2       2
417770700       0       0       1       1
```  

## 2.获取行数，列数，元素个数等

```
def test():
        names = ['c1', 'c2', 'c3', 'c4', 'c5']
        df = pd.read_csv("testdata", sep="\t", header=None, names=names)
        print(df.info())
        print("\n")
        print("len is: ", len(df))
        print("columns is: ", df.columns)
        print("shape is: ", df.shape)
        print("size is: ", df.size)
```  

代码输出结果：  

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   c1      10 non-null     int64
 1   c2      10 non-null     int64
 2   c3      10 non-null     int64
 3   c4      10 non-null     int64
 4   c5      10 non-null     int64
dtypes: int64(5)
memory usage: 528.0 bytes
None


len is:  10
columns is:  Index(['c1', 'c2', 'c3', 'c4', 'c5'], dtype='object')
shape is:  (10, 5)
size is:  50
```  

其中，info()方法包含了很多信息，包括类型，column信息,non-null的个数，数据类型，内存占用等。  

len(df)可以获取dataframe的行数  
columns可以获取column相关的信息  
shape是个二元元组，包括行列信息，所以如果想得到dataframe的行列数据可以通过shape获取。  
size则是整个dataframe的元素个数。  
