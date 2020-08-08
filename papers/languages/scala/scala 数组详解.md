## 1.初始化数组
想要初始化数组，可以跟java里面一样，使用new关键字，指定数据类型与数组长度。  

```
    def test() = {
        val arr = new Array[Int](3)
        arr.foreach(x => print(x + ","))
    }
```  

上面代码run起来以后：  

```
0,0,0,
```  

也可以不使用new关键字，直接提供初始值：    

```
    def test() = {
        val arr = Array[Int](3)
        arr.foreach(x => print(x + ","))
    }
```  

注意此时run起来以后，结果就为:  

```
3,
```  

通过上面的例子，很容易看出有没有new关键字，区别还是很大的。  

## 2.初始化变长数组
很多时候，我们需要长度可变的数组。比如在java中，很常用的就是ArrayList。在Scala中，则有ArrayBuffer这一神器。为了看清楚ArrayBuffer的用法，直接上源码。  


```
    def test() = {
        val arrBuffer = ArrayBuffer[Int]()
        //数组末尾添加一个元素
        arrBuffer += 1
        //数组末尾添加多个元素
        arrBuffer += (2,3,4)
        //数组末尾添加另外一个数组
        arrBuffer ++= Array(5,6,7)
        printArr(arrBuffer)  // 1,2,3,4,5,6,7,
        //删除最后一个元素
        arrBuffer.trimEnd(1)
        //删除第一个元素
        arrBuffer.trimStart(1)
        printArr(arrBuffer) // 2,3,4,5,6,
        //在指定位置插入元素
        arrBuffer.insert(1,0)
        printArr(arrBuffer) // 2,0,3,4,5,6,
        //在指定位置插入序列
        arrBuffer.insert(2,1,2,3)
        printArr(arrBuffer) // 2,0,1,2,3,3,4,5,6,
        //删除指定位置元素
        arrBuffer.remove(0)
        printArr(arrBuffer) // 0,1,2,3,3,4,5,6,
        //删除指定位置以后的若干个元素
        arrBuffer.remove(0,4)
        printArr(arrBuffer) // 3,4,5,6,
    }

    def printArr(arrBuffer: ArrayBuffer[Int]) = {
        arrBuffer.foreach(x => print(x + ","))
        println()
    }
```  

## 3.Array与ArrayBuffer相互转换
如果我们需要在Array与ArrayBuffer中进行相互转换，操作也很简单。  

```
    def test() = {
        val arrayBuffer = ArrayBuffer(1,2,3)
        val res = arrayBuffer.toArray

        val array = Array[Int](5,6,7)
        val buf = array.toBuffer
    }

```  

## 4.数组遍历
集合遍历是最常见的做法。一般用for循环就可以搞定：  

```
    def test() = {
        val array = Array("a", "b", "c", "d")
        for(i <- 0 until array.length)
            println(i + ":" + array(i))
    }
```  

将代码run起来以后，输出如下：  

```
0:a
1:b
2:c
3:d
```  

如果想将步长调整为2：  

```
for(i <- 0 until (array.length,2))
```  

如果想实现逆序遍历：  

```
for(i <- (0 until (array.length)).reverse)
```  

在java中有增强型for循环，scala中自然也提供了这一方便的操作：  

```
for(item <- array)
```  

## 5.一些实用的操作
数组有一些经常使用，特别好用的操作，也一并列出来。  

```
    def test() = {
        val array = Array(1,2,3,4,5)
        println(array.sum) //15
        println(array.max) //5
        println(array.min) //1
        println(array.mkString("-")) //1-2-3-4-5,实际项目中经常使用
        println(array.mkString("(", "-",")")) //(1-2-3-4-5)
    }
```  

## 6.一些其他操作
使用yield产生一个新数组  

```
    def test() = {
        val array = Array(2, 4, 5, 6, 7)
        val res = for(item <- array if item % 2 == 0) yield item * 2
        res.foreach(x => print(x + ",")) // 4,8,12,
    }
```  
上面的操作等价于以下代码：  

```
array.filter(_ % 2 == 0).map(_ * 2)
```  
