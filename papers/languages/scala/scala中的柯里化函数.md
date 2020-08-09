## 1.什么是柯里化函数
在scala相关的教程与参考文档里，经常会看到柯里化函数这个词。但是对于具体什么是柯里化函数，柯里化函数又有什么作用，其实可能很多同学都会有些疑惑。今天就跟大家来掰扯掰扯柯里化函数(Haskell Curry)。  

首先看两个简单的函数：  

```
    def add(x: Int, y: Int) = x + y

    def addCurry(x: Int)(y: Int) = x + y
```  

以上两个函数实现的都是两个整数相加的功能。对于add方法，调用方式为`add(1,2)`。对于addCurry方法，调用的方式为`addCurry(1)(2)`。这种方式就叫做柯里化。说得更加简单粗暴一点，有多个参数列表，或者说多个小括号括起来的函数参数列表的函数就是柯里化函数。  

## 2.为什么要使用柯里化
看了前面的例子，很多人估计忍不住就要开喷了：你特么逗我呢？好好的给一个方法传两个参数不挺好么，干嘛搞这么复杂。  
我能理解大家的感受，我第一次看到这种做法心里也是有一万匹草泥马奔腾而过。不过我们要相信一句话，存在即合理，既然这么干，肯定是有合理的地方，暂且慢慢分析。  

curry化最大的意义在于把多个参数的函数等价转化成多个单参数函数的级联，这样所有的函数就都统一了，方便做lambda演算。 在scala里，curry化对类型推演也有帮助，scala的类型推演是局部的，在同一个参数列表中后面的参数不能借助前面的参数类型进行推演，curry化以后，放在两个参数列表里，后面一个参数列表里的参数可以借助前面一个参数列表里的参数类型进行推演。  

上面的说法比较书面化，用更加口语化的一点来描述：  
1.把多个参数转化为单参数函数的级联，达到了动态确定参数的目的。  
2.当某些参数不确定时，可以先保留一个存根。剩余的参数确定以后，就可以通过存根调用剩下的参数。  
3.通过类似于建造者模式(building)，把一个大的东西的构造过程，切成一个个的小模块来逐步构造。举个最简单的例子，`Person.name("xxx").age(num).salary(count).phone(xxxx)`。  

## 3.scala源码中的柯里化
scala源码中存在大量的柯里化函数的应用，看几个简单的例子。  

```
  def foldLeft[B](z: B)(f: (B, A) => B): B = {
    var acc = z
    var these = this
    while (!these.isEmpty) {
      acc = f(acc, these.head)
      these = these.tail
    }
    acc
  }
```  

从foldLeft的方法原型里很容易就看出来，这是就是典型的柯里化函数的应用。foldLeft有两个参数，一个为参入的初始值z，类型为B。另一个为函数f，f有两个参数，一个类型与传入的初始值相同，另一个为集合本身的类型A，最后方法返回的类型为B。  

```
    def foldtest() = {
        val list = List(1, 2, 3)
        val strResleft = list.foldLeft("res:")((x: String, y:Int) => x + y)
        val strResRight = list.foldRight("res:")((y: Int, x: String) => x + y)
        println(strResleft)
        println(strResRight)
    }
```  

函数的输出：  

```
res:123
res:321
```  