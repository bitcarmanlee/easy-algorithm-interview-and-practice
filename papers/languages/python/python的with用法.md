## 1.With语句是什么?
有一些任务，可能事先需要设置，事后做清理工作。对于这种场景，Python的with语句提供了一种非常方便的处理方式。一个很好的例子是文件处理，你需要获取一个文件句柄，从文件中读取数据，然后关闭文件句柄。  

如果不用with语句，代码如下：  

```
file = open("/tmp/foo.txt")
data = file.read()
file.close()
```  

这里有两个问题:  

一是可能忘记关闭文件句柄；  
二是文件读取数据发生异常，没有进行任何处理。  

下面是处理异常的加强版本：  

```
try:
    f = open('xxx')
except:
    print 'fail to open'
    exit(-1)
try:
    do something
except:
    do something
finally:
     f.close()
```  

虽然这段代码运行良好，但是太冗长了。  

这时候就是with一展身手的时候了。除了有更优雅的语法，with还可以很好的处理上下文环境产生的异常。  

下面是with版本的代码：  

```
with open("/tmp/foo.txt") as file:
    data = file.read()
```  

## 2.with如何工作?
紧跟with后面的语句被求值后，返回对象的 \__enter__() 方法被调用，这个方法的返回值将被赋值给as后面的变量。  
当with后面的代码块全部被执行完之后，将调用前面返回对象的 \__exit__()方法。  

下面例子可以具体说明with如何工作：  

```
#!/usr/bin/env python
# with_example01.py
class Sample:
    def __enter__(self):
        print "In __enter__()"
        return "Foo"
    def __exit__(self, type, value, trace):
        print "In __exit__()"
def get_sample():
    return Sample()
with get_sample() as sample:
    print "sample:", sample
```  

运行代码，输出如下  

```
bash-3.2$ ./with_example01.py
In __enter__()
sample: Foo
In __exit__()
```  

正如你看到的: 1. \__enter__()方法被执行 2. \__enter__()方法返回的值 - 这个例子中是”Foo”，赋值给变量’sample’ 3. 执行代码块，打印变量”sample”的值为 “Foo” 4. \__exit__()方法被调用  
 
with真正强大之处是它可以处理异常。可能你已经注意到Sample类的 \__exit__ 方法有三个参数 val, type 和 trace。 这些参数在异常处理中相当有用。我们来改一下代码，看看具体如何工作的。  

```
#!/usr/bin/env python
# with_example02.py
class Sample:
    def __enter__(self):
        return self
    def __exit__(self, type, value, trace):
        print "type:", type
        print "value:", value
        print "trace:", trace
    def do_something(self):
        bar = 1/0
        return bar + 10
with Sample() as sample:
    sample.do_something()
```  

这个例子中，with后面的get_sample()变成了Sample()。这没有任何关系，只要紧跟with后面的语句所返回的对象有 \__enter__() 和 \__exit__() 方法即可。此例中，Sample()的 \__enter__() 方法返回新创建的Sample对象，并赋值给变量sample。  

代码执行后：  

```
bash-3.2$ ./with_example02.py
type: <type 'exceptions.ZeroDivisionError'>
value: integer division or modulo by zero
trace: <traceback object at 0x1004a8128>
Traceback (most recent call last):
  File "./with_example02.py", line 19, in <module>
    sample.do_something()
  File "./with_example02.py", line 15, in do_something
    bar = 1/0
ZeroDivisionError: integer division or modulo by zero
```  

实际上，在with后面的代码块抛出任何异常时，\__exit__() 方法被执行。正如例子所示，异常抛出时，与之关联的type，value和stack trace传给 \__exit__() 方法，因此抛出的ZeroDivisionError异常被打印出来了。开发库时，清理资源，关闭文件等等操作，都可以放在 \__exit__ 方法当中。  

另外，\__exit__ 除了用于tear things down，还可以进行异常的监控和处理，注意后几个参数。要跳过一个异常，只需要返回该函数True即可。  

下面的样例代码跳过了所有的TypeError，而让其他异常正常抛出。  

```
def __exit__(self, type, value, traceback):
    return isinstance(value, TypeError)
```  

上文说了 \__exit__ 函数可以进行部分异常的处理，如果我们不在这个函数中处理异常，他会正常抛出，这时候我们可以这样写（python 2.7及以上版本，之前的版本参考使用contextlib.nested这个库函数）：  

```
try:
    with open( "a.txt" ) as f :
        do something
except xxxError:
    do something about exception
```  

总之，with-as表达式极大的简化了每次写finally的工作，这对保持代码的优雅性是有极大帮助的。  

如果有多个项，我们可以这么写：  

```
with open("x.txt") as f1, open('xxx.txt') as f2:
    do something with f1,f2
```  

因此，Python的with语句是提供一个有效的机制，让代码更简练，同时在异常产生时，清理工作更简单。  

## 3.相关术语
要使用 with 语句，首先要明白上下文管理器这一概念。有了上下文管理器，with 语句才能工作。  
下面是一组与上下文管理器和with 语句有关的概念。  
上下文管理协议（Context Management Protocol）：包含方法 \__enter__() 和 \__exit__()，支持该协议的对象要实现这两个方法。  

上下文管理器（Context Manager）：支持上下文管理协议的对象，这种对象实现了\__enter__() 和 \__exit__() 方法。上下文管理器定义执行 with 语句时要建立的运行时上下文，负责执行 with 语句块上下文中的进入与退出操作。通常使用 with 语句调用上下文管理器，也可以通过直接调用其方法来使用。  

运行时上下文（runtime context）：由上下文管理器创建，通过上下文管理器的 \__enter__() 和\__exit__() 方法实现，\__enter__() 方法在语句体执行之前进入运行时上下文，\__exit__() 在语句体执行完后从运行时上下文退出。with 语句支持运行时上下文这一概念。  

上下文表达式（Context Expression）：with 语句中跟在关键字 with 之后的表达式，该表达式要返回一个上下文管理器对象。  

语句体（with-body）：with 语句包裹起来的代码块，在执行语句体之前会调用上下文管理器的 \__enter__() 方法，执行完语句体之后会执行\__exit__() 方法。  



## 相关链接：
1.http://blog.kissdata.com/2014/05/23/python-with.html  
2.https://www.ibm.com/developerworks/cn/opensource/os-cn-pythonwith/  