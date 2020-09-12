## 1.lambda函数初探
lambda函数又名匿名函数。顾名思义，匿名函数，那肯定就是没有函数名称啦。先看个最简单的例子：  
先写个正常的函数：  

```
def f(x):
    return x+1
```  

很简单，不解释。如果写成lambda函数：  

```
g = lambda x:x+1
print g
print g(2)
```  

```
<function <lambda> at 0x1007cc668>
3
```  

由此可见g确实是个函数对象。lambda函数都是以lambda开头，后面接参数，参数后面再接冒号，冒号后面则是函数返回的具体内容。  

当然也可以在lambda函数中指定多个参数：  

```
f = lambda x,y:x+y+1
print "the result is: ", f(2,3)
```  

```
the result is:  6
```  

## 2.为什么要用lambda函数
很多人说，lambda函数只是省略了函数名而已。而且这样的匿名函数，又不能在别的地方被调用，那干嘛还要使用lambda函数呢？  
一个东西既然存在，肯定有他存在的合理性与必然性。根据我的使用感受来看，使用lambda函数主要有以下优点：  
1.省略了函数名。什么，这不是优点？拜托，请问写代码最难的部分是什么？之前github上做过类似调查，结果"给变量/函数命名"的选项遥遥领先！给变量/函数取个短小精悍容易理解又能正确反应其含义的名字是件很困难的事情好不好！尤其是那些只调用一次的函数，给它起个靠谱的名字，真的是太困难了。lambda函数正好就派上了用场。  
2.在有些场合，省略了函数定义的过程，代码更加简洁而且容易理解。  

总结起来看的话，lambda函数更多起的是润滑剂或者语法糖的作用，让使用者更为方便。在很多场合，lambda函数也可以用其他方式实现，但那样可能会付出代码更为复杂的代价。  

## 3.与map函数结合
map函数的官方定义如下：  

Return a list of the results of applying the function to the items of the argument sequence(s).  If more than one sequence is given, the function is called with an argument list consisting of the corresponding item of each sequence, substituting None for missing values when not all sequences have the same length.  If the function is None, return a list of the items of the sequence (or a list of tuples if more than one 
 sequence).    
 
为大家翻译一把：map函数返回一个结果列表，结果列表里的每个元素是将序列参数里的每个元素传给map中调用的方法求出的。如果参数中包括不止一个序列，那个map中调用的方法的参数将由一个list组成，每个参数对应每个序列的每个元素。当序列长度不相等时，对应的缺失值为None。如果map中没有调用方法，返回的是序列本身（如果序列参数不止一个，返回的是一个列表元祖)。  
  
上面翻译得不是很接地气，给大家举个例子就清楚了：  

```
ret_list = map(lambda x:x+1,[1,2,3])
print "ret_list is: ",ret_list
```  

```
ret_list is:  [2, 3, 4]
```  

上面的例子中，map函数有两个参数，一个lambda方法，lambda方法返回的是x+1；另外的参数是一个列表，map函数做的事，就是对列表项中的每个数字进行加1的操作，最后返回一个列表。  

## 4.lambda函数转化为列表解析
当然，上面例子中map函数中的lambda方法，可以使用列表解析的方式来实现。  

```
print [x+1 for x in range(1,4)]
```  

这样写，更简洁明了。对于一般人而言，也比lambda更容易理解。另外，列表解析的速度也很快，是非常pythonic的写法。  

## 5.lambda函数需要注意的细节
有如下的代码：  

```
fs = [ lambda n: i+n for i in range(5) ]

for k in range(5):
    print "fs[%d]: " %k,fs[k](4)
```  

此时的输出为：  

```
fs[0]:  8
fs[1]:  8
fs[2]:  8
fs[3]:  8
fs[4]:  8
```  

怪哉。咋不符合预期勒。其实问题就出在变量i上面。因为lambda函数中没有指定参数i，所以这时输入的i为全局变量！  

这么写就OK了：  

```
fl = [ (lambda n,i=i: i+n) for i in range(5)]
for k in range(5):
    print "fl[%d]: " %k,fl[k](4)
```  

```
fl[0]:  4
fl[1]:  5
fl[2]:  6
fl[3]:  7
fl[4]:  8
```  
