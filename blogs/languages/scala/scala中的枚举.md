## 1.scala枚举原理  
严格来说，和其它语言不同，Scala 并没有枚举这种类型。Scala 中的枚举值只是Enumeration下的Value类的实例，而不是枚举自身的实例。Value类的实例主要依靠其构造方法的两个值:id与name来构建。其中，id是自增长，name如果不指定时默认使用的就是值的名字。所以不像其它语言，Scala 并不能任意定义构造方法来构造枚举。  

```
abstract class Enumeration (initial: Int) extends Serializable {
  thisenum =>

  def this() = this(0)
  ...
  protected final def Value(i: Int, name: String): Value = new Val(i, name)
...
  }
  abstract class Value extends Ordered[Value] with Serializable {
    /** the id and bit location of this enumeration value */
    def id: Int
    /** a marker so we can tell whose values belong to whom come reflective-naming time */
    private[Enumeration] val outerEnum = thisenum

    override def compare(that: Value): Int =
      if (this.id < that.id) -1
      else if (this.id == that.id) 0
      else 1
    override def equals(other: Any) = other match {
      case that: Enumeration#Value  => (outerEnum eq that.outerEnum) && (id == that.id)
      case _                        => false
    }
    override def hashCode: Int = id.##

    /** Create a ValueSet which contains this value and another one */
    def + (v: Value) = ValueSet(this, v)
  }

  /** A class implementing the [[scala.Enumeration.Value]] type. This class
   *  can be overridden to change the enumeration's naming and integer
   *  identification behaviour.
   */
  @SerialVersionUID(0 - 3501153230598116017L)
  protected class Val(i: Int, name: String) extends Value with Serializable {
    def this(i: Int)       = this(i, nextNameOrNull)
    def this(name: String) = this(nextId, name)
    def this()             = this(nextId)
    ...
    }
```  
从上面的源码可以看出，真正的主构造方法为`Val(i: Int, name: String)`，下面的辅助构造方法有三个，分别可以只传id，只传name，或者任何参数不传。  

## 2.例子
以一个星期几的枚举为例，看看scala中的枚举如何使用。  

```
object Weekday extends Enumeration {

    type Weekday = Value
    val Monday = Value(1)
    val Tuesday = Value(2, "tue")
    val Wednesday = Value(3)
    val Thursday = Value(4)
    val Friday = Value(5)
    val Saturday = Value(6)
    val Sunday = Value(7)
    val SS = Value

    def main(args: Array[String]): Unit = {
        // 枚举值,Monday只传了id,name默认为枚举值
        val monday = Weekday.Monday
        println(monday)

        // 通过name获得枚举值
        val tuesday = Weekday.withName("tue")
        println(tuesday)

        // 通过id获得枚举值
        println(Weekday(6))

        // 获得id
        println(Weekday.SS.id)
    }
}
```  

输出的结果为  

```
Monday
tue
Saturday
8
```
