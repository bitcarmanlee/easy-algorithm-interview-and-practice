## 1.可变参数的定义
从JDK1.5之后，java就提供了变长参数(variable arguments，varargs)。我们在定义方法的时候，可以使用不确定个数的参数。对于同一个方法，也可以通过不确定参数个数的方式进行重载。首先来看个最简单的例子:  

```
public void printArray(String... args) {
    for(int i=0; i<args.length; i++) {
        System.out.print(args[i] + " ");
    }
}
```  

在main方法里调用此方法，例如：  

```
printArray("hello","world");
```  

这个时候控制台会打印出`hello world `！以上就是可变参数最简单的应用方式。  

## 2.与固定参数方法的比较
如果某一方法被调用的时候，既能与固定参数个数的方法match，也能与被重载的有可变参数的方法match，那么优先调用固定参数个数的方法。  

```
public class MultiPrameters {

    public void printArray(String... args) {
        for(int i=0; i<args.length; i++) {
            System.out.print(args[i] + " ");
        }
    }

    public void printArray(String rawString) {
        System.out.println("only one string!");
    }

    public static void main(String[] args) {
        MultiPrameters mul = new MultiPrameters();
        mul.printArray("hello");
        mul.printArray("hello","world");
    }

}
```  

将上面的代码run起来以后，控制台输出如下：  

```
only one string!
hello world 
```  

## 3.每个方法最多一个变长参数，并且该参数的位置是方法的的最后

```
public void print(String... args,Int num){}
 
public void print(String... args,Int... nums){}
```  

以上两种写法，都是错误的！  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/args/1.png)  

IDE里会直接提示你:Vararg paramter must be the last in the list!  

## 4.注意不能让调用的方法可以与两个可变参数匹配
理解起来也不是很复杂，大家看如下示例代码  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/args/2.png)  

IDE里直接报错，ambiguous method call both! 很明显，main方法调用的时候不知道调用哪个printArray方法！所以我们在实际编码过程中，避免带有变长参数方法的重载  