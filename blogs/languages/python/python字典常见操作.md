1.按value对dic进行排序,返回一个列表，列表的元素是k-v对：  

```
list_open = sorted(dic_open_app.items(),key = lambda d:d[1],reverse = True)
```  

2.为整个dic设置默认值：  

```
from collections import defaultdict
dic_device = defaultdict(int)
```  

3.用dict函数生成字典：  
```
>>> a=[1,2,3]
>>> b=['a','b','c']
>>> zip(a,b)
[(1, 'a'), (2, 'b'), (3, 'c')]
>>> dict(zip(a,b))
{1: 'a', 2: 'b', 3: 'c'}
```


