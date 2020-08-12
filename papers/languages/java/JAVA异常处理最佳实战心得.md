## 1.异常分类
异常Exception是Java中非常常用的功能，它可以简化代码，并且增强代码的安全性。尤其是在各种服务相关的代码中，可能正常业务逻辑的代码量很少，大部分都是各种try catch处理各种异常的代码，因为实际中异常情况很多，为了保证服务的健壮与稳定性，要尽可能考虑与处理掉各种异常情况。所以在java中遇到大段大段的try catch也就不足为奇。  

![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/exception/1.jpeg)  
(图片来自网络)  

从上面的图可以看出来，  
1.Throwable是所有异常的根，java.lang.Throwable  
2.Throwable包括Error与Exception两个子类。  
3.Error类一般是指与虚拟机相关的问题，如系统崩溃，虚拟机错误，内存空间不足，方法调用栈溢出等。如java.lang.StackOverFlowError和Java.lang.OutOfMemoryError。对于这类错误，Java编译器不去检查他们，编译器也没法提前发现。对于这类错误导致的应用程序中断，仅仅靠程序本身是无法恢复与预防的。所以对于Error，一般是程序直接终止停止运行。  
4.Exception类为程序可以处理的异常。遇到这种类型的异常，一般在代码中会去做相关处理，并且让程序恢复运行，而不是直接让程序终止运行。  

## 2.Runtime Exception 与 Checked Exception
Runtime Exception一般表示虚拟机层面操作中可能遇到的异常，是一种常见运行时错误。运行时异常在代码中不一定要求捕获或者抛出。  
常见的RuntimeException  
1.NullPointerException NullPointerException是开发中最常见的UncheckedException，尤其实在代码调试阶段。如果在一个空指针上引用方法或变量或对象等，编译器编译的时候不会报错，但是运行期会抛出NullPointerException。  
2.ArithmeticException 算术运算异常 最常见的为除数为0  
3.IllegalArgumentException 传递非法参数异常  
4. IndexOutOfBoundsException 下标越界异常 这个我们在处理各种数组，集合的时候也经常遇到。  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/exception/2.png)  

Checked exceptions与runtime exception的目的不尽相同。Checked exception一般用来指示一种调用方能够直接处理的异常情况。而runtime exception一般是虚拟机层面的问题，代表一种调用方本身无法处理或恢复的程序错误。  

checked exceptions意味着不在程序的即时控制内的错误场景。它们通常与外部资源/网络资源交互，例如数据库问题、网络连接错误、丢失文件等。程序中经常要处理各种资源文件，所以像FileNotFoundException这种异常就很常见。FileNotFoundException的继承关系如下图。  

![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/exception/3.png)  

## 3.异常处理的基本方法
Java的异常处理本质上是抛出异常和捕获异常。  
抛出异常：要理解抛出异常，首先要明白什么是异常情形（exception condition），它是指阻止当前方法或作用域继续执行的问题。其次把异常情形和普通问题相区分，普通问题是指在当前环境下能得到足够的信息，总能处理这个错误。对于异常情形，已经无法继续下去了，因为在当前环境下无法获得必要的信息来解决问题，你所能做的就是从当前环境中跳出，并把问题提交给上一级环境，这就是抛出异常时所发生的事情。抛出异常后，会有几件事随之发生。首先，是像创建普通的java对象一样将使用new在堆上创建一个异常对象；然后，当前的执行路径（已经无法继续下去了）被终止，并且从当前环境中弹出对异常对象的引用。此时，异常处理机制接管程序，并开始寻找一个恰当的地方继续执行程序，这个恰当的地方就是异常处理程序或者异常处理器，它的任务是将程序从错误状态中恢复，以使程序要么换一种方式运行，要么继续运行下去。  
捕获异常：在方法抛出异常之后，运行时系统将转为寻找合适的异常处理器（exception handler）。潜在的异常处理器是异常发生时依次存留在调用栈中的方法的集合。当异常处理器所能处理的异常类型与方法抛出的异常类型相符时，即为合适的异常处理器。运行时系统从发生异常的方法开始，依次回查调用栈中的方法，直至找到含有合适异常处理器的方法并执行。当运行时系统遍历调用栈而未找到合适的异常处理器，则运行时系统终止。同时，意味着Java程序的终止。  

对于运行时异常、错误和检查异常，Java技术所要求的异常处理方式有所不同。  

由于运行时异常及其子类的不可查性，为了更合理、更容易地实现应用程序，Java规定，运行时异常将由Java运行时系统自动抛出，允许应用程序忽略运行时异常。  

对于方法运行中可能出现的Error，当运行方法不欲捕捉时，Java允许该方法不做任何抛出声明。因为，大多数Error异常属于永远不能被允许发生的状况，也属于合理的应用程序不该捕捉的异常。  

对于所有的检查异常，Java规定：一个方法必须捕捉，或者声明抛出方法之外。也就是说，当一个方法选择不捕捉检查异常时，它必须声明将抛出异常。  
(此部分内容来自参考文献1)  

## 4.异常处理常见的样例
与异常处理相关的关键字有如下几个：try,catch,finally,throw,throws。所有异常的处理都围绕这几个字展开。  
try:　用于监听，判断try代码块中的内容是否有异常。如果发生异常，将会被跑出来。  
catch:　捕获try代码块中的相关异常。   
finally:　finally 关键字用来创建在 try 代码块后面执行的代码块。无论是否发生异常，finally 代码块中的代码总会被执行。在 finally 代码块中，可以运行清理类型等收尾善后性质的语句。比如关闭数据库连接、断开网络连接和关闭磁盘文件等。  
throw:　用来抛出异常。  
throws:　如果一个方法没有捕获到一个检查性异常，那么该方法必须使用 throws 关键字来声明，用在方法签名中。  

### 4.1 try-catch方式捕获异常
这种是最常见的处理异常的方式。一般的用法如下：  

```
try{
    //do something and might generate some exceptions    
}catch(Exception e1){
    //handling exception1
}catch(Exception e2){
    //handling exception2
}
```  

如果抛出的异常对象属于catch子句的异常类，或者属于该异常类的子类，则认为生成的异常对象与catch块捕获的异常类型相匹配。  
如果有多重catch，整体的原则为：先catch住子类，再catch父类，层层递进。  

举个例子：  

```
try{
    //code open a file
}catch(FileNotFoundException e1){
    //handling e1
}catch(IOException e2){
    //handling e2
}catch(Exception e3){
    //handling e3
}
```  

### 4.2 try-catch-finally方式捕获异常  
这种方式也很常见。与上面唯一的区别在于多了一个finally部分用来处理一些售后工作。  

```
try{
    //code open a file
}catch(FileNotFoundException e1){
    //handling e1
}catch(IOException e2){
    //handling e2
}catch(Exception e3){
    //handling e3
}finally(){
    //close the file
}
```  

### 4.3 方法中throw出异常  
上面的方式，我们都是去捕获系统抛出的异常，当然我们也可以抛出来异常。在实际项目中，我们经常自己定义各种异常，方便快速定位与查找系统异常。  
自己抛出异常也非常简单  

```
throw ThrowableObject
```  
只需要抛出一个Throwable的对象即可。比如我们经常用类似的方法这么做：  

```
public class TestThrow extends Exception {

    public static class SomeException extends Exception {
        // nothing to do
    }

    public static void main(String[] args) {
        try {
            throw new SomeException();
        } catch (SomeException ex) {
            ex.printStackTrace();
        }
    }
}
```  

先定义一个名为SomeException的类，该类继承自Exception。然后在逻辑中先抛出这个异常再catch住。  
注意throw是在函数内。  

### 4.4 throws
如果一个方法可以导致一个异常，但是在这个方法内我们不想处理，想交给他的调用者去处理，这个时候可以采用throws的方式。要做到这点，我们可以在方法声明中包含一个throws子句。一个throws子句列举了一个方法可能引发的所有异常类型，可以包括多个异常。  

例如我们经常写的mapreduce程序里，mapper阶段的map方法就throws出来有两个异常：  

```
  protected void map(KEYIN key, VALUEIN value, 
                     Context context) throws IOException, InterruptedException {
    context.write((KEYOUT) key, (VALUEOUT) value);
  }
```  

所以我们每次重写map方法的时候，也会throws出这两个异常。  
注意throws是在方法签名中，而不是在方法内部！  


## 5.throw与throws的区别
throw语句在方法体内，标识抛出异常，有方法体内的语句来处理。一旦执行到throw语句，说明肯定要抛出异常，程序执行完throw语句之后立即停止；throw后面的任何语句不被执行，最邻近的try块用来检查它是否含有一个与异常类型匹配的catch语句。如果发现了匹配的块，控制转向该语句；如果没有发现，次包围的try块来检查，以此类推。如果没有发现匹配的catch块，默认异常处理程序中断程序的执行并且打印堆栈轨迹。  
throws语句在方法签名中，主要是声明这个方法会抛出这种类型的异常，使它的调用者知道要捕获这个异常。只是说该方法有可能要抛出某些异常。  

### 6.finally中不要改变返回值
finally子句是可选项，可以有也可以没有。但是每个try语句至少需要一个catch或者finally子句。  
如果try里面有个return语句，try 后的 finally{} 里的 code 会在方法返回调用者前被执行。  
什么意思呢？总结起来一句话：在finally中改变返回值的做法是不好的。因为如果存在finally代码块，try中的return语句不会立马返回调用者，而是记录下返回值待finally代码块执行完毕之后再向调用者返回其值，然后如果在finally中修改了返回值，就会返回修改后的值。显然，在finally中返回或者修改返回值会对程序造成很大的困扰。  
看两个例子：  

```
public static int test() {
    int result = 0;
    try {
        result = 1;
        return result;
    } catch (Exception e) {
        result = 2;
        return result;
    } finally {
        result = 3;
    }
}
```  

上面这段代码，方法的返回值是1。  

```
public class TestFinally extends Exception {
    public static class Person {
        public String name;
        public Person(String name) {
            this.name = name;
        }
    }

    public static Person test() {
        Person person = new Person("lili");
        try {
            person.name = "mm";
            return person;
        } catch (Exception ex) {
            return person;
        } finally {
            person.name = "yy";
        }
    }

    public static void main(String[] args) {
        Person person = test();
        System.out.println(person.name);
    }
}
```  

以上代码输出为yy!  

如果finally中没有return语句，但是改变了要返回的值，这里有点类似与引用传递和值传递的区别，分以下两种情况，：  

1）如果return的数据是基本数据类型或文本字符串，则在finally中对该基本数据的改变不起作用，try中的return语句依然会返回进入finally块之前保留的值。  

2）如果return的数据是引用数据类型，而在finally中对该引用数据类型的属性值的改变起作用，try中的return语句返回的就是在finally中改变后的该属性的值。  

不管怎么说，在finally中返回或者修改返回值都不是一件好事情，墙裂建议大家不这么干。   

## 参考文献：
1.https://www.cnblogs.com/Qian123/p/5715402.html#_label2  
2.https://blog.csdn.net/Next_Second/article/details/73090994  