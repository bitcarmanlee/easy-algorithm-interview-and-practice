我们经常会听说IoC，也就是Inversion of Controller，控制反转。事实上，IoC并不是一个新鲜的概念，最早可能是在1988年，由Ralph E. Johnson和Brian Foote在论文Designing Reusable Classes中提出。IoC从字面上来说有两个内容，一个是控制，一个是反转。那么什么是控制呢？又是怎样反转的呢？  

为了更好的理解，我们用个实例来说明吧。下面的程序有一个Example类，它含有一个doStuff()方法来完成某件事情。注意，以下的代码都是截取的片段，并不完整。  

如果采用传统的编程：  
Example.java  

```
public class Example {
 
    private DataFinder dataFinder;
 
    public Example(){
        dataFinder = new MysqlDataFinder();
    }
     
    public void doStuff() {
        // 此处具体实现省略
        ...
        dataFinder.getData();
        ...
    }
 
}
```  

此外提供一个DataFinder接口：  
DataFinder.java  

```
public interface DataFinder {
    void getData();
}
```  

MysqlDataFinder实现：  

MysqlDataFinder.java  

```
public class MysqlDataFinder implements DataFinder{
 
    @Override
    public void getData() {
        ...
    }
}
```  

最后有个Main方法：  
Client.java  

```
public class Client {
 
    public static void main(String[] args){
         
        Example example = new Example();
        example.doStuff();
         
    }
}
```  

现在问题来了，因为DataFinder接口有很多不同的实现，譬如可以读取Mysql数据库中的数据MysqlDataFinder，还可能读取Oracle数据库中的数据的OracleDataFinder。它们都实现了DataFinder接口，并有各自的getData()实现。我们要想读取不同的数据源中的数据，就需要实现不同的Example类:  

```
public class Example1 {
 
    private DataFinder dataFinder;
 
    public Example1(){
        dataFinder = new MysqlDataFinder();
    }
     
    public void doStuff() {
        // 此处具体实现省略
        ...
        dataFinder.getData();
        ...
    }
}
 
public class Example2 {
 
    private DataFinder dataFinder;
 
    public Example2(){
        dataFinder = new OracleDataFinder();
    }
     
    public void doStuff() {
        // 此处具体实现省略
        ...
        dataFinder.getData();
        ...
    }
 
}
 
public class Client {
 
    public static void main(String[] args){
         
        Example example1 = new Example1();
        example1.doStuff();
         
        Example example2 = new Example2();
        example2.doStuff();
    }
}
```  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/ioc/1.png)    

Example既依赖于接口DataFinder，又同时依赖实现，因为它需要在编译阶段就确定使用哪种实现，这样显然缺乏灵活性，会产生很多重复的代码，有没有更好的方法减少重复呢？我们首先想到，可以在Example构造器中给个参数，来控制实现的DataFinder类型：  

```
public class Example {
 
    private DataFinder dataFinder;
 
    public Example(){
    }
     
    public Example(int type){
        if(type == 1){
            dataFinder = new MysqlDataFinder();
        }else if(type == 2){
            dataFinder = new OracleDataFinder();
        }
    }
     
    public void doStuff() {
        // 此处具体实现省略
        ...
        dataFinder.getData();
        ...
    }
}
 
public class Client {
 
    public static void main(String[] args){
         
        Example example1 = new Example(1);
        example1.doStuff();
         
        Example example2 = new Example(2);
        example2.doStuff();
    }
}
```  

现在代码变得简单了，但Example类依然依赖具体的实现，实际上Example并不应该有这么多的控制逻辑，它应该只负责调用doStuff()方法来完成工作，至于用什么类型的DataFinder不应该是它考虑的问题。我们试着将控制调用哪种类型DataFinder的任务交给Client类。  

```
public class Example {
 
    private DataFinder dataFinder;
 
    public Example(){
    }
     
    public Example(DataFinder dataFinder){
        this.dataFinder = dataFinder;
    }
     
    public void doStuff() {
        // 此处具体实现省略
        ...
        dataFinder.getData();
        ...
    }
}
 
public class Client {
 
    public static void main(String[] args){
         
        Example example1 = new Example(new MysqlDataFinder());
        example1.doStuff();
         
        Example example2 = new Example(new OracleDataFinder());
        example2.doStuff();
    }
}
```  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/ioc/2.png)    

这样Example不用依赖具体的实现了，不用管到底是用哪种类型的DataFinder。换句话说，就是将调用类Example类对于选择哪个具体DataFinder的控制权从其中移除，转交给Client决定，实现了“控制”的“反转”，这也就是我们所说的IoC。  

我们现在知道了控制反转，我们可以把它看作是一个概念。而依赖注入(Dependency Injection)是控制反转的一种实现方法。James Shore给出了依赖注入的定义：依赖注入就是将实例变量传入到一个对象中去(Dependency injection means giving an object its instance variables)。  

Spring的核心就是依赖注入。Spring支持的注入方式主要有两种：setter注入(setter injection)和构造器注入(constructor injection)。我们上面的代码便是使用的构造器注入。关于注入的这两种方式请查看后续章节。  

此外，对于控制反转还有另外一种实现: service locator。有兴趣的可以研究一下。  

传统编程和IoC的对比  
1.传统编程：决定使用哪个具体的实现类的控制权在调用类本身，在编译阶段就确定了。  
2.IoC模式：调用类只依赖接口，而不依赖具体的实现类，减少了耦合。控制权交给了容器，在运行的时候才由容器决定将具体的实现动态的“注入”到调用类的对象中。  

注：这是博主本人在网络上找了比较长的时间找到的一个关于控制反转与依赖注入比较好的一个文章。没有找到原文的出处，所以没给出具体的链接地址。  