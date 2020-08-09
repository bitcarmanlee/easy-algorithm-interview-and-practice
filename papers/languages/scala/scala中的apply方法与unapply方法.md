## 1.apply方法
当scala中类或者对象有一个主要用途的时候，apply方法就是一个很好地语法糖。  

请看下面一个简单的例子：  

```
class Foo(foo: String) {
}

object Foo {
	def apply(foo: String) : Foo = {
		new Foo(foo)
	}
}
```  

定义了一个Foo类，并且在这个类中，有一个伴生对象Foo，里面定义了apply方法。有了这个apply方法以后，我们在调用这个Foo类的时候，用函数的方式来调用：  

```
object Client {
	
	def main(args: Array[String]): Unit = {
		val foo = Foo("Hello")
	}
}
```  

我们用`Foo("Hello")`的方式，就得到了一个Foo类型的对象，这一切就是apply方法的功劳。如果没有apply方法，我们将需要使用new关键字来得到Foo对象。  

## 2.apply方法用来做工厂
apply方法的最佳实践方式之一就是用来做工厂。比如在Scala的标准库中，许多集合类给我们提供了apply方法来创建集合：  

```
object Client {
	
	def main(args: Array[String]): Unit = {
		val arr = new Array[Int](3)
		arr(0) = 0
		arr(1) = 1
		arr(2) = 2
		arr.foreach(x => print(x + " "))
		println()
		
		val array = Array(1,2,3)
		array.foreach(x => print(x + " "))
	}
}
```  

上面两种方式我们都可以用来创建Array。第一种方式是使用new关键字，这是传统的面向对象的方式。那么第二种方式是什么情况呢？如果我们在IDE里点进去，可以发现IDE会提示我们有一个apply方法。点进去看apply方法的源码：  

```
  /** Creates an array of `Int` objects */
  // Subject to a compiler optimization in Cleanup, see above.
  def apply(x: Int, xs: Int*): Array[Int] = {
    val array = new Array[Int](xs.length + 1)
    array(0) = x
    var i = 1
    for (x <- xs.iterator) { array(i) = x; i += 1 }
    array
  }
```  

## 3.unapply方法
从上面的例子不难看出，apply方法有点类似于java中的构造函数，接受构造参数变成一个对象。那么unapply方法就刚好相反，他是接受一个对象，从对象中提取出相应的值。  

unapply方法主要用于模式匹配中。  
看个简单的例子：  

```
class Money(val value: Double, val country: String) {}

object Money {
    def apply(value: Double, country: String) : Money = new Money(value, country)

    def unapply(money: Money): Option[(Double, String)] = {
        if(money == null) {
            None
        } else {
            Some(money.value, money.country)
        }
    }
}
```  

客户端实现：  

```
    def testUnapply() = {
        val money = Money(10.1, "RMB")
        money match {
            case Money(num, "RMB") =>  println("RMB: " + num)
            case _ => println("Not RMB!")
        }
    }
```  

最后输出为：  

```
RMB: 10.1
```  


所以下面那种创建数组的方式，其实是通过Array类的apply方法实现的。  

## 参考文档：
1.https://stackoverflow.com/questions/9737352/what-is-the-apply-function-in-scala/9738862#9738862  
2.https://twitter.github.io/scala_school/zh_cn/basics2.html  