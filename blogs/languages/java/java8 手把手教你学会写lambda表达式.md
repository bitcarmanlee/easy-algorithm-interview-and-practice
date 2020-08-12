Java8发布已经有一段时间了，这次发布的改动比较大，很多人将这次改动与Java5的升级相提并论。Java8其中一个很重要的新特性就是lambda表达式，允许我们将行为传到函数中。  
想想看，在Java8之前我们想要将行为传入函数，仅有的选择就是匿名内部类。Java8发布以后，lambda表达式将大量替代匿名内部类的使用，简化代码的同时，更突出了原来匿名内部类中最重要的那部分包含真正逻辑的代码。尤其是对于做数据的同学来说，当习惯使用类似scala之类的函数式编程语言以后，体会将更加深刻。现在我们就来看看Java8中lambda表达式的一些常见写法。  


## 1.替代匿名内部类
毫无疑问，lambda表达式用得最多的场合就是替代匿名内部类，而实现Runnable接口是匿名内部类的经典例子。lambda表达式的功能相当强大，用()->就可以代替整个匿名内部类！请看代码：  

如果使用匿名内部类：
```
    @Test
    public void oldRunable() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("The old runable now is using!");
            }
        }).start();
    }
```  

而如果使用lambda表达式：  

```
    @Test
    public void runable() {
        new Thread(() -> System.out.println("It's a lambda function!")).start();
    }
```  

最后的输出：  

```
The old runable now is using!
It's a lambda function!
```  

是不是强大到可怕？是不是简单到可怕？是不是清晰明了重点突出到可怕？这就是lambda表达式的可怕之处，用极少的代码完成了之前一个类做的事情！  

## 2.使用lambda表达式对集合进行迭代
Java的集合类是日常开发中经常用到的，甚至说没有哪个java代码中没有使用到集合类。。。而对集合类最常见的操作就是进行迭代遍历了。请看对比：  


```
    @Test
    public void iterTest() {
        List<String> languages = Arrays.asList("java","scala","python");
        //before java8
        for(String each:languages) {
            System.out.println(each);
        }
        //after java8
        languages.forEach(x -> System.out.println(x));
        languages.forEach(System.out::println);
    }
```  

如果熟悉scala的同学，肯定对forEach不陌生。它可以迭代集合中所有的对象，并且将lambda表达式带入其中。  

```
languages.forEach(System.out::println);
```  

这一行看起来有点像c++里面作用域解析的写法，在这里也是可以的。  

## 3.用lambda表达式实现map
一提到函数式编程，一提到lambda表达式，怎么能不提map。。。没错，java8肯定也是支持的。请看示例代码：  

```
    @Test
    public void mapTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0);
        cost.stream().map(x -> x + x*0.05).forEach(x -> System.out.println(x));
    }
```  

最后的输出结果：  

```
10.5
21.0
31.5
```  

map函数可以说是函数式编程里最重要的一个方法了。map的作用是将一个对象变换为另外一个。在我们的例子中，就是通过map方法将cost增加了0,05倍的大小然后输出。  

## 4.用lambda表达式实现map与reduce
既然提到了map，又怎能不提到reduce。reduce与map一样，也是函数式编程里最重要的几个方法之一。。。map的作用是将一个对象变为另外一个，而reduce实现的则是将所有值合并为一个，请看：  


```
    @Test
    public void mapReduceTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0);
        double allCost = cost.stream().map(x -> x+x*0.05).reduce((sum,x) -> sum + x).get();
        System.out.println(allCost);
    }
```  

最终的结果为：  

```
63.0
```  

如果我们用for循环来做这件事情：  

```
    @Test
    public void sumTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0);
        double sum = 0;
        for(double each:cost) {
            each += each * 0.05;
            sum += each;
        }
        System.out.println(sum);
    }
```  

相信用map+reduce+lambda表达式的写法高出不止一个level。  

## 5.filter操作
filter也是我们经常使用的一个操作。在操作集合的时候，经常需要从原始的集合中过滤掉一部分元素。  

```
    @Test
    public void filterTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0,40.0);
        List<Double> filteredCost = cost.stream().filter(x -> x > 25.0).collect(Collectors.toList());
        filteredCost.forEach(x -> System.out.println(x));

    }
```  

最后的结果：  

```
30.0
40.0
```  

将java写出了python或者scala的感觉有没有！是不是帅到爆！  

## 6.与函数式接口Predicate配合
除了在语言层面支持函数式编程风格，Java 8也添加了一个包，叫做 java.util.function。它包含了很多类，用来支持Java的函数式编程。其中一个便是Predicate，使用 java.util.function.Predicate 函数式接口以及lambda表达式，可以向API方法添加逻辑，用更少的代码支持更多的动态行为。Predicate接口非常适用于做过滤。  

```
    public static void filterTest(List<String> languages, Predicate<String> condition) {
        languages.stream().filter(x -> condition.test(x)).forEach(x -> System.out.println(x + " "));
    }

    public static void main(String[] args) {
        List<String> languages = Arrays.asList("Java","Python","scala","Shell","R");
        System.out.println("Language starts with J: ");
        filterTest(languages,x -> x.startsWith("J"));
        System.out.println("\nLanguage ends with a: ");
        filterTest(languages,x -> x.endsWith("a"));
        System.out.println("\nAll languages: ");
        filterTest(languages,x -> true);
        System.out.println("\nNo languages: ");
        filterTest(languages,x -> false);
        System.out.println("\nLanguage length bigger three: ");
        filterTest(languages,x -> x.length() > 4);
    }
```  

最后的输出结果：  

```
Language starts with J: 
Java 

Language ends with a: 
Java 
scala 

All languages: 
Java 
Python 
scala 
Shell 
R 

No languages: 

Language length bigger three: 
Python 
scala 
Shell 

```  

可以看到，Stream API的过滤方法也接受一个Predicate，这意味着可以将我们定制的 filter() 方法替换成写在里面的内联代码，这也是lambda表达式的魔力！  

参考文档：  
1.http://www.importnew.com/16436.html  