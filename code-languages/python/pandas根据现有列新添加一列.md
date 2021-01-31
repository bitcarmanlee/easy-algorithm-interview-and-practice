pandas中一个Dataframe，经常需要根据其中一列再新建一列，比如一个常见的例子：需要根据分数来确定等级范围，下面我们就来看一下怎么实现。  

```
def getlevel(score):
    if score < 60:
        return "bad"
    elif score < 80:
        return "mid"
    else:
        return "good"


def test():
    data = {'name': ['lili', 'lucy', 'tracy', 'tony', 'mike'],
            'score': [85, 61, 75, 49, 90]
            }
    df = pd.DataFrame(data=data)
    # 两种方式都可以
    # df['level'] = df.apply(lambda x: getlevel(x['score']), axis=1)
    df['level'] = df.apply(lambda x: getlevel(x.score), axis=1)

    print(df)
```  

上面代码运行结果  

```
    name  score level
0   lili     85  good
1   lucy     61   mid
2  tracy     75   mid
3   tony     49   bad
4   mike     90  good
```  

要实现上面的功能，主要是使用到dataframe中的apply方法。  
上面的代码，对dataframe新增加一列名为level，level由分数一列而来，如果小于60分为bad，60-80之间为mid，80以上为good。  
其中axis=1表示原有dataframe的行不变，列的维数发生改变。  