scala的各种源码里，有大量的implicit关键字。老见到他晃来晃去又不知道为什么，本博主憋得慌，于是有了这篇小文章。

## 1.最常见的隐式转换函数
我们定义了一个方法test，接受的参数类型是String。当我们输出的参数为"101"的时候，显然是OK的。但是当输入的参数为101这个int时，显然就会有问题：  

```
scala> def printMsg(msg:String) = println(msg)
printMsg: (msg: String)Unit

scala> printMsg("101")
101

scala> printMsg(101)
<console>:13: error: type mismatch;
 found   : Int(101)
 required: String
       printMsg(101)
                ^
```  

我们给来个隐式转换函数，将int转成string：  

```
scala> implicit def turnIntToString(num:Int) = num.toString
warning: there was one feature warning; re-run with -feature for details
turnIntToString: (num: Int)String

scala> printMsg(101)
101
```  

隐式函数是在一个scop下面，给定一种输入参数类型，自动转换为返回值类型的函数，和函数名，参数名无关。  

## 2.再来个常见的例子
讲到隐式转换，大部门的资料里都会提到这个例子：在Predef中使用了方法调用的隐式转换  

```
Map(1 -> 11, 2 -> 22)
```  

上面这段Map中的参数是个二元元组。注意Int是没有 -> 方法。 但是在Predef中定义了：  

```
  final class ArrowAssoc[A](val __leftOfArrow: A) extends AnyVal {
    // `__leftOfArrow` must be a public val to allow inlining. The val
    // used to be called `x`, but now goes by `__leftOfArrow`, as that
    // reduces the chances of a user's writing `foo.__leftOfArrow` and
    // being confused why they get an ambiguous implicit conversion
    // error. (`foo.x` used to produce this error since both
    // any2Ensuring and any2ArrowAssoc pimped an `x` onto everything)
    @deprecated("Use `__leftOfArrow` instead", "2.10.0")
    def x = __leftOfArrow

    @inline def -> [B](y: B): Tuple2[A, B] = Tuple2(__leftOfArrow, y)
    def →[B](y: B): Tuple2[A, B] = ->(y)
  }
  @inline implicit def any2ArrowAssoc[A](x: A): ArrowAssoc[A] = new ArrowAssoc(x)
```  

1->11其实就是1.->(11)的偷懒写法。  
这里怎么能让整数类型1能有->方法呢？其实就是any2ArrowAssoc起的作用了，将整型的1 implicit转换为 ArrowAssoc(1)，然后再调用->方法。  


## 3.方法调用的隐式转换
先上代码  

```
object Test {

  case class Person (name:String,age:Int) {
    def +(num:Int) = age + num
    def +(p:Person) = age + p.age
  }

  def main(args: Array[String]): Unit = {
    val person = Person("Micheal",18)
    println(person + 1) //result is 19
    //println(1 + person) 会报错,因为int的+方法没有重载Person参数

    implicit def intAddPerson(num:Int) = Person("default",num)
    println(1 + person) //result is 19
  }

}
```  

有了隐式转换方法之后，编译器检查 1 + person 表达式，发现Int的+方法没有有Person参数的重载方法。在放弃之前查看是否有将Int类型的对象转换成以Person为参数的+方法的隐式转换函数，于是找到了，然后就进行了隐式转换。  


## 4.隐式参数
函数或者方法可以带有一个标记为implicit的参数列表。在这种情况下，编译器会查找缺省值，提供给该函数或方法。  

```
object Test {

  case class Delimiters(left:String,right:String)

  def transferStr(input:String)(implicit delims:Delimiters) =
    delims.left + input + delims.right

  implicit val delimiters = Delimiters("(",")")

  def main(args: Array[String]): Unit = {
    val res = transferStr("hello world")
    println(res)
  }
  
}
```  

输出结果为：  

```
(hello world)
```  

## 5.利用隐式参数进行隐式转换

我们提供一个泛型函数来得到相对小的值：  

```
def smaller[T](a: T, b: T) = if (a < b) a else b
```  

这里由于我们并不知道a和b的类型是否有<操作符，所以编译器不会通过。  
解决办法是添加一个隐式参数order来指代一个转换函数  

```
def smaller[T](a:T,b:T)(implicit order:T => Ordered[T])
  = if(order(a) < b) a else b
```  

由于Ordered[T]特质中有一个接受T作为参数的<方法，所以编译器将在编译时知道T，并且从而判决是否T => Ordered[T]类型的隐式定义存在于作用域中。  

这样，才可以调用smaller(40, 2)或者smaller("AA", "BB")。  

注意，order是一个带有单个参数的函数，被打上了implicit标签，所以它不仅是一个隐式参数，也是一个隐式转换。那么，我们可以在函数体重省略order的显示调用。  


```
def smaller[T](a: T, b: T)(implicit order: T => Ordered[T])
  = if (a < b) a else b
```  

因为a没有带<的方法，那么会调用order(a)进行转换。  

## 6.隐式类
1.隐式类必须有一个带一个参数的主构造函数  
2.必须定义在另一个class/object/trait里面（不能独立定义）  
3.隐式类构造器只能带一个不是implicit修饰的参数  
4.作用域中不能有与隐式类类型相同的成员变量，函数以及object名称  

```
class B {
  def add(x:Int,y:Int) = {
    x + y
  }
}

object ImpClass {
  implicit class mulB(arg:B) {
    def multiply(x:Int,y:Int) =
      x * y
  }
}

object client {
  def main(args: Array[String]): Unit = {
    import ImpClass._
    val b = new B()
    val res = b.multiply(2,3)
    println("res is: " + res)
  }
}
```  

结果：  

```
res is: 6

```  

## 参考资料：
1.http://blog.csdn.net/oopsoom/article/details/24643869  
2.http://fangjian0423.github.io/2015/12/20/scala-implicit/  
3.http://blog.jasonding.top/2016/02/21/Scala/【Scala类型系统】隐式转换与隐式参数/  
4.http://bit1129.iteye.com/blog/2186533  
5.scala Predef部分源码  