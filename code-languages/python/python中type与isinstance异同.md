在python中，经常会使用到type与isinstance两个内置的函数来判断变量属于什么类型。那么这两个函数有什么区别呢？下面来简单分析一下。  

## 1.type
type函数的源码如下:  

```
    def __init__(cls, what, bases=None, dict=None): # known special case of type.__init__
        """
        type(object) -> the object's type
        type(name, bases, dict) -> a new type
        # (copied from class doc)
        """
        pass
```  

此部分代码位于__builtin__.py中。从这段代码可以看出，type函数的用法很简单，就是type(object)，返回的是传入的object的类型。  

## 2.isinstance
isinstance函数的源码：  

```
def isinstance(p_object, class_or_type_or_tuple): # real signature unknown; restored from __doc__
    """
    isinstance(object, class-or-type-or-tuple) -> bool
    
    Return whether an object is an instance of a class or of a subclass thereof.
    With a type as second argument, return whether that is the object's type.
    The form using a tuple, isinstance(x, (A, B, ...)), is a shortcut for
    isinstance(x, A) or isinstance(x, B) or ... (etc.).
    """
    return False
```  

isinstance的用法为:  

isinstance(object,type-or-tuple-or-class) -> bool  
传入的第一个参数为对象，第二个参数为类型名(int,str,float等)或者类型名的一个列表(如(str, str, int)为一个列表)，返回值为一个布尔变量。  


## 3.两个函数的异同
相同点  
都可以判断变量是否属于某个内建类型。  

不同点  
1.type只接受一个参数，不仅可以判断变量是否属于某个类型，还可以直接返回参数类型。而isinstance只能判断是否属于某个已知的类型，不能直接得到变量所属的类型。  

2.isinstance可以判断子类实例对象是属于父类的；而type会判断子类实例对象和父类类型不一样。  

```
class A1(object):
    pass


class B1(A1):
    pass


print type(A1()) is A1
print type(B1()) is A1
print isinstance(B1(), B1)
```  

输出结果为:  

```
True
False
True
```  

从以上的分析可以看出，type主要是用来获取未知变量的类型，而instance可以用于继承关系的判断  

## 4.旧式类type
旧式类与新式类的type()结果是不一样的。旧式类type的结果都为<type 'instance'>。  

```
class A1(object):
    pass


class B1(A1):
    pass


class C1:
    pass


print type(B1())
print type(C1())
print type(C1()) is C1
```  

结果如下：  

```
<class '__main__.B1'>
<type 'instance'>
False
```  
