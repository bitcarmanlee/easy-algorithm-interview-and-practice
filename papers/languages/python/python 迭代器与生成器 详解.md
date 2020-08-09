在python中，我们经常使用for循环来遍历各种集合，例如最常用的有list，dict等等，这些集合都是可迭代对象。我们先来了解一下python中的迭代器(Iterator)。  

## 一、迭代器
顾名思义，迭代器，自然就是用来做迭代用的（好像是废话）。以list为例，我们用list，最多的情况就是用来做循环了（循环就是迭代嘛）  

```
>>> list = [1,2,3]
>>> dir(list)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```  
list就有\__iter__方法。如果调用此方法，则会返回一个迭代器  

```
>>> it = list.__iter__()
>>> it
<listiterator object at 0x10fa12950>
>>> dir(it)
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__length_hint__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'next']
```  

所谓迭代器，是指具有next方法的对象。注意调用next方式的时候，不需要任何参数。调用next方法时，迭代器会返回它的下一个值。如果迭代器没有值返回，则会抛出StopIteration的异常。  

```
>>> it.next()
1
>>> it.next()
2
>>> it.next()
3
>>> it.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```  

有的同学会问，我们用list用得好好的，为什么要用什么iterator？因为list是一次性获得所有值，如果这个列表很大，需要占用很大内存空间，甚至大到内存装载不下；而迭代器则是在迭代（循环）中使用一个计算一个，对内存的占用显然小得多。  

### 用迭代器实现Fibonacci数列

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年5月6日

@author: lei.wang
'''

class Fibonacci(object):
    def __init__(self):
        self.a = 0
        self.b = 1
        
    def next(self):
        self.a,self.b = self.b,self.a + self.b
        print self.a
        return self.a
    
    def __iter__(self):
        return self
    
if __name__ == '__main__':
    fib = Fibonacci()
    for n in fib:
        if n > 10:
            #print n
            break

```  

刚才我们讲的都是从列表转为迭代器，那从迭代器能变成列表么？答案是当然可以，请看：  

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年5月6日

@author: lei.wang
'''

class MyIterator(object):
    index = 0
    
    def __init__(self):
        pass
    
    def next(self):
        self.index += 1
        if self.index > 10:
            raise StopIteration
        return self.index
    
    def __iter__(self):
        return self
    
if __name__ == '__main__':
    my_interator = MyIterator()
    my_list = list(my_interator)
    print my_list
    
```  

```
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```  

## 二、生成器
当我们调用一个普通的python函数时（其实不光是python函数，绝大部分语言的函数都是如此)，一般都是从函数的第一行开始执行，直到遇到return语句或者异常或者函数的最后一行。这样，函数就将控制权交还与调用者，函数中的所有工具以及局部变量等数据都将丢失。再次调用这个函数的时候，所有的局部变量，堆栈信息都将重新创建，跟之前的调用再无关系。  

有时候我们并不希望函数只返回一个值，而是希望返回一个序列，比如前面的fibonacci序列。要做到这一点，这种函数需要能够保存自己的工作状态。这样的话，就不能使用我们通常所使用的return语句，因为一旦使用return语句，代码执行的控制权就交给了函数被调用的地方，函数的所有状态将被清零。在这种情况下，我们就需要使用yield关键字。含有yield关键字的地方，就是一个生成器。  


在python中，生成器通过生成器函数生成，生成器函数定义的方法跟普通函数定义的方法一致。唯一不同的地方是，生成器函数不用return返回，而是用yield关键字一次返回一个结果，在每个结果之间挂起与继续他们的状态，来自动实现迭代（循环）。  

废话说了这一大堆，直接上代码，show me the code:  

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年5月6日

@author: lei.wang
'''

def myXrange(n):
    print "myXrange beginning!"
    i = 0
    while i < n:
        print "before yield, i is: ",i
        yield i
        i += 1
        print "after yield, i is: ",i
    print "myXrange endding!"        
    
def testMyXrange():
    my_range = myXrange(3)
    print my_range
    print "--------\n"
    
    print my_range.next()
    print "--------\n"
    
    print my_range.next()
    print "--------\n"
    
    print my_range.next()
    print "--------\n"    
    
    print my_range.next()
    print "--------\n"
    
testMyXrange()
```  

代码运行的结果  

```
<generator object myXrange at 0x10b3f6b90>
--------

myXrange beginning!
before yield, i is:  0
0
--------

after yield, i is:  1
before yield, i is:  1
1
--------

after yield, i is:  2
before yield, i is:  2
2
--------

after yield, i is:  3
myXrange endding!
Traceback (most recent call last):
  File "/Users/lei.wang/code/java/pydevttt/leilei/bit/interview/myGenerator.py", line 37, in <module>
    testMyXrange()
  File "/Users/lei.wang/code/java/pydevttt/leilei/bit/interview/myGenerator.py", line 34, in testMyXrange
    print my_range.next()
StopIteration

```  

有代码运行的结果，我们很容易看出：  
1.当调用生成器函数时候，函数返回的，只是一个生成器对象，并没有真正执行里面的逻辑。  
2.当next()方法第一次被调用以后，生成器才真正开始工作。一旦遇到yield语句，代码便停止运行。注意此时的停止运行跟return的是不一样的。  
3.调用next()方法的时候，返回的是yield处的参数值  
4.当继续调用next()方法时，代码将在上一次停止的yield语句处继续执行，并且到下一个yield处停止。  
5.一直到后面没有yield语句，最后抛出StopIteration的异常。  

生成器其实对我们来说并不陌生，请看：  
以大家都比较熟悉的列表解析式为例：  

```
>>> list=[i for i in range(10)]
>>> list
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> type(list)
<type 'list'>
```  

将方括号改为圆括号：  

```
>>> gen=(i for i in range(3))
>>> gen
<generator object <genexpr> at 0x10c4a19b0>
>>> gen.next()
0
>>> gen.next()
1
>>> gen.next()
2
>>> gen.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```  

大伙看到没有，这就是一个典型的生成器。  

再举一个我们常见的例子：  
大家都经常使用range生成一个列表做循环。注意range生成的是一个列表。那如果这个列表很大，大到内存都无法放下。那么，我们这个时候需要使用xrange了。xrange产生的就是一个生成器，就不受内存的限制。。。  

用生成器产生Fibonacci序列：  

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年5月6日

@author: lei.wang
'''
class Fibonacci_generator(object):
    def __init__(self):
        self.a = 0
        self.b = 1
    
    def get_num(self):
        while True:
            self.a,self.b = self.b,self.a+self.b
            print self.a
            yield self.a

if __name__ == '__main__':
    fib = Fibonacci_generator()
    for n in fib.get_num():
        if n > 10:
            break

```  

运行上面的代码：  

```
1
1
2
3
5
8
13

```  