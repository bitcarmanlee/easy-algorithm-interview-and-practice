Scala算是一门博采众家之长的语言，兼具OO与FP的特性，若使用恰当，可以更好地将OO与FP的各自优势发挥到极致；然而问题也随之而来，倘若过分地夸大OO特性，Scala就变成了一门精简版的Java，写出的是没有Scala Style的拙劣代码；倘若过分追求FP的不变性等特性，因为Scala在类型系统以及Monad实现的繁琐性，又可能导致代码变得复杂，不易阅读，反而得不偿失。  

看来，赋予程序员选择的自由，有时候未必是好事！  

在OO世界里，设计模式曾经风靡全世界，你不懂设计模式，都不好意思说自己是程序员。现在呢？说你懂设计模式，倒显得你逼格低了，心里鄙视：“这年头谁还用设计模式，早过时了！”程序员心中的鄙视链开始加成，直接失血二十格。  

其实什么事情都得辩证来看！设计模式对OO设计的推进作用不容忽视，更不容轻视。我只是反对那种为了“模式”而“模式”的僵化思想，如果没有明白设计模式的本质思想，了解根本的设计原理，设计模式无非就是花拳绣腿罢了。当然，在FP世界里，设计模式开始变味开始走形，但诸多模式的本质，例如封装、抽象，仍然贯穿其中，不过是表达形式迥然而已罢了。  

在混合了OO与FP的Scala语言中，我们来观察设计模式的实现，会非常有趣。Pavel Fatin有篇博客 [Design Pattern in Scala](https://pavelfatin.com/design-patterns-in-scala/%20Design%20Patterns%20in%20Scala)将Java设计模式与Scala进行了对比，值得一读。我这里想借用他的案例，然后从另一个角度来俯瞰设计模式。  

在Pavel Fatin比较的设计模式中，部分模式在Scala中不过是一种语法糖（Syntax Sugar），包括：  

Factory Method  
Lazy Initialization  
Singleton  
Adapter  
Value Object  

## 1.Factory Method  
文中给出的Factory Method模式，准确地说其实是静态工厂模式，它并不在GOF 23种模式之列，但作为对复杂创建逻辑的一种封装，常常被开发人员使用。站在OCP（开放封闭原则）的角度讲，该模式对扩展不是开放的，但对于修改而言，却是封闭的。如果创建逻辑发生了变化，可以保证仅修改该静态工厂方法一处。同时，该模式还可以极大地简化对象创建的API。  

在Scala中，通过引入伴生对象（Companion Object）来简化静态工厂方法，语法更加干净，体现了Scala精简的设计哲学。即使不是要使用静态工厂，我们也常常建议为Scala类定义伴生对象，尤其是在DSL上下文中，更是如此，因为这样可以减少new关键字对代码的干扰。  

## 2.Lazy Initialization
lazy修饰符在Scala中有更深远的涵义，例如牵涉到所谓严格（Strictness）函数与非严格（Non-strictness）函数。在Scala中，若未明确声明，所有函数都是严格求值的，即函数会立即对它的参数进行求值。而如果对val变量添加lazy修饰符，则Scala会延迟对该变量求值，直到它第一次被引用时。如果要定义非严格函数，可以将函数设置为by name参数。    

scala的lazy修饰符常常被用作定义一些消耗资源的变量。这些资源在初始化时并不需要，只有在调用某些方法时，才需要准备好这些资源。例如在Spark SQL的QeuryExecution类中，包括optimizedPlan、sparkPlan、executedPlan以及toRdd等，都被定义为lazy val：  

```
class QueryExecution(val sparkSession: SparkSession, val logical: LogicalPlan) {
  lazy val analyzed: LogicalPlan = {
    SparkSession.setActiveSession(sparkSession)
    sparkSession.sessionState.analyzer.execute(logical)
  }
  lazy val withCachedData: LogicalPlan = {
    assertAnalyzed()
    assertSupported()
    sparkSession.sharedState.cacheManager.useCachedData(analyzed)
  }
  lazy val optimizedPlan: LogicalPlan = sparkSession.sessionState.optimizer.execute(withCachedData)
  lazy val sparkPlan: SparkPlan = {
    SparkSession.setActiveSession(sparkSession)
    planner.plan(ReturnAnswer(optimizedPlan)).next()
  }
  lazy val executedPlan: SparkPlan = prepareForExecution(sparkPlan)
  lazy val toRdd: RDD[InternalRow] = executedPlan.execute()
}  
```  

这样设计有一个好处是，当程序在执行到这些步骤时，并不会被马上执行，从而使得初始化QueryExecution变得更快。只有在需要时，这些变量对应的代码才会执行。这也是延迟加载的涵义。  

## 3.Singleton Pattern
C#提供了静态类的概念，但Java没有，而Scala则通过引入Object弥补了Java的这一缺失，而且从语义上讲，似乎比静态类（Static Class）更容易让人理解。  

Object可以派生自多个trait。例如派生自App trait，就可直接享有main函数的福利。  

```
trait App extends DelayedInit {
  def main(args: Array[String]) = {
    this._args = args
    for (proc <- initCode) proc()
    if (util.Properties.propIsSet("scala.time")) {
      val total = currentTime - executionStart
      Console.println("[total " + total + "ms]")
    }
  }
}

object Main extends App
```  

继承多个trait的好处是代码复用。我们可以将许多小粒度方法的实现定义在多个trait中。这些方法如果被类继承，则成为实例方法，如果被Object继承，则变成了线程安全的静态方法（因为继承trait的实现就是一个mixin）。多么奇妙！所以很多时候，我们会尽量保证Obejct的短小精悍，然后将许多逻辑放到trait中。当你看到如下代码时，其实不必惊讶：  

```
object Main extends App 
  with InitHook
  with ShutdownHook
  with ActorSystemProvider
  with ScheduledTaskSupport
```  

这种小粒度的trait既可以保证代码的复用，也有助于职责分离，还有利于测试。真是再好不过了！  

## 4.Adapter Pattern
隐式转换当然可以用作Adapter。在Scala中，之所以可以更好地调用Java库，隐式转换功不可没。从语法上看，隐式转换比C#提供的扩展方法更强大，适用范围更广。  

Pavel Fatin给出了日志转换的Adapter案例：  

```
trait Log {
  def warning(message: String)
  def error(message: String)
}

final class Logger {
  def log(level: Level, message: String) { /* ... */ }
}

implicit class LoggerToLogAdapter(logger: Logger) extends Log {
  def warning(message: String) { logger.log(WARNING, message) }
  def error(message: String) { logger.log(ERROR, message) }
}

val log: Log = new Logger()
```  

这里的隐式类LoggerToLogAdapter可以将Logger适配为Log。与Java实现Adapter模式不同的是，我们不需要去创建LoggerToLogAdapter的实例。如上代码中，创建的是Logger实例。Logger自身与Log无关，但在创建该对象的上下文中，由于我们定义了隐式类，当Scala编译器遇到该隐式类时，就会为Logger添加通过隐式类定义的代码，包括隐式类中定义的对Log的继承，以及额外增加的warning与error方法。  

在大多数场景，Adapter关注的是接口之间的适配。但是，当要适配的接口只有一个函数时，在支持高阶函数（甚至只要支持Lambda）的语言中，此时的Adapter模式就味如鸡肋了。假设Log与Logger接口只有一个log函数（不管它的函数名是什么），接收的参数为(Level, String)，那么从抽象的角度来看，它们其实属于相同的一个抽象：  

```
f: (Level, String) => Unit
```  

任何一个符合该定义的函数，都是完全适配的，没有类型与函数名的约束。  

如果再加上泛型，抽象会更加彻底。例如典型的Load Pattern实现：  

```
def using[A](r : Resource)(f : Resource => A) : A =
    try {
        f(r)
    } finally {
        r.dispose()
    }
```  

泛型A可以是任何类型，包括Unit类型。这里的f扩大了抽象范围，只要满足从Resource转换到A的语义，都可以传递给using函数。更而甚者可以完全抛开对Resource类型的依赖，只需要定义了close()方法，都可以作为参数传入：  

```
def using[A <: def close():Unit, B][resource: A](f: A => B): B =
    try {
        f(resource)
    } finally {
        resource.close()
    }

using(io.Source.fromFile("example.txt")) { source => {
    for (line <- source.getLines) {
        println(line)
    }
  }
}
```  

因为FileResource定义了close()函数，所以可以作为参数传给using()函数。  

## 5.Value Object

Value Object来自DDD中的概念，通常指的是没有唯一标识的不变对象。Java没有Value Object的语法，然而因其在多数业务领域中被频繁使用，Scala为其提供了快捷语法Case Class。在几乎所有的Scala项目中，都可以看到Case Class的身影。除了在业务中表现Value Object之外，还可以用于消息传递（例如AKKA在Actor之间传递的消息）、序列化等场景。此外，Case Class又可以很好地支持模式匹配，或者作为典型的代数数据类型（ADT）。例如Scala中的List，可以被定义为：  

```
sealed trait List[+T]
case object Nil extends List[Nothing]
case class Cons[+T](h: T, t: List[T]) extends List[T]
```  

这里，case object是一个单例的值对象。而Nil与Cons又都同时继承自一个sealed trait。在消息定义时，我们常常采用这样的ADT定义。例如List定义中，Nil与Cons就是List ADT的sum或者union，而Cons构造器则被称之为是参数h（代表List的head）与t（代表List的tail）的product。这也是ADT（algebraic data type）之所以得名。注意它与OO中的ADT（抽象数据类型）是风马牛不相及的两个概念。  

原文链接： http://zhangyi.farbox.com/post/designthinking/design-patterns-with-scala-syntax-sugar