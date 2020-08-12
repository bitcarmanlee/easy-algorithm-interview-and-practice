## 1.单例对象
Scala中没有静态方法或静态字段，但可以使用object这个语法结构来实现相同的功能。Object与class在语法层面上很相似，除了不能提供构造器参数外，object可以拥有class的所有特性。  

废话不多说，直接上代码  

```
object Singleton {

  var count = 0

  def addCount:Long = {
    count += 1
    count
  }
}

object Client {
  def main(args: Array[String]): Unit = {
    println(Singleton.addCount)
    println(Singleton.addCount)
  }
}
```  

让代码run起来  

```
1
2
```  

创建单例对象需要用Object关键字，而非Class。因为单例对象无法初始化，所以不能给它的主构造函数传递参数  
单例一旦定义完毕，它的名字就表示了这个单例对象的唯一一个实例。单例可以传给函数，就像通常传递实例一样  

## 2.伴生类与伴生对象
单例对象可以和类具有相同的名称，此时该对象也被称为“伴生对象”。  
先看代码  

```
class Person private(val name:String){
  private def getSkill() =
    name + "'s skill is: " + Person.skill
}

object Person {
  private val skill = "basketball"
  private val person = new Person("Tracy")
  def printSkill =
    println(person.getSkill())

  def main(args: Array[String]): Unit = {
    Person.printSkill
  }
}
```  

将代码run起来  

```
Tracy's skill is: basketball
```  

Tricks:  
1.伴生类Person的构造函数定义为private，虽然这不是必须的，却可以有效防止外部实例化Person类，使得Person类只能供对应伴生对象使用；  
2.每个类都可以有伴生对象，伴生类与伴生对象写在同一个文件中；  
3.在伴生类中，可以访问伴生对象的private字段Person.skill；  
4.而在伴生对象中，也可以访问伴生类的private方法 Person.getSkill（）；  
5.在外部不用实例化，直接通过伴生对象访问Person.printSkill（）方法  
