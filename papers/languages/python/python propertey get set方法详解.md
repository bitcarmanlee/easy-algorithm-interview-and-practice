## 1.java里get/set方法
大部分的同学开始写java代码的时候，最初始的代码肯定是字段的get/set方法。大家对于java特别冗长的诟病，很大一部分来自于无处不在的get/set方法。甚至国内有相当一部分不负责任的java书籍，里面靠大段的get/set代码来拼凑篇幅。。。  

来个最简单的例子，估计大家都写过类似的代码：  

```
public class Person {

    private int age;

    public Person(int age) {
        this.age = age;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```  

## 2.python里的get/set方法
python里如果按java的那一套写法，代码应该像是这样：  

```
class Person(object):

    def __init__(self):
        self._age = None

    def get_age(self):
        return self._age

    def set_age(self,age):
        if(isinstance(age,str)):
            self._age = int(age)
        elif(isinstance(age,int)):
            self._age = age
```  

显然这是java风格的代码，python的哲学是简洁明了，这么麻烦的代码显然不是我们想要的。如果我们想直接访问上面Person类的age属性，也得使用get/set方法，否则会报错：  


```
p = Person()
p.set_age("18")
print p.get_age() #OK，没问题
print p.age #会报错，'Person' object has no attribute 'age'
```  

## 3.property方法
如果我们想在py中直接访问属性，比如想在上面的例子中直接访问Person的age字段，可以在Person类的最后加如下一行代码：  

```
age = property(get_age,set_age)
```  

这样，我们就直接可以访问age字段了：  

```
p = Person()
p.age = 18
print p.get_age() #OK，没问题，返回的结果是18
print p.age #OK，没问题，返回的结构也是18
```  

上面是用函数模式的方式来使用property的。当然我们也可以用装饰器的模式使用。  

```
class Person(object):

    def __init__(self):
        self._age = None

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self,age):
        if isinstance(age,str):
            self._age = int(age)
        elif isinstance(age,int):
            self._age = age

    @age.deleter
    def age(self):
        del self._age

p = Person()
p.age = "18"
print p.age #18
del p.age
print p.age #报错,AttributeError: 'Person' object has no attribute '_age'
```  

上面使用property装饰器模式的时候注意几个小点：  
1.三个函数的名字与字段名是一样的。  
2.使用proterty可以比较简单实现字段的读写控制。例如想要字段为只读属性，那么只需要提供getter方法，上面的setter方法可以去掉。  

## 4.用property定义需要计算的属性
同时我们还可以用property来定义需要进行计算的字段。这些字段不会保存在对象中，只有当我们实际需要的时候才会完成真正计算。  

```
class Person(object):

    def __init__(self):
        self._age = None

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self,age):
        if isinstance(age,str):
            self._age = int(age)
        elif isinstance(age,int):
            self._age = age

    @property
    def height(self):
        return self.age * 10

p = Person()
p.age = ("18")
print p.height #180
```  

上面的例子，就是根据年龄来推算身高。。  

## 5.property的基本原理
在python中，property()是一个内置的函数。他的原型如下：  

```
   def __init__(self, fget=None, fset=None, fdel=None, doc=None): # known special case of property.__init__
        """
        property(fget=None, fset=None, fdel=None, doc=None) -> property attribute
        
        fget is a function to be used for getting an attribute value, and likewise
        fset is a function for setting, and fdel a function for del'ing, an
        attribute.  Typical use is to define a managed attribute x:
        
        class C(object):
            def getx(self): return self._x
            def setx(self, value): self._x = value
            def delx(self): del self._x
            x = property(getx, setx, delx, "I'm the 'x' property.")
        
        Decorators make defining new properties or modifying existing ones easy:
        
        class C(object):
            @property
            def x(self):
                "I am the 'x' property."
                return self._x
            @x.setter
            def x(self, value):
                self._x = value
            @x.deleter
            def x(self):
                del self._x
        
        # (copied from class doc)
        """
        pass
```  

在python的源码中，我们就很容易看出property的用法。其中，fget是一个获取字段值的函数，而fget是一个设置字段值的函数，fdel是一个删除属性的函数，doc是一个字符串（类似于注释）。从函数实现上看，这些函数参数都是可选的，默认为None，调用的其实就是__get__,__set__,__del__方法!  

```
age = property(get_age,set_age)
```  

这句代码，其实可以被分解为  

```
age = property()
age = age.getter(get_age)
age = age.setter(set_age)
```  

不去定义名字get_age和set_age，因为他们不是必须的，并且污染类的命名空间。而通过property的实现方式，都很简单。在python各种类库的源码中，经常会遇到很多类似的代码结构。  