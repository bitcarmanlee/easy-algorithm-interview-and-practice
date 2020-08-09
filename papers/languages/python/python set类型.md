## 1.set类型用途
在python中，dict是一种非常重要的数据结构，几乎无处不见。dict是一种典型的k-v结构，不管其中的元素多少，查找速度是非常快的，可以认为是近似的$O(1)$的查找速度而与dict本身的大小无关。  

在许多场景中，我们只关注dict的key，而对value不care，目的只是确保这个集合中元素的唯一性。这个时候，set就能派上用场了。set中是一系列元素的集合，这一点与list很类似。但是，set中的元素有最重要的两点性质：1.无序，这一点与dict很像，意味着就不能用索引访问里面的元素；2.没有重复元素，保证了里面元素的唯一性。  

## 2.set的一些简单用法
先看看如何初始化  

```
>>> x1 = set("abc")
>>> x1
set(['a', 'c', 'b'])
>>> x2 = set(['a','b','d','e'])
>>> x2
set(['a', 'b', 'e', 'd'])
>>> x3 = set("hello")
>>> x3
set(['h', 'e', 'l', 'o'])
```  

需要稍微注意的一点是，`x2 = set(['a','b','d','e'])`中，`['a','b','d','e']`是指传入的参数是一个list。而x2显示出来的`set(['a', 'b', 'e', 'd'])`只是说明set中有'a','b','c','d'四个元素，这个[]并不是表示一个list。  

从x3可以看出，重复元素在set中已经自动被干掉！  

如果要添加元素，可以有add或者update：  

```
>>> y = set("123")
>>> y
set(['1', '3', '2'])
>>> y.add("4")
>>> y
set(['1', '3', '2', '4'])
>>> y.update("456")
>>> y
set(['1', '3', '2', '5', '4', '6'])
```  

add不用多解释。update的解释如下：  

```
Update a set with the union of itself and others.
```  

不难看出，update是将两个set做并集的操作。或者说，是将一个set中的元素添加到原set中！而且由set的不重复性可知，不管是add操作还是update操作，都不会添加进重复元素！  

如果想要删除元素，可以用remove方法：  

```
>>> y.remove('1')
>>> y
set(['3', '2', '5', '4', '6'])
```  

需要注意的是，使用remove方法的时候，需要先判断元素在不在set中。如果元素不在集合中，会报KeyError的错误：  

```
>>> y.remove('a')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'a'
```  

## 3.遍历set
对于任意一种集合类型，遍历都是最基本也是最重要的操作。因为set是一种无序集合，所以遍历的时候，不能通过下标索引的方式。而且不同的机器，遍历出来的顺序也不尽相同：  

```
>>> x = set("abc")
>>> for i in x:
...     print i
...
a
c
b
```  

## 4.set求交并差集等操作
求两个set的并集：  

```
>>> x1 = set("abc")
>>> x2 = set("abde")
>>> x1 | x2
set(['a', 'c', 'b', 'e', 'd'])
>>> x1.union(x2)
set(['a', 'c', 'b', 'e', 'd'])
```  

求交集：  

```
>>> x1 & x2
set(['a', 'b'])
>>> x1.intersection(x2)
set(['a', 'b'])
```  

在x1中但不在x2中：  

```
>>> x1 - x2
set(['c'])
>>> x1.difference(x2)
set(['c'])
```  

不同时在x1,x2中出现：  

```
>>> x1 ^ x2
set(['c', 'e', 'd'])
>>> x1.symmetric_difference(x2)
set(['c', 'e', 'd'])
```  

## 5.set(dict)中的key只能为不可变对象
不管是set也好，还是dict也罢，里面的key只能为不可变对象。这一点非常重要！  
在python中，像数值型(number)，字符串(str)，元祖(tuple)为不可变类型(immutable)，而像列表(list)，字典(dict)，集合(set)等为可变类型(mutable)。  

看一个不可变类型的例子：  

```
>>>a = 1 #将名字a与内存中值为1的内存绑定在一起
>>>a = 2 #将名字a与内存中值为2的内存绑定在一起，而不是修改原来a绑定的内存中的值，这时，内存中值为1的内存地址引用计数-1，当引用计数为0时，内存地址被回收
>>>b = a #变量b执行与a绑定的内存
>>>b = 3 #创建一个内存值为3的内存地址与变量名字b进行绑定。这是a还是指向值为2的内存地址。
>>>a,b
>>>(2,3)
```  

再看一个可变类型的例子：  

```
def mutable(b = []): #函数使用了缺省变量
    b.append(0)
    return b
>>>mutable()
[0]
>>>mutable()
[0,0]
>>>mutable()
[0,0,0]
```  

对于set类型来说，所有的key均为不可变对象。如果添加可变对象，会报错：  

```
>>> x1 = set("abc")
>>> x1.add([1,2])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```  

我们在上面想对一个set添加一个list类型的元素，list是可变对象，所以unhashable无法添加成功！  