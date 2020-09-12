## 1.zip函数的定义  
zip是python中的一个内建函数，平时用得不是太多。zip的签名如下:  

```
def zip(seq1, seq2, *more_seqs): # known special case of zip
    """
    zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]
    
    Return a list of tuples, where each tuple contains the i-th element
    from each of the argument sequences.  The returned list is truncated
    in length to the length of the shortest argument sequence.
    """
    pass
```  

从python源码中可以看出zip的大致用途:输入是n个序列，返回的是一个由tuples组成的list，每个tuple是输入序列中的第i个元素。如果输入的序列长度不一样，那么返回的列表将按输入序列中最短的那个做截断。  

## 2.用法示范
### 2.1 矩阵进行转置

```
>>>a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```  

上述列表可以描述一个二维矩阵  
采用列表的方式，我们可以完成矩阵转置的需求  

```
>>> [ [row[col] for row in a] for col in range(len(a[0]))]
[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```  

还可以通过zip的方式:  

```
>>> zip(*a)
[(1, 4, 7), (2, 5, 8), (3, 6, 9)]
```  

上面的操作是利用*这个操作符，将list做unzip操作。  
因为列表里的类型是tuple，将tuple转换成list即可：  

```
>>> map(list, zip(*a))
[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```  

### 2.2 生成字典  

```
>>> keys = [1, 2, 3]
>>> values = ['a', 'b', 'c']
>>> d = dict(zip(keys, values))
>>> d
{1: 'a', 2: 'b', 3: 'c'}
```  
