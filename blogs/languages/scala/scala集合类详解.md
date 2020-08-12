对scala中的集合类虽然有使用，但是一直处于一知半解的状态。尤其是与java中各种集合类的混合使用，虽然用过很多次，但是一直也没有做比较深入的了解与分析。正好趁着最近项目的需要，加上稍微有点时间，特意多花了一点时间对scala中的集合类做个详细的总结。  

## 1.数组Array
在说集合类之前，先看看scala中的数组。与Java中不同的是，Scala中没有数组这一种类型。在Scala中，Array类的功能就与数组类似。  
与所有数组一样，Array的长度不可变，里面的数据可以按索引位置访问。  

```
  def test() = {
    val array1 = new Array[Int](5)
    array1(1) = 1
    println(array1(1))
    val array2 = Array(0, 1, 2, 3, 4)
    println(array2(3))
  }
```  

上面的demo就演示了Array的简单用法。  

## 2.集合类的大致结构
网上的一张图，scala中集合类的大体框架如下图所示。    
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/scala/1.jpeg)      

特意查了下scala的源码，贴上几张图，可以对应到上面的这幅继承关系图。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/scala/2.png)    

根据图以及源码可以很清晰地看出scala中的集合类可以分为三大类：  
1.Seq，是一组有序的元素。  
2.Set，是一组没有重复元素的集合。  
3.Map，是一组k-v对。  

## 3.Seq分析
Seq主要由两部分组成：IndexedSeq与LinearSeq。现在我们简单看下这两种类型。  

首先看IndexedSeq，很容易看出来这种类型的主要访问方式是通过索引，默认的实现方式为vector。  

```
  def test() = {
    val x = IndexedSeq(1,2,3)
    println(x.getClass)
    println(x(0))

    val y = Range(1, 5)
    println(y)
  }
```  

将以上函数运行起来以后，输出如下：  

```
class scala.collection.immutable.Vector
1
Range(1, 2, 3, 4)
```  

而作为LinearSeq，主要的区别在于其被分为头与尾两部分。其中，头是容器内的第一个元素，尾是除了头元素以外剩余的其他所有元素。LinearSeq默认的实现是List。  

```
  def test() = {
    val x = collection.immutable.LinearSeq("a", "b", "c")
    val head = x.head
    println(s"head is: $head")

    val y = x.tail
    println(s"tail of y is: $y")
  }
```  

将上面的代码运行起来以后，得到的结果如下：  

```
head is: a
tail of y is: List(b, c)
```  

## 4.Set
与其他任何一种编程语言一样，Scala中的Set集合类具有如下特点：  
1.不存在有重复的元素。  
2.集合中的元素是无序的。换句话说，不能以索引的方式访问集合中的元素。  
3.判断某一个元素在集合中比Seq类型的集合要快。  

Scala中的集合分为可变与不可变两种，对于Set类型自然也是如此。先来看看示例代码：  

```
  def test() = {
    val x = immutable.HashSet[String]("a","c","b")
    //x.add("d")无法使用，因为是不可变集合，没有add方法。
    val y = x + "d" + "f"  // 增加新的元素，生成一个新的集合
    val z = y - "a"  // 删除一个元素，生成一个新的集合
    val a = Set(1,2,3)
    val b = Set(1,4,5)
    val c = a ++ b  // 生成一个新的集合，增加集合
    val d = a -- b  // 生成一个新的集合，去除集合
    val e = a & b // 与操作
    val f = a | b // 或操作
  }
```  

因为上面代码里的集合类型都是不可变类型，所以所有语句结果其实都是生成一个新的集合。  

```
  def test() = {
    val x = new mutable.HashSet[String]()
    x += "a"  // 添加一个新的元素。注意此时没有生成一个新的集合
    x.add("d") //因为是可变集合，所以有add方法
    x ++= Set("b", "c")  // 添加一个新的集合
    x.foreach(each => println(each))
    x -= "b"  // 删除一个元素
    println()
    x.foreach(each => println(each))
    println()
    val flag = x.contains("a") // 是否包含元素
    println(flag)
  }
```  

将上面这段代码运行起来以后，得到的结果如下：  

```
c
d
a
b

c
d
a

true
```  

## 5.Map
Map这种数据结构是日常开发中使用非常频繁的一种数据结构。Map作为一个存储键值对的容器（key－value），其中key值必须是唯一的。  默认情况下，我们可以通过Map直接创建一个不可变的Map容器对象，这时候容器中的内容是不能改变的。示例代码如下。  

```
  def test() = {
    val peoples = Map("john" -> 19, "Tracy" -> 18, "Lily" -> 20) //不可变
    // people.put("lucy",15) 会出错，因为是不可变集合。
    //遍历方式1
    for(p <- peoples) {
      print(p + "  ") // (john,19)  (Tracy,18)  (Lily,20)
    }
    //遍历方式2
    peoples.foreach(x => {val (k, v) = x; print(k + ":" + v + "  ")}) //john:19  Tracy:18  Lily:20
    //遍历方式3
    peoples.foreach ({ case(k, v) => print(s"key: $k, value: $v  ")})
    //key: john, value: 19  key: Tracy, value: 18  key: Lily, value: 20
  }
```  
上面代码中的hashMap是不可变类型。  
如果要使用可变类型的map，可以使用mutable包中的map相关类。  

```
  def test() = {
    val map = new mutable.HashMap[String, Int]()
    map.put("john", 19) // 因为是可变集合，所以可以put
    map.put("Tracy", 18)
    map.contains("Lily") //false
    val res = getSome(map.get("john"))
    println(res) //Some(19)
  }

  def getSome(x:Option[Int]) : Any = {
    x match {
      case Some(s) => s
      case None => "None"
    }
  }
```  

## 6.可变数组ArrayBuffer
特意将ArrayBuffer单独拎出来，是因为ArrayBuffer类似于Java中的ArrayList。而ArrayList在Java中是用得非常多的一种集合类。  

ArrayBuffer与ArrayList不一样的地方在于，ArrayBuffer的长度是可变的。与Array一样，元素有先后之分，可以重复，可以随机访问，但是插入的效率不高。  

```
  def test() = {
    val arrayBuffer = new mutable.ArrayBuffer[Int]()
    arrayBuffer.append(1)  //后面添加元素
    arrayBuffer.append(2)
    arrayBuffer += 3  //后面添加元素
    4 +=: arrayBuffer  //前面添加元素
  }
```  

## 7.java与scala集合的相互转换

scala最大的优势之一就是可以使用JDK上面的海量类库。实际项目中，经常需要在java集合类与scala集合类之间做转化。具体的转换对应关系如下：  
scala.collection.Iterable <=> Java.lang.Iterable  
scala.collection.Iterable <=> Java.util.Collection  
scala.collection.Iterator <=> java.util.{ Iterator, Enumeration }  
scala.collection.mutable.Buffer <=> java.util.List  
scala.collection.mutable.Set <=> java.util.Set  
scala.collection.mutable.Map <=> java.util.{ Map, Dictionary }  
scala.collection.mutable.ConcurrentMap <=> java.util.concurrent.ConcurrentMap  

scala.collection.Seq         => java.util.List  
scala.collection.mutable.Seq => java.util.List  
scala.collection.Set         => java.util.Set  
scala.collection.Map         => java.util.Map  
java.util.Properties         => scala.collection.mutable.Map[String, String]  

在使用这些转换的时候，只需要scala文件中引入scala.collection.JavaConversions._  即可。  

一般比较多件的场景是在scala中调用java方法。如前面所讲，jdk的类库太丰富了，在scala中会经常有调用java方法的需求。给个简单的例子：  

假设有如下java代码：  

```
public class TestForScala {

    public static <T> void printCollection(List<T> list) {
        for(T t: list) {
            System.out.println(t);
        }
    }
}

```  

我们想在scala代码中调用TestForScala类中的printCollection方法。可以这么写：  

```
  def test() = {
    val raw = Vector(1, 2, 3)
    TestForScala.printCollection(raw)
  }
```  

java方法中需要的参数是个List，参照我们前面的转换关系，scala.collection.Seq可以自动转化为java中的List，而Vector就是scala中Seq的实现，所以可以直接传入到printCollection方法中！  
