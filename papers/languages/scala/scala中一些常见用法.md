## 1.花括号与小括号的区别
以下代码的用法，非常常见：  

```
val raw = List(("a",1),("b",2),("c",3))
val res = raw.map{ case (key,value) => value }.reduce(_ + _)
println(res)
```  

注意这里如果将map方法的大括号换成小括号，代码会报错。  
方法中的花括号有2种意思：  
1）scala中函数的小括号，可以用花括号来表示，即foo{xx} 与 foo(xx)是一回事儿。  
2）对于只有一个参数的方法，其小括号是可以省略的，map(lambda)可写为 map lambda，即这块{case (key,value) => value} 连同花括号整体是一个lambda(函数字面量)。  


这里很明显花括弧啊的用法是第二种。  

## 2.case偏函数
以下代码的用法，也非常常见：  

```
val res2 = List(1,2,3).map{
   case 1 => "first"
   case 2 => "second"
   case _ => "other"
  }
```  

{case x => y} 叫做偏函数(必须用大括号“｛｝”，使用“（）”会报错)。 与完全函数想对应，普通的方法都是完全函数，即f(i:Int) = xxx 是将所有Int类型作为参数的，是对整个Int集的映射；而偏函数则是对部分数据的映射。  

## 3.变长参数
有时候，函数需要一个可变长度的参数。在scala中是容易实现的：  

```
object T1 {

  def sum(args:Int*) = {
    var result = 0
    for(arg <- args) result += arg
    result
  }

  def main(args: Array[String]): Unit = {
    val s = sum(1 to 5:_*)
    println(s)
  }
}
```  

注意调用的时候使用:_*，将序列或者集合的内容全部当做参数来传递。  

## 4.asInstanceOf[AnyRef]  

```
val str = MessageFormat.format("The answer to {0} is {1}","everything",40.asInstanceOf[AnyRef])
```  

这种写法很常见，对于任意的Object类型的参数都是可以这样。这种类似的参数在变长参数方法中使用最多。  