在函数式语言中，函数是一等公民，也是最基本的功能块。通常为了使代码更加清晰易读，我们往往会写许多辅助函数。但是大家都知道，给函数或者变量起个合适的名字，是coding中最难的任务，没有之一。函数多了以后，很容易名字就冲突，而且暴露给外部过多的函数也会带来各种问题。在java里，我们是通过private method这种方式来解决。当然，scala里也可以这么干。但是我们既然说scala是函数式语言，那我们就采用函数式语言的方式来解决这个问题：在函数内部再定义函数。就像局部变量一样,其作用 域仅限于外部函数内部。  

在 http://blog.csdn.net/bitcarmanlee/article/details/52194255 一文中，我们提到了用牛顿法求解方根。现在我们以此为例，来看看scala中怎么实现。  

## 1.常规方式，定义很多外部函数

```
object Demo {

  //满足终止条件
  def isGoodEnough(guess:Double,x:Double) =
    abs(guess * guess - x) < 0.0001
  //返回绝对值
  def abs(x:Double) =
    if (x<0) -x else x
  //迭代公式
  def sqrtIter(guess:Double,x:Double):Double =
    if (isGoodEnough(guess,x))
      guess
    else
      sqrtIter((guess + x/guess)/2,x)
  //默认从1开始迭代
  def sqrt(x:Double):Double =
    sqrtIter(1,x)
    
  def main(args: Array[String]): Unit = {
    println(sqrt(2))
  }
}
```  

将代码run起来：  

```
1.4142156862745097
```  

上面的代码，总共定义了4个函数。但是对于用户来说，用户只关心sqrt函数，而我们一下暴露了4个函数给用户。scala 里可以内部函数，我们可以将这些辅助函数定义为 sqrt的内部函数，更进一步，由于内部函数可以访问其函数体外部定义的变量，我们可以去掉这些辅助函数中的 x参数，代码将会变得更为简洁，内部函数访问包含该函数的参数是非常常见的一种嵌套函数的用法。  

## 2.使用内部函数

```
object Demo {
  def sqrtEncapsulation(x:Double):Double = {

    def sqrtIter(guess:Double):Double = {
      if(isGoodEnough(guess))
        guess
      else
        sqrtIter((guess + x/guess) / 2)
    }
    def isGoodEnough(guess:Double) = {
      abs(guess * guess - x) < 0.0001
    }
    def abs(x:Double) = {
      if(x < 0) -x else x
    }

    sqrtIter(1)
  }

  def main(args: Array[String]): Unit = {
    println(sqrtEncapsulation(2))
  }
}
```  

是不是经过这么包装以后，代码的可读性更强，封装得也更好，使用起来也更为方便呢？
