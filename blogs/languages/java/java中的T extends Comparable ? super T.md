<T extends Comparable<? super T>> 这样的类型参数 (Type Parameter) 在 JDK 中或工具类方法中经常能看到。例如在Collections中的sort方法：  

```
    public static <T extends Comparable<? super T>> void sort(List<T> list) {
        list.sort(null);
    }
```  

很多人第一眼看到这个函数签名，都会有些疑惑，干嘛搞这么麻烦，这么声明不就好了么  

```
<T extends Comparable<T>>
```  

为什么非要声明成这么复杂的形式  

```
<T extends Comparable<? super T>>
```  

经过一番看书，搜索，搞明白了这样声明的目的。  

## 1.<T extends Comparable<T>> 和 <T extends Comparable<? super T>>的简单区别
```
<T extends Comparable<T>>
```  
类型 T 必须实现 Comparable 接口，并且这个接口的类型是 T。  

```
<T extends Comparable<? super T>>
```  
类型 T 必须实现 Comparable 接口，并且这个接口的类型是 T 或 T 的任一父类。这样声明后，T 的实例之间，T 的实例和它的父类的实例之间，可以相互比较大小。  


## 2.示例１
看一个很多地方都能找到的例子  

```
public class Test1 {

    public static void main(String[] args) {
        Demo<GregorianCalendar> p1 = null; // 报错会
    }

}

class Demo<T extends Comparable<T>> {}
```  

上述代码在IDE中会报错：  
Error:(11, 14) java: 类型参数java.util.GregorianCalendar不在类型变量T的范围内。  

为什么会报上面的错误呢？因为GregorianCalendar并没有实现Comparable接口。  
如果将上面的代码稍作修改，就能正常运行：  

```
public class Test1 {

    public static void main(String[] args) {
        Demo<GregorianCalendar> p1 = null;
    }
}

class Demo<T extends Comparable<? super T>> {}
```  

为什么现在没有问题？因为GregorianCalendar继承了Calendar类，而Calendar实现了Comparable接口。  

通过上面的例子，很明显能看出来： <T extends Comparable<? super T>>这种声明的方式，不仅可以接受T类型，还可以接受T的父类型，这样类型参数对所传入的参数限制更少，提高了 API 的灵活性。  

## 3.示例2
看另外一个例子  

```
public class Test2 {

    public static <T extends Comparable<T>> void sort1(List<T> list) {
        Collections.sort(list);
    }

    public static <T extends Comparable<? super T>> void sort2(List<T> list) {
        Collections.sort(list);
    }


    public static void t1() {
        List<Animal> animals = new ArrayList<Animal>();
        animals.add(new Animal(20));
        animals.add(new Animal(30));

        List<Dog> dogs = new ArrayList<Dog>();
        dogs.add(new Dog(5));
        dogs.add(new Dog(10));

        sort1(animals);
        // sort1(dogs); 会报错

        sort2(animals);
        sort2(dogs);
    }
}


class Animal implements Comparable<Animal> {
    public int age;

    public Animal(int age) {
        this.age = age;
    }

    public int compareTo(Animal other) {
        return this.age - other.age;
    }
}

class Dog extends Animal {

    public Dog(int age) {
        super(age);
    }
}

```  

上面的例子有两个类：Animal类实现了Comparable接口，Dog继承了Animal类。sort1方法的参数为`<T extends Comparable<T>>` ，sort2方法的参数为`<T extends Comparable<? super T>>`。  

sort1方法只能对`List<Animal>`类型的list进行排序，对于`List<Dog>`类型不能排序。  
sort2方法因为方法签名的参数为`<T extends Comparable<? super T>>`，所以不管是`List<Animal>`类型还是`List<Dog>`类型，都可以！  