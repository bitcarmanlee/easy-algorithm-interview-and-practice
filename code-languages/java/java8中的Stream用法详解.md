## 1.为什么java8中加入Stream
Stream 作为 Java 8 的一大亮点，它与 java.io 包里的 InputStream 和 OutputStream 是完全不同的概念。Java 8 中的 Stream 是对集合（Collection）对象功能的增强，它专注于对集合对象进行各种非常便利、高效的聚合操作（aggregate operation），或者大批量数据操作 (bulk data operation)。尤其是对于数据从业人员来说，对数据做各种操作转换是再正常不过的需求，基本每天都会用到。例如下面这么一个简单的小需求：求一个集合中字符串长度小于5的数量。  
在java8之前，我们一般这么做：  

```
    @Test
    public void lenIter() {
        List<String> list = Arrays.asList("java", "scala", "python", "shell", "ruby");
        int num = 0;
        for(String lan: list) {
            if(lan.length() < 5) {
                num++;
            }
        }
        System.out.println(num);
    }
```  

这段代码逻辑很简单，但是显得很冗长，可读性嘛也就呵呵了。如果用Stream，我们可以这样：  

```
    @Test
    public void lenStream() {
        List<String> list = Arrays.asList("java", "scala", "python", "shell", "ruby");
        long num = list.parallelStream().filter(x -> x.length() < 5).count();
        System.out.println(num);
    }
```  

代码量明显减少而且逻辑特别清楚，即使不懂代码的人看到也能猜出来是什么意思。如果大家了解过函数式编程，就会觉得特别亲切自然。  

## 2.什么是Stream
Stream 不是集合元素，它不是数据结构并不保存数据，它是有关算法和计算的，它更像一个高级版本的 Iterator。原始版本的 Iterator，用户只能显式地一个一个遍历元素并对其执行某些操作；高级版本的 Stream，用户只要给出需要对其包含的元素执行什么操作，比如 “过滤掉长度大于 10 的字符串”、“获取每个字符串的首字母”等，Stream 会隐式地在内部进行遍历，做出相应的数据转换。  
Stream 就如同一个迭代器（Iterator），单向，不可往复，数据只能遍历一次，遍历过一次后即用尽了，就好比流水从面前流过，一去不复返。  
而和迭代器又不同的是，Stream 可以并行化操作，迭代器只能命令式地、串行化操作。顾名思义，当使用串行方式去遍历时，每个 item 读完后再读下一个 item。而使用并行去遍历时，数据会被分成多个段，其中每一个都在不同的线程中处理，然后将结果一起输出。Stream 的并行操作依赖于 Java7 中引入的 Fork/Join 框架（JSR166y）来拆分任务和加速处理过程。  

Stream和Collection的区别主要有：  
1.stream本身并不存储数据，数据是存储在对应的collection里，或者在需要的时候才生成的；  
2.stream不会修改数据源，总是返回新的stream；  
3.stream的操作是懒执行(lazy)的：仅当最终的结果需要的时候才会执行，比如上面的例子中，结果仅需要前3个长度大于7的字符串，那么在找到前3个长度符合要求的字符串后，filter()将停止执行；  

使用stream的步骤如下：  
1.创建stream；  
2.通过一个或多个中间操作(intermediate operations)将初始stream转换为另一个stream；  
3.通过中止操作(terminal operation)获取结果；该操作触发之前的懒操作的执行，中止操作后，该stream关闭，不能再使用了；  

## 3.创建Stream的方法
最常用的为使用静态方法创建  

```
    @Test
    public void numberStreamConstruct() {
        IntStream.of(new int[] {1, 2, 3}).forEach(System.out::println);
        IntStream.range(1, 3).forEach(System.out::println);
        IntStream.rangeClosed(1, 3).forEach(System.out::println);
    }
```  

## 4.Stream的转换
Stream最大的用途就是各种转换了。跟Spark中的Rdd类似，Rdd里面也是各种transfer操作。  
1.filter操作。即使原stream中满足条件的元素构成新的stream：  

```
    @Test
    public void lenStream() {
        List<String> list = Arrays.asList("java", "scala", "python", "shell", "ruby");
        long num = list.parallelStream().filter(x -> x.length() < 5).count();
        System.out.println(num);
    }
```  

结果：  

```
2
```  

得到长度小于5的单词个数  

2.map操作。map算是最常用的一种操作了，遍历原stream中的元素，转换后构成新的stream：  

```
    @Test
    public void turnUpperCase() {
        List<String> list = Arrays.asList(new String[] {"a", "b", "c"});
        List<String> result = list.stream().map(String::toUpperCase).collect(Collectors.toList());
        result.forEach(x -> System.out.print(x + " "));
    }
```  

3.distinct操作。distinct也是常用的操作之一。  

```
    @Test
    public void distinctStream() {
        Stream<String> distinctStream = Stream.of("bj","shanghai","tianjin","bj","shanghai").distinct();
        Stream<String> sortedStream = distinctStream.sorted(Comparator.comparing(String::length));
        sortedStream.forEach(x -> System.out.print(x + " "));
    }
```  

结果如下  

```
bj tianjin shanghai 
```  

4.排序操作。  

```
    @Test
    public void sortStream() {
        Stream<Integer> sortedStream = Stream.of(1,3,7,4,5,8,6,2).sorted();
        sortedStream.collect(Collectors.toList()).forEach(x -> System.out.print(x + " "));
        System.out.println();

        Stream<Integer> sortedReverseStream = Stream.of(1,3,7,4,5,8,6,2).sorted(new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o1 - o2;
            }
        });
        Stream<Integer> sortedReverseStreamV2 = Stream.of(1,3,7,4,5,8,6,2).sorted((Integer o1, Integer o2) -> o2 - o1);
        sortedReverseStreamV2.collect(Collectors.toList()).forEach(x -> System.out.print(x + " "));
    }
```  

最终的结果：  

```
1 2 3 4 5 6 7 8 
8 7 6 5 4 3 2 1 
```  

## 5.reduction操作
1.reduction就是从stream中取出结果，是terminal operation，因此经过reduction后的stream不能再使用了。主要包含以下操作： findFirst()/findAny()/allMatch/anyMatch()/noneMatch等等  

```

    @Test
    public void reductionStream() {
        Stream<String> wordList = Stream.of("bj","tj","sh","yy","yq").distinct();
        Optional<String> firstWord = wordList.filter(word -> word.startsWith("y")).findFirst();
        System.out.println(firstWord.orElse("unknown"));
    }
```  

结果：  

```
yy
```  

2. reduce方法。与其他语言里的reduce方法一样的逻辑。  

```
    @Test
    public void reduceTest() {
        Stream<Integer> list = Stream.of(1,2,3,4,5);
        Optional<Integer> result = list.reduce((x, y) -> x + y);
        System.out.println(result);
    }
```  
结果如下：  

```
Optional[15]
```  

## 6.collect
collect()方法可以对stream中的元素进行各种处理后，得到stream中元素的值。并且Collectors接口提供了很方便的创建Collector对象的工厂方法。  

```
    @Test
    public void collectTest() {
        List<String> list = Stream.of("hello", "world", "hello", "java").collect(Collectors.toList());
        list.forEach(x -> System.out.print(x + " "));
        System.out.println();
        Set<String> set = Stream.of("hello", "world", "hello", "java").collect(Collectors.toSet());
        set.forEach(x -> System.out.print(x + " "));
        System.out.println();
        Set<String> treeset = Stream.of("hello", "world", "hello", "java").collect(Collectors.toCollection(TreeSet::new));
        treeset.forEach(x -> System.out.print(x + " "));
        System.out.println();
        String resultStr = Stream.of("hello", "world", "hello", "java").collect(Collectors.joining(","));
        System.out.println(resultStr);
    }
```  

最后的输出结果为：  

```
hello world hello java 
world java hello 
hello java world 
hello,world,hello,java
```  