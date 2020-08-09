## 1.scala中如何定义类
scala中定义类的方式很简单  

```
class Point(xc:Int,yc:Int)
```  

上面这行代码就定义了一个类  
1.首先是关键字class  
2.其后是类名 Point  
3.类名之后的括号中是构造函数的参数列表，这个例子中是类的两个变量xc，yc，且均为Int类型的数据。  

## 2.类的构造方法
类的定义中可以有多个构造参数。与java中不同的是，scala类名称后直接加上构造函数的参数列表，这个构造函数就是主构造函数。另外，Scala中有只有一个主要构造函数，其他都是辅助构造函数。而且需要注意的是，辅助构造函数必须调用主构造函数或者通过this(...)之间相互调用。  

另外与java中不同的一点是，在scala中重写方法，必须加上override关键字，否则编译器会报错！  

```
class Point(xc:Int,yc:Int) {

  var x:Int = xc
  var y:Int = yc

  val isOriginal:Boolean = {
    x == 0 && y == 0
  }

  def this(xc:Int) {
    this(xc,0)
    println("hello,I'm another constructor!")
  }

  def move(dx:Int,dy:Int): Unit = {
    x += dx
    y += dy
  }

  override def toString(): String = "(" + x + ", " + y + ")"
}
```  

再写个客户端代码调用这个类：  

```
object TestPoint {

  def t1(): Unit = {
    val p1 = new Point(10,15)
    println(p1)
    val p2 = new Point(1)
    println(p2)
  }

  def main(args: Array[String]): Unit = {
    t1()
  }
}
```  

将客户端代码run起来  

```
(10, 15)
hello,I'm another constructor!
(1, 0)
```  

## 3.继承
scala继承基类很简单，跟java一样会用extends关键字即可。  

```
class MyPoint(xc:Int,yc:Int) extends Point(xc,yc) {

  def sayMyPoint(): Unit = {
    println("location: " + xc + "," + yc)
  }

  override def move(dx: Int, dy: Int): Unit = {
    x += 2*dx
    y += 2*dy
    println("now x is: " + x + ",y is: " + y)
  }
}
```  

调用继承类：  

```
object TestPoint {

  def t2(): Unit = {
    val p1 = new MyPoint(10,15)
    p1.sayMyPoint()
    p1.move(5,5)
  }

  def main(args: Array[String]): Unit = {
    t2()
  }
}
```  

将代码run起来：  

```
location: 10,15
now x is: 20,y is: 25
```
