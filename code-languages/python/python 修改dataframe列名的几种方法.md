实际开发中经常有修改dataframe列名的需求，特意总结了如下可用的几种方法。  

```
import pandas as pd


def t1():
    df = pd.DataFrame({'c1':[1, 2, 3], 'c2': [4, 5, 6]})
    print(df)

    df.columns = ['d1', 'd2']
    print(df)

    df.rename(columns={'d1': 'e1', 'd2': 'e2'}, inplace=True)
    print(df)

    df = df.rename(columns={'e1': 'f1', 'e2': 'f2'})
    print(df)


t1()
```  

上面代码的输出：  

```
   c1  c2
0   1   4
1   2   5
2   3   6
   d1  d2
0   1   4
1   2   5
2   3   6
   e1  e2
0   1   4
1   2   5
2   3   6
   f1  f2
0   1   4
1   2   5
2   3   6
```  

由上面的代码可以看出，修改列名的两种方式为：  
1.直接使用df.columns的方式重新命名，不过这种方式需要列出所有列名。  
2.使用rename方法，注意如果需要原地修改需要带上inplace=True的参数，否则原dataframe列名不会发生改变。  