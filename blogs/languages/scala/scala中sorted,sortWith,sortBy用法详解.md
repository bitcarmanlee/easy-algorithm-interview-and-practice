scala的集合中提供了三种排序的方式：sorted,sortWith,sortBy。那么这三种方式有什么不同呢？下面我们结合源码来分析一下  

## 1.sorted
先来看看scala中sorted的源码。  

```
  def sorted[B >: A](implicit ord: Ordering[B]): Repr = {
    val len = this.length
    val arr = new ArraySeq[A](len)
    var i = 0
    for (x <- this.seq) {
      arr(i) = x
      i += 1
    }
    java.util.Arrays.sort(arr.array, ord.asInstanceOf[Ordering[Object]])
    val b = newBuilder
    b.sizeHint(len)
    for (x <- arr) b += x
    b.result
  }
```  

源码中有两点值得注意的地方：  
1.sorted方法中有个隐式参数ord: Ordering。  
2.sorted方法真正排序的逻辑是调用的java.util.Arrays.sort。  

## 2.sortBy
看看sortBy的源码，很简单。  

```
  def sortBy[B](f: A => B)(implicit ord: Ordering[B]): Repr = sorted(ord on f)
```  

sortBy最后也是调用的sorted方法。不一样的地方在于，sortBy前面还需要提供一个属性。  

## 3.sortWith
sortWith的源码如下。  

```
def sortWith(lt: (A, A) => Boolean): Repr = sorted(Ordering fromLessThan lt)
```  

跟前面两个不同的是，sortWith需要传入一个比较函数用来比较！  

## 4.实例
理论部分说完了，下面来干货  

```
object ImplicitValue {
	
	implicit val KeyOrdering = new Ordering[String] {
		override def compare(x: String, y: String) : Int = {
			y.compareTo(x)
		}
	}
}

```  

首先定义了一个隐式比较器。  

```
	def test1() = {
		import ImplicitValue.KeyOrdering
		val list = List( "a", "g", "F", "B", "c")
		val sortedList = list.sorted
		println(sortedList) // List(g, c, a, F, B)
	}
```  
注意因为我们将隐式比较器import了进来，这个时候sorted排序的规则是按照我们自定义的比较器进行比较。在我们自定义的比较器中，定义的是按字符串逆序，所以最终的输出结果为字符串按从大到小的顺序排列！  


再来看看sortWith的用法。  

```
	//忽略大小写排序
	def compareIngoreUpperCase(e1: String, e2: String) : Boolean = {
		e1.toLowerCase < e2.toLowerCase
	}
	
	def test2() = {
		val list = List( "a", "g", "F", "B", "c")
		val sortWithList1 = list.sortWith(_ < _) // List(B, F, a, c, g)
		val sortwithList2 = list.sortWith((left, right) => left < right) //List(B, F, a, c, g)
		val sortwithList3 = list.sortWith(compareIngoreUpperCase) // List(a, B, c, F, g)
		println(sortWithList1)
		println(sortwithList2)
		println(sortwithList3)
	}
```  

本例中， sortWithList1与sortWithList2最终的结果是一致的，只不过写法不一样而已，都是按字符串从小到大的顺序排列。sortwithList3则是按照传入的compareIngoreUpperCase函数进行排序！  

最后看看sortBy的代码  

```
	def test3() = {
		val m = Map(
			-2 -> 5,
			2 -> 6,
			5 -> 9,
			1 -> 2,
			0 -> -16,
			-1 -> -4
		)
		//按key排序
		m.toList.sorted.foreach{
			case (key, value) =>
				println(key + ":" + value)
		}
		println
		
		//按value排序
		m.toList.sortBy(_._2).foreach {
			case (key, value) =>
				println(key + ":" + value)
		}
	}
```  

最后的输出结果为：  

```
-2:5
-1:-4
0:-16
1:2
2:6
5:9

0:-16
-1:-4
1:2
-2:5
2:6
5:9

```  