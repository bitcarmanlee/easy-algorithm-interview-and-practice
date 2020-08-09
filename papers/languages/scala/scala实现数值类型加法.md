在前面的文章里，我们讲了在java中如何利用泛型实现数值类型加法。具体可以参考博文 http://blog.csdn.net/bitcarmanlee/article/details/78733637。  
那么在scala中，我们怎么实现上面的需求呢？  

## 1.用 <: 模拟extends关键字行不通
如果按照在java中的处理思路，我们可以这么尝试一下：  

```
    def numberAdd[T <: Number](t1 : T, t2 : T) = {
        t1.doubleValue() + t2.doubleValue()
    }

    @Test
    def numberaddtest() = {
        val (t1, t2) = (1, 2)
        numberAdd(t1, t2)
    }
```  

在scala中，`<:`表示类型的上限，与java中的extends含义一样。我们试图将上面的test方法run起来，发现IDE中报错：  

```
Error:(26, 19) type mismatch;
 found   : Int
 required: T
        numberAdd(t1, t2)
Error:(26, 9) inferred type arguments [Int] do not conform to method numberAdd's type parameter bounds [T <: Number]
        numberAdd(t1, t2)
Error:(26, 23) type mismatch;
 found   : Int
 required: T
        numberAdd(t1, t2)
```  

很明显，上面的方法是行不通的。  

## 2.使用Numeric[T]
为什么上面的方法行不通呢？因为Scala的数字类型并不都共享一个超类，所以我们不能使用T <: Number。相反，要使之能工作，Scala的math库对适当的类型T 定义了一个隐含的Numeric[T]，我们可以使用他来完成类似的功能。  

首先上可以运行的代码：  

```
    def add[T](x: T, y: T)(implicit num: Numeric[T]) = {
        val result = num.plus(x, y)
        result
    }
    @Test
    def testAdd() = {
        val int1 = 1
        val int2 = 2
        println("int sum is: " + add(int1, int2))

        val long1 = 100L
        val long2 = 200L
        println("long sum is: " + add(long1, long2))

        val f1 = 1.0f
        val f2 = 2.0f
        println("float sum is: " + add(f1, f2))

        val d1 = 1.0
        val d2 = 2.0
        println("double sum is: " + add(d1, d2))
    }
```  

将上面的test方法run起来，可以得到如下输出：  

```
int sum is: 3
long sum is: 300
float sum is: 3.0
double sum is: 3.0
```  

## 3.Numeric[T]的用法

Numeric[T]在scala中源码如下：  

```
  type Numeric[T] = scala.math.Numeric[T]
  val Numeric = scala.math.Numeric
```  

当然，我们也可以通过implicitly方法，用context bound(上下文绑定)的方式让上面的代码更简单：  

```
    def add2[T: Numeric](x: T, y: T) = {
        implicitly[Numeric[T]].plus(x, y)
    }
```  

其中，implicitly方法在scala中的定义如下：  

```
@inline def implicitly[T](implicit e: T) = e    // for summoning implicit values from the nether world 
```  

implicitly 主要是在当前作用域查找指定类型，例如以下的例子：  

```
    @Test
    def testimplicit() = {
        implicit val x = 1
        implicit val x1 = 2.0
        val y = implicitly[Int]
        val z = implicitly[Double]
        println(y + "\t" + z)
    }
```  

将test方法run起来以后，输出如下：  

```
1	2.0
```  

## 4.数值集合求和
搞定了单个的数值求和，那么数值集合的求和自然就变得容易了：  

```
    def add4[T: Numeric](x : Array[T]) = {
        var sum = 0.0
        for(each <- x) {
            sum += implicitly[Numeric[T]].toDouble(each)
        }
        println(sum)
    }

    @Test
    def test() = {
        val array = Array(1, 2, 3)
        add4(array)
    }
```  

代码输出：  

```
6.0
```  

## 参考内容：
1.https://stackoverflow.com/questions/4373070/how-do-i-get-an-instance-of-the-type-class-associated-with-a-context-bound  
2.https://stackoverflow.com/questions/2982276/what-is-a-context-bound-in-scala  
3.http://www.jianshu.com/p/1d119c937015 Scala中的Implicit详解  
4.https://vimsky.com/article/1562.html scala常见问题整理  
5.https://fangjian0423.github.io/2015/06/07/scala-generic/ scala泛型  