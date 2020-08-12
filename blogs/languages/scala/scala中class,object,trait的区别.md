## 1.object
object的特点是：  
1.可以拥有属性和方法，且默认都是"static"类型，可以直接用object名直接调用属性和方法，不需要通过new出来的对象（也不支持）。  
2.object里的main函数式应用程序的入口。  
3.object和class有很多和class相同的地方，可以extends父类或Trait，但object不可以extends object，即object无法作为父类。  

## 2.class
一个主构造器（函数），其他是辅助构造器  
辅助构造器的实现体里，必须引用（调用）主构造器  
主构造器的参数，也会成为类的属性  
辅助构造函数的名称都是this   
辅助构造函数中必须以一个其他辅助构造器或主构造器的调用开始。  
构造函数  

生成的字段方法  
name:String　对象私有字段。如果没有方法使用name,则没有该字段。  
Private val/var name String   私有字段，私有getter/setter方法。  
Val/var name:String   私有字段，公有getter/setter方法  

scala类中是没有static方法的，那么如何实现某个类既有普通方法又有静态方法？伴生对象就可以满足这个要求，伴生类和伴生对象可以相互访问彼此的私有成员。  

```
class TestClass(val id: Int) {

    def this(id1: Int, id2: Int) {
        this(id1)
    }

    def add2(a: Int, b: Int) = {
        a + b
    }
}

object TestClass {

    def apply(id: Int)= {
        println("-----------apply--------")
        new TestClass(id)
    }

    def add(a: Int, b: Int): Int = {
        a + b
    }

    def main(args: Array[String]): Unit = {
        val r1 = TestClass.add(1, 2)
        println(s"r1 is: $r1")

        val t1 = new TestClass(1)
        val r2 = t1.add2(3, 4)
        println(s"r2 is: $r2")

        val t2 = TestClass(100000)
        println(s"t2.id is: ${t2.id}")

        val t3 = new TestClass(100, 200)
        println((s"t3.id is: ${t3.id}"))
    }
}

```  

输出结果为:  

```
r1 is: 3
r2 is: 7
-----------apply--------
t2.id is: 100000
t3.id is: 100
```  

## 3.trait
Scala的Trait相当于Java里的Interface，但Trait不仅可以定义函数，还可以有函数体实现。实现关键词是extends，实现多个Trait用with。当extends的多个Trait里有相同函数时，子类必须重写该函数。  

父trait里无函数体的函数，子类必须override  
重写父类里有函数体的函数，必须有关键词override  
trait里的变量，都是val类型  
在trait里定义的的变量，必须是val类型，如果变量没初始化，子类必须override  

```
trait TestTrait {
    def printfun()
}

class TestTraitImp extends TestTrait {
    override def printfun(): Unit = {
        println("I'm TestTrait implement!")
    }
}

object TestClass {
	def main(args: Array[String]): Unit = {
	    val t4 = new TestTraitImp()
        t4.printfun()
    }
}
```  

运行的结果为  

```
I'm TestTrait implement!
```  

## 4.scala类层级结构  
Scala里，每个类都继承自通用的名为Any的超类。因为所有的类都是Any的子类，所以定义在Any中的方法就是“共同的”方法：它们可以被任何对象调用。  

Any有两个子类：AnyVal和AnyRef(相当于Java里的Object)。  

AnyVal是Scala里每个内建值类的父类。有9个这样的值类：Byte、Short、Char、Int、Long、Float、Double、Boolean和Unit。其中的前8个都对应到Java的基本类型。这些值类都被定义为既是抽象的又是final的，不能使用new创造这些类的实例。Unit被用作不返回任何结果的方法的结果类型。Unit只有一个实例值，写成()。  
AnyRef类是Scala里所有引用类(reference class)的基类。它其实是Java平台上java.lang.Object类的别名。因此Java里写的类和Scala里写的都继承自AnyRef。  
scala.Null和scala.Nothing是用统一的方式处理Scala面向对象类型系统的某些“边界情况”的特殊类型。Null类是null引用对象的类型，它是每个引用类（继承自AnyRef的类）的子类。Null不兼容值类型。Nothing类型在Scala的类层级的最低端；它是任何其他类型的子类型。然而，根本没有这个类型的任何值。Nothing的一个用处是它标明了不正常的终止。  

## 5.scala实现单例模式
因为scala中没有static，所以我们用伴生对象来实现单例模式。  

```
class SingleModel {
    def printfunc() = {
        println("this is SingleModel!")
    }

}

object SingleModel {
    private var instance: SingleModel = null

    def getInstance() = {
        if (instance == null) {
            this.synchronized {
                if (instance == null) {
                    instance = new SingleModel()
                }
            }
        }
        instance
    }
}
```  

客户端调用的代码如下  

```
object SingleModelClient {

    def main(args: Array[String]): Unit = {
        val instance = SingleModel.getInstance()
        instance.printfunc()
    }
}
```  

最后的输出为  

```
this is SingleModel!
```  
