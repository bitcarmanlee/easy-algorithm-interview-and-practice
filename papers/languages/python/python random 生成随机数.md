代码中经常有一些生成随机数的需求。特意整理了一下python中random模块的一些相关用法。  

## python生成随机数  

随机整数：  

```
>>> import random
>>> random.randint(0,99)
21
```  

随机选取0到100间的偶数：  

```
>>> import random
>>> random.randrange(0, 101, 2)
42
```  

随机浮点数：  

```
>>> import random
>>> random.random() 
0.85415370477785668 范围0-1.0
>>> random.uniform(1, 10)
5.4221167969800881
```  

## 选择一个随机元素

```
>>> random.choice("abc")
'b'
```  

## 将一个列表中的元素打乱  

```
>>> p = ["Python","is", "powerful","simple", "and so on..."]  
>>> random.shuffle(p)   
>>> print p
['and so on...', 'Python', 'powerful', 'is', 'simple']
```  

## 从指定序列中随机获取指定长度片段

```
>>> list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> a=random.sample(list,5)
>>> a
[5, 2, 9, 1, 3]
>>> list
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```  

## 随机字符：

```
>>> import random
>>> random.choice('abcdefg&#%^*f')
'd'
```  

## 多个字符中选取特定数量的字符：

```
>>> import random
random.sample('abcdefghij',3) 
['a', 'd', 'b']
```  

## 多个字符中选取特定数量的字符组成新字符串：

```
>>> import random
>>> import string
>>> string.join(random.sample(['a','b','c','d','e','f','g','h','i','j'], 3)).replace(" ","")
'fih'
```  

## 随机选取字符串：

```
>>> import random
>>> random.choice ( ['apple', 'pear', 'peach', 'orange', 'lemon'] )
'lemon'
```  

## 洗牌：

```
>>> import random
>>> items = [1, 2, 3, 4, 5, 6]
>>> random.shuffle(items)
>>> items
[3, 2, 5, 6, 4, 1]
```  


