## 1.一切皆对象
python是面向对象语言。在python中，一切皆对象，函数自然也不例外。在python中定义个最简单的函数如下:  

```
def fun():
    print "hello world"
```  

当代码执行遇到def以后，会现在内存中生成一个函数对象，这个函数对象被定义为这个函数的名字。当我们调用函数时就要指定函数的名字，通过函数名才能找到这个函数。 函数的代码段在定义时是不会执行的，只有当这个函数被调用时，函数内部的代码段才会被执行。 函数调用结束时，这个函数内部生成的所有数据都会被销毁。  

函数可以作为对象可以赋值给一个变量，可以作为元素添加到集合对象中，可以作为参数值传递给其它函数，还可以当做函数的返回值被引用。  

## 2.函数拥有对象模型的通用属性
函数作为一个对象，拥有对象模型的通用属性：id,类型和值。以上面的函数为例:  

```
def fun():
    print "hello world"
    
print id(fun)
print type(fun)
print fun
fun()
```  

代码输出如下:    

```
4297786264
<type 'function'>
<function fun at 0x1002b0398>
hello world
```  

使用id加函数名，可以打印func这个函数在内存中的身份地址;  
使用type加函数名可以打印func这个函数的类型;  
只输入函数名，不加括号时，会输出函数在内存中的地址;  
使用def语句来定义函数，func是函数名. 定义func这个函数后，函数里面的打印语句并没有执行，而是等待被调用 ，然后才会执行输出语句。  

## 3.函数可以被引用

```

def fun():
    print "hello world"

f1 = fun
print f1
print fun
f1()
```  

最终的输出：  

```
<function fun at 0x1002b0398>
<function fun at 0x1002b0398>
hello world
```  

由上面的例子不难看出，把函数赋值给一个变量时，就是把这个函数在内存中的地址绑定给这个变量，这样引用这个变量时就是在调用这个函数。将fun赋值给变量f以后，他们指向的是同一个内存地址，使用f1变量名加括号相当于在调用fun()。  

## 4.函数可以当参数传递

```
def fun():
    print "hello world"


def wrapfunc(inner):
    print "hello wrap"
    inner()


wrapfunc(fun)
```  

最后程序的输出：  

```
hello wrap
hello world
```  

## 5.函数作为返回值

```
def fun():
    print "hello world"


def wrapfunc(inner):
    return inner


print wrapfunc(fun)
```  

最后的输出结果为：  

```
<function fun at 0x1002b0398>
```