## 1.java里的Null Pointer Exception
写过一阵子的Java后, 应该会对NullPointerException (NPE)这种东西很熟悉，基本上会碰到这种异常，就是你有一个变量是 null，但你却调用了它的方法，或是取某个的值。  

举例而言，下面的 Java 代码就会抛出NPE异常：  

```
例1:
String s1 = null;
System.out.println("length:" + s1.length());
```  

当然，一般来说，我们很少会写出这么明显的错误代码。  

但另一方，在 Java 的使用习惯说，我们常常以「返回 null」这件事,来代表一个函数的返回值是不是有意义。  

```
例2：
//就是在 Java 里 HashMap 的 get() 方法，如果找不到对应的 key 值，就会反回 null：
HashMap<String, String> myMap = new HashMap<String, String>();
myMap.put("key1", "value1");
String value1 = myMap.get("key1");  // 返回 "value1"
String value2 = myMap.get("key2");  // 返回 null

System.out.println(value1.length()); // 没问题，答案是 6
System.out.println(value2.length()); // 抛 NullPointerException
```  

在上面的例子中，myMap 里没没有对应的key值，那么get()会传回null。  
如果你像上面一样没有做检查，那很可能就会抛出 NullPointerException，所以我们要像下面一样，先判断得到的是不是 null 才可以调用算字符串长度的方法。  

```
例3:
HashMap<String, String> myMap = new HashMap<String, String>();

myMap.put("key1", "value1");

String value1 = myMap.get("key1");  // 返回 "value1"
String value2 = myMap.get("key2");  // 返回 null

if (value1 != null) {
    System.out.println(value1.length()); // 没问题，答案是 6
}

if (value2 != null) {
    System.out.println(value2.length()); // 没问题，如果 value2 是 null，不会被执行到
}
```  

那我们要怎么知道一个 Java 里某个函数会不会返回null 呢?  

答案是你只能依靠 JavaDoc 上的说明、去查看那个函式的源码来看，再不然就是靠黑盒测试（如果你手上根本没有源码），又或者直接等他哪天爆掉再来处理。  

## 2.Scala 里的 Option[T] 的概念
相较之下，如果你去翻 Scala 的 Map 这个类别，会发现他的回传值类型是个 Option[T]，但这个有什么意义呢？  

我们还是直接来看代码吧:  

```
例4：
// 虽然 Scala 可以不定义变量的类型，不过为了清楚些，我还是
// 把他显示的定义上了

val myMap: Map[String, String] = Map("key1" -> "value")
val value1: Option[String] = myMap.get("key1")
val value2: Option[String] = myMap.get("key2")

println(value1) // Some("value1")
println(value2) // None
```  

在上面的代码中，myMap 一个是一个 Key 的类型是 String，Value 的类型是 String 的 hash map，但不一样的是他的 get() 返回的是一个叫 Option[String] 的类别。  

但在各个Option 类别代表了什么意思呢？答案是他在告诉你：我很可能没办法回传一个有意义的东西给你喔！  

像上面的例子里，由于 myMap 里并没有 key2 这笔数据，get() 自然要想办法告诉你他找不到这笔数据，在 Java 里他只告诉你他会回传一个 String，而在 Scala 里他则是用 Option[String] 来告诉你：「我会想办法回传一个 String，但也可能没有 String 给你」。  

至于这是怎么做到的呢？很简单，Option 有两个子类别，一个是 Some，一个是 None，当他回传 Some 的时候，代表这个函式成功地给了你一个 String，而你可以透过 get() 这个函式拿到那个 String，如果他返回的是 None，则代表没有字符串可以给你。  

当然，在返回 None，也就是没有 String 给你的时候，如果你还硬要调用 get() 来取得 String 的话，Scala 一样是会报告一个 Exception 给你的。  

至于怎么判断是 Some 还是 None 呢？我们可以用 isDefined 这个函式来判别，所以如果要和 Java 版的一样，打印 value 的字符串长度的话，可以这样写：  

```
例5：
// 虽然 Scala 可以不定义变量的类型，不过为了清楚些，我还是
// 把他显示的定义上了

val myMap: Map[String, String] = Map("key1" -> "value")
val value1: Option[String] = myMap.get("key1")
val value2: Option[String] = myMap.get("key2")

if (value1.isDefined) {
    println("length:" + value1.get.length)
}

if (value2.isDefined) {
    println("length:" + value2.get.length)
}

```  

还是改用 Pattern Matching 好了  
我知道你要翻桌了，这和我们直接来判断反回值是不是 null 还不是一样？！如果没检查到一样会出问题啊，而且这还要多做一个 get 的动作，反而更麻烦咧！  

不过就像我之前说过的，Scala 比较像是工具箱，他给你各式的工具，让你自己选择适合的来用。  

所以既然上面那个工具和原本的 Java 版本比起来没有太大的优势，那我们就换下一个 Scala 提供给我们的工具吧！  

Scala 提供了 Pattern Matching，也就是类似 Java 的 switch-case 加强版，所以我们上面的程序也可以改写成像下面这样：  

```
例6:
// 虽然 Scala 可以不定义变量的类型，不过为了清楚些，我还是
// 把他显示的定义上了
val myMap: Map[String, String] = Map("key1" -> "value")
val value1: Option[String] = myMap.get("key1")
val value2: Option[String] = myMap.get("key2")

value1 match {
    case Some(content) => println("length:" + content.length)
    case None => // 啥都不做
}

value2 match {
    case Some(content) => println("length:" + content.length)
    case None => // 啥都不做
}
```  

上面是另一个使用 Option 的方式，你用 Pattern Matching 来检查 value1 和 value2 是不是 Some，如果是的话就把 Some 里面的值抽成一个叫 content 的变量，然后再来看你要做啥。  

在大多数的情况下，比起上面的方法，我会更喜欢这个做法，因为我觉得 Pattern Matching 在视觉上比 if 来得更容易理解整个程序的流程。  

但话说回来，其实这还是在测试返回值是不是 None，所以充其量只能算是 if / else 的整齐版而已  

## 3.Option[T] 是个容器，所以可以用 for 循环
之前有稍微提到，在 Scala 里 Option[T] 实际上是一个容器，就像数组或是 List 一样，你可以把他看成是一个可能有零到一个元素的 List。  

当你的 Option 里面有东西的时候，这个 List 的长度是一（也就是 Some），而当你的 Option 里没有东西的时候，他的长度是零（也就是 None）。  

这就造成了一个很有趣的现象－－如果我们把他当成一般的 List 来用，并且用一个 for 循环来走访这个 Option 的时候，如果 Option 是 None，那这个 for 循环里的程序代码自然不会执行，  
于是我们就达到了「不用检查 Option 是否为 None」这件事。  

于是下面的程序代码可以就达成和我们上面用 if 以及 Pattern Matching 的程序代码相同的效果：  

```
例7:
// 虽然 Scala 可以不定义变量的类型，不过为了清楚些，我还是
// 把他显示的定义上了

val myMap: Map[String, String] = Map("key1" -> "value")
val value1: Option[String] = myMap.get("key1")
val value2: Option[String] = myMap.get("key2")

for (content <- value1) {
    println("length:" + content.length)
}

for (content <- value2) {
    println("length:" + content.length)
}
```  

我们可以换个想法解决问题  

话说上面的几个程序，我们都是从「怎么做」的角度来看，一步步的告诉计算机，如果当下的情况符合某些条件，就去做某些事情。  

但之前也说过，Scala 提供了不同的工具来达成相同的功能，这次我们就来换个角度来解决问题－－我们不再问「怎么做」，而是问「我们要什么」。  

我们要的结果很简单，就是在取出的 value 有东西的时候，印出「length: XX」这样的字样，而 XX 这个数字是从容器中的字符串算出来的。  

在 Functional Programming 中有一个核心的概念之一是「转换」，所以大部份支持 Functional Programming 的程序语言，都支持一种叫 map()  
的动作，这个动作是可以帮你把某个容器的内容，套上一些动作之后，变成另一个新的容器。  

举例而言，在 Scala 里面，如果有们有一个 List[String]，我们希望把这个 List 里的字符串，全都加上" World" 这个字符串的话，可以像下面这样做：  

```
例8:
scala> val xs = List("Hello", "Goodbye", "Oh My")
xs: List[String] = List(Hello, Goodbye, Oh My)
scala> xs.map(_ + " World!")
res0: List[String] = List(Hello World!, Goodbye World!, Oh My World!)
```  

你可以看到，我们可以用 map() 来替 List 内的每个元素做转换，产生新的东西。  

所以我们现在可以开始思考，在我们要达成的 length: XX 中，是怎么转换的：  

先算出 Option 容器内字符串的长度  
然后在长度前面加上 "length:" 字样  
最后把容器走访一次，印出容器内的东西  
有了上面的想法，我们就可以写出像下面的程序：  

```
例9:
// 虽然 Scala 可以不定义变量的类型，不过为了清楚些，我还是
// 把他显示的定义上了

val myMap: Map[String, String] = Map("key1" -> "value")
val value1: Option[String] = myMap.get("key1")
val value2: Option[String] = myMap.get("key2")

// map 两次，一次算字数，一次加上讯息
value1.map(_.length).map("length:" + _).foreach(println _)

// 把算字数和加讯息全部放在一起
value2.map("length:" + _.length).foreach(pritlnt _)
```  

透过这样「转换」的方法，我们一样可以达成想要的效果，而且同样不用去做「是否为 None」的判断。  

再稍微强大一点的 for 循环组合  
上面的都是只有单一一个 Option[T] 操作的场合，不过有的时候你会需要「当两个值都是有意义的时候才去做某些事情」的状况，这个时候 Scala 的 for 循环配上 Option[T] 就非常好用。  

同样直接看程序代码：  

```
例10:
val option1: Option[String] = Some("AA")
val option2: Option[String] = Some("BB");

for (value1 <- option1; value2 <- option2) {
    println("Value1:" + value1)
    println("Value2:" + value2)
}

```  

在上面的程序代码中，只有当 option1 和 option2 都有值的时候，才会印出来。如果其中有任何一个是 None，那 for 循环里的程序代码就不会被执行。  

当然，这样的使用结构不只限于两个 Option 的时候，如果你有更多个 Option 变量，也只要把他们放到 for 循环里去，就可以让 for 循环只有在所有 Option 都有值的时候才能执行。  

但我其实想要默认值耶……  
有的时候，我们会希望当函数没办法返回正确的结果时，可以有个默认值来做事，而不是什么都不错。  

就算是这样也没问题！  

因为 Option[T] 除了 get() 之外，也提供了另一个叫 getOrElse() 的函式，这个函式正如其名－－如果 Option 里有东西就拿出来，不然就给个默认值。  

举例来讲，如果我用 Option[Int] 存两个可有可无的整数，当 Option[Int] 里没东西的时候，我要当做 0 的话，那我可以这样写：  

```
例11:
val option1: Option[Int] = Some(123)
val option2: Option[Int] = None

val value1 = option1.getOrElse(0) // 这个 value1 = 123
val value2 = option2.getOrElse(0) // 这个 value2 = 0
```  

所以 Option[T] 万无一失吗？  
当然不是！由于 Scala 要和 Java 兼容，所以还是让 null 这个东西继续存在，所以你一样可以产生 NullPointerException，而且如果你不注意，对一个空的 Option 做 get，Scala 一样会爆给你看。  

```
例12:
val option1: Option[Int] = null
val option2: Option[Int] = None

option1.foreach(println _) // 爆掉，因为你的 option1 本来就是 null 啊
option2.get()              // 爆掉，对一个 None 做 get 是一定会炸的
```  

我自己是觉得 Option[T] 比较像是一种保险装置，而且这个保险需要一些时间来学习，也需要在有正确使用方式（例如在大部份的情况下，你都不应该用 Option.get() 这个东西），才会显出他的好处来。  

只是当习惯了之后，就会发现 Option[T] 真的可以替你避掉很多错误，至少当你一看到某个 Scala API 的回传值的型态是 Option[T] 的时候，你会很清楚的知道自己要小心。  

原文链接： https://my.oschina.net/u/200745/blog/69845  