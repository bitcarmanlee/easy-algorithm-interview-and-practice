## 1.函数式编程带来的好处
函数式编程近些年异军突起，又重新回到了人们的视线，并得到蓬勃发展。总结起来，无外乎如下好处：  
1.减少了可变量(Immutable Variable)的声明，程序更为安全。  
2.相比命令式编程，少了非常多的状态变量的声明与维护，天然适合高并发多现成并行计算等任务，这也是函数是编程近年又大热的重要原因。  
3.代码更为简洁，可读性更强，对强迫症的同学来说是个重大福音。  

## 2.函数式编程的本质
函数式编程中的函数这个术语不是指计算机中的函数（实际上是Subroutine），而是指数学中的函数，即自变量的映射。也就是说一个函数的值仅决定于函数参数的值，不依赖其他状态。比如sqrt(x)函数计算x的平方根，只要x不变，不论什么时候调用，调用几次，值都是不变的。  

引用知乎上的一段描述：  
纯函数式编程语言中的变量也不是命令式编程语言中的变量，即存储状态的单元，而是代数中的变量，即一个值的名称。变量的值是不可变的（immutable），也就是说不允许像命令式编程语言中那样多次给一个变量赋值。比如说在命令式编程语言我们写“x = x + 1”，这依赖可变状态的事实，拿给程序员看说是对的，但拿给数学家看，却被认为这个等式为假。  

函数式语言的如条件语句，循环语句也不是命令式编程语言中的控制语句，而是函数的语法糖，比如在Scala语言中，if else不是语句而是三元运算符，是有返回值的。  

## 3.实例
### 1.集合中包含某一个元素
经常有判断集合是否包含某一元素的需求。在命令式编程中，我们一般都会这么干：  

```
public class IfExists {

    public static void traditional() {
        boolean flag = false;
        String[] citys = {"bj","sh","gz","sz"};
        for(String city:citys) {
            if(city.equals("bj")) {
                flag = true;
                break;
            }
        }
        System.out.println(flag);
    }

    public static void main(String[] args) {
        traditional();
    }
}
```  

这段代码正常工作肯定是没有问题的。而且逻辑本身也很简单，大家都能写出来。但是在我看来，是不是太长了。。。  

看看我们用scala实现一下  

```
object IfExists{

  def main(args: Array[String]): Unit = {
    println(Array("bj","sh","gz","sz").contains("bj"))
  }
}
```  

直接针对集合进行操作，省去了讨厌的循环判断等一系列对我们来说累赘得很的操作。瞬间感觉清爽好多有木有。  

### 2.对一个集合做一系列处理
现在有个价格的集合。如果价格大于20，先九折，然后相加。如果用java实现  

```
public class Price {

    public final static List<BigDecimal> prices = Arrays.asList(
        new BigDecimal("10"), new BigDecimal("30"), new BigDecimal("17"),
        new BigDecimal("20"), new BigDecimal("15"), new BigDecimal("18"),
        new BigDecimal("45"), new BigDecimal("12"));

    public static void sumOfPrices() {
        BigDecimal total = BigDecimal.ZERO;
        for(BigDecimal price:prices) {
            if(price.compareTo(BigDecimal.valueOf(20)) > 0) {
                total = total.add(price.multiply(BigDecimal.valueOf(0.9)));
            }
        }
        System.out.println("The total is: " + total);
    }

    public static void main(String[] args) {
        sumOfPrices();
    }
}
```  

这代码也可以正常工作没有问题。问题跟前面一样，还是太累赘，不是那么优雅，可读性也不是很好。用scala写一下上面的逻辑：  

```
object Prices {

  def main(args: Array[String]): Unit = {
    val prices = Array(10, 30, 17, 20, 15, 18, 45, 12)
    val total = prices.filter(x => x>20)
      .map(x => x*0.9)
      .reduce((x,y) => x+y)
    println("total is: " + total)
  }
}
```  

简直就是强迫症患者的福音有木有！而且这段代码的可读性不知道高了多少：针对集合，先做filter操作，将大于20的元素选出来，然后做map操作，乘以0.9的系数，最后再将所有的值相加。接近于自然语言的表达方式，一目了然。  