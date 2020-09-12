在别的编码语言中，break与continue两种控制语句是非常常见的用法，一般也有对应的关键字。但是在scala中，没有专门的break与continue关键字。那怎么在循环中实现break与continue功能呢？  

## 1.实现break功能

```
package com.xiaomi.leilei.test1

import scala.util.control.Breaks._

/**
  * Created by wanglei on 17/8/11.
  */
object breakdemo {

    def breaktest() = {
        val arr = Array(1, 2, 3, 4, 5, 6)
        breakable {
            arr.foreach { x =>
                if (x > 3) break
                else println(x)
            }
        }
    }

    def main(args: Array[String]): Unit = {
        breaktest()
    }

}

```  

最后的输出结果为：  

```
1
2
3

```  

## 2.实现continue功能

```
package com.xiaomi.leilei.test1

import scala.util.control.Breaks._

/**
  * Created by wanglei on 17/8/11.
  */
object breakdemo {

    def continuetest() = {
        val arr = Array(1, 2, 3, 4, 5, 6)
        arr.foreach {
            x => breakable {
                if(x == 4) break()
                else println(x)
            }
        }
    }

    def main(args: Array[String]): Unit = {
        continuetest()
    }

}

```  

通过上面的代码不难发现，实现break与continue功能，都需要`util.control.Breaks._`类的辅助。不同的是，将整个循环的逻辑放在breakable方法中，在需要真正跳出循环的时候使用break方法，这样达到了跳出整个循环的目的。而continue功能是将breakable放在循环内，这样可以实现结束本次循环的目的而不是结束整个循环。  

## 3.Breaks的部分源码

```
package scala
package util.control

/** A class that can be instantiated for the break control abstraction.
 *  Example usage:
 *  {{{
 *  val mybreaks = new Breaks
 *  import mybreaks.{break, breakable}
 *
 *  breakable {
 *    for (...) {
 *      if (...) break()
 *    }
 *  }
 *  }}}
 *  Calls to break from one instantiation of `Breaks` will never
 *  target breakable objects of some other instantiation.
 */
```  

如果翻译过来就是说:  
1.Breaks是一个可以实例化为中断控制抽象的类。  
2.Breaks的实例对象永远不用破坏要被中断对象的实例。  
3.注释中给出了明确的要实现break功能的代码样式。  