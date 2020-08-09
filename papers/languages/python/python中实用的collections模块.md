## 1.Counter类
Counter类是hashtable对象的计数，是dict的子类，从2.7以后的版本加入。  
计数器是我们常用的一个功能，collections中的Counter类就提供了此功能。  

```
>>> from collections import *
>>> a = Counter()
>>> b = Counter("aabbcccd")
>>> c = Counter({"a":10,"b":20})
>>> d = Counter(a=10,b=20)
>>> b["a"]
2
>>> c.most_common()
[('b', 20), ('a', 10)]
```  

## 2.defaultdict类
defaultdict使用工厂函数创建字典，使用的时候不用考虑缺失的key。从2.5版本后引入。  
python原生的dict结构，如果使用d[key]的方式访问，需要先判断key是否存在。如果key在字典中不存在，会抛出一个KeyError的异常。  
defaultdict就是为解决这个痛点而生的。只要传入一个默认的工厂方法，如果用d[key]的方式访问字典而key不存在，会调用这个工厂方法使用其结果来作为这个key的默认值。  

```
#!/usr/bin/env python
#coding:utf-8

from collections import *

def test_defaultdict():
    members = [
    ['male', 'John'],
    ['male', 'Jack'],
    ['female', 'Lily'],
    ['male', 'Pony'],
    ['female', 'Lucy']
    ]

    result_dic = defaultdict(list)

    for sex,name in members:
        result_dic[sex].append(name)

    for k,v in result_dic.items():
        print k,"\t",v

test_defaultdict()
```  

最后的输出为：  

```
male 	['John', 'Jack', 'Pony']
female 	['Lily', 'Lucy']
```  

## 3.OrderedDict类
排序字典，是字典的子类。从2.7版本后引入。  
在python中，dict，set等数据结构的key是hash无序的。有时候，我们需要得到排序的字典。collections中的OrderedDict类即可满足我们的上述需求。  

```
#!/usr/bin/env python
#coding:utf-8

from collections import *

def test_orderdict():
    raw_dic = {"watermelon":4,"grape":3,"apple":1,"mango":2}
    ret_dic_by_key = OrderedDict(sorted(raw_dic.items(),key = lambda item:item[0]))
    ret_dic_by_value = OrderedDict(sorted(raw_dic.items(),key = lambda item:item[1]))
    ret_dic_by_keylen = OrderedDict(sorted(raw_dic.items(),key = lambda item:len(item[0])))

    print "ret_dic_by_key is: "
    for k,v in ret_dic_by_key.items():
        print k,"\t",v

    print "ret_dic_by_value is: "
    for k,v in ret_dic_by_value.items():
        print k,"\t",v

    print "ret_dic_by_keylen is: "
    for k,v in ret_dic_by_keylen.items():
        print k,"\t",v

test_orderdict()
```  

将代码run起来以后：  

```
ret_dic_by_key is:
apple 	1
grape 	3
mango 	2
watermelon 	4
ret_dic_by_value is:
apple 	1
mango 	2
grape 	3
watermelon 	4
ret_dic_by_keylen is:
grape 	3
mango 	2
apple 	1
watermelon 	4
```  

## 4.namedtuple
namedtuple，命名元组，是一个工厂函数。从2.6版本后引入。  
namedtuple主要用来产生可以使用名称来访问元素的数据对象，通常用来增强代码的可读性， 在访问一些tuple类型的数据时尤其好用。  

```
#!/usr/bin/env python
#coding:utf-8

from collections import *

def test_namedtuple():
    Point = namedtuple('Point','x y')
    location = [10,20]
    p = Point._make(location)
    print p
    print "p.x is: ",p.x
    print "p.y is: ",p.y


test_namedtuple()
```  

将代码run起来以后：  

```
Point(x=10, y=20)
p.x is:  10
p.y is:  20
```  

## 5.deque
deque，双端队列，从2.4版本后引入。  
双端队列（deque）是一种支持向两端高效地插入数据、支持随机访问的容器。它最大的好处就是实现了从队列 头部快速增加和取出对象: .popleft(), .appendleft() 。  
从piglei同志的博客中摘取一个deque的例子：  

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
下面这个是一个有趣的例子，主要使用了deque的rotate方法来实现了一个无限循环
的加载动画
"""
import sys
import time
from collections import deque

fancy_loading = deque('>--------------------')

while True:
    print '\r%s' % ''.join(fancy_loading),
    fancy_loading.rotate(1)
    sys.stdout.flush()
    time.sleep(0.08)

# Result:

# 一个无尽循环的跑马灯
------------->-------
```  
