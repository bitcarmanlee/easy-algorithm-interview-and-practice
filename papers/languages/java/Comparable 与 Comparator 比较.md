## 1.两个接口的原型

Java中，Comparable与Comparator接口都是用来做比较的。那么这两个接口在实际使用中到底有什么不同呢？下面我们来结合实例分析一下。  

先看看两个接口在JDK中的原型。  

```
package java.lang;
import java.util.*;

public interface Comparable<T> {
    public int compareTo(T o);
}
```

```
package java.util;

import java.io.Serializable;
import java.util.function.Function;
import java.util.function.ToIntFunction;
import java.util.function.ToLongFunction;
import java.util.function.ToDoubleFunction;
import java.util.Comparators;

@FunctionalInterface
public interface Comparator<T> {
    int compare(T o1, T o2);
    boolean equals(Object obj);
}
```  

## 2.Comparable的用法
一般来说，Comparable是为了对某个类的集合进行排序，所以此时一般都是这个需要排序的类本身去实现Comparable接口。换句话说，如果某个类实现了Comparable接口，那么这个类的数组或者说List就可以进行排序了。  

举个简单的例子：  

```
public class Employee implements Comparable<Employee> {

    private String name;
    private int salary;

    public Employee(String name, int salary) {
        this.name = name;
        this.salary = salary;
    }

    @Override
    public int compareTo(Employee other) {
        return this.salary - other.salary;
    }

    @Override
    public String toString() {
        return "name is: " + name + ", salary is: " + salary;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getSalary() {
        return salary;
    }

    public void setSalary(int salary) {
        this.salary = salary;
    }
}
```  

在客户端中实现Employee集合排序：  

```
public class CompareTest {

    public static List<Employee> genList() {
        Employee e1 = new Employee("aaa",100);
        Employee e2 = new Employee("bbb",150);
        Employee e3 = new Employee("ccc", 80);
        List<Employee> list = new ArrayList();

        list.add(e1);
        list.add(e2);
        list.add(e3);

        return list;
    }

    public static void t1() {
        List<Employee> list = genList();
        //Collections.sort(list); 两种方式都可以，此种方式源码中就是调用的list.sort(null)
        list.sort(null);
        System.out.println(list);
    }
    
    public static void main(String[] args) {
        t1();
    }

}
```  

将客户端的代码run起来，最后输出的结果为：  

```
[name is: ccc, salary is: 80, name is: aaa, salary is: 100, name is: bbb, salary is: 150]
```  

因为Employee实现了Comparable接口，所以能直接对Employee数组进行排序。  

## 3.Comparator接口用法
很多时候我们无法对类进行修改，或者说此类修改的成本太高，但是又希望对其进行排序。那怎么办？这个时候Comparator接口就排上了用场。  
比如我们将前面的Employee类稍作修改，不实现Comparable接口，加上final关键字：  

```
public final class Employee  {

    private String name;
    private int salary;

    public Employee(String name, int salary) {
        this.name = name;
        this.salary = salary;
    }

    @Override
    public String toString() {
        return "name is: " + name + ", salary is: " + salary;
    }
    ...此处省略get/set
}
```  

这个时候我们显然无法修改Employee类了。但是还是需要对其排序，怎么办？  

如果在jdk8之前，使用匿名内部类的方式：  

```
    public static void test() {
        List<Employee> list = genList();
        Collections.sort(list, new Comparator<Employee>() {
            @Override
            public int compare(Employee o1, Employee o2) {
                return o1.getSalary() - o2.getSalary();
            }
        });
        System.out.println(list);
    }
```  

在jdk8之后，可以使用lambda表达式：  

```
    public static void test() {
        List<Employee> list = genList();
        Comparator<Employee> comparator = (Employee e1, Employee e2) -> e1.getSalary() - e2.getSalary();
        list.sort(comparator);
        System.out.println(list);
    }
```  

如果将此方法run起来，输出如下：  

```
[name is: ccc, salary is: 80, name is: aaa, salary is: 100, name is: bbb, salary is: 150]
```  

同学们可能会注意到，Comparable接口中只有一个compareTo方法要实现，而Comparator有两个方法，但是我们只实现了一个方法，那么另外一个方法呢？  

其实很简单，因为另外一个方法是equals方法。所有的类都继承了Object类，而Object类中实现了equals方法，所以我们这里不实现equals方法也无所谓！  


## 4.Comparator中的各种实现方式比较

Comparator中的compare方法实现方式还是比较多的。下面我们来一一说明。  

### 4.1 传统的匿名内部类
JDK8之前，一般是采用匿名内部类的方式实现：  

```
        Collections.sort(list, new Comparator<Employee>() {
            @Override
            public int compare(Employee o1, Employee o2) {
                return o1.getSalary() - o2.getSalary();
            }
        });
```  

### 4.2 lambda表达式
JDK8之后，可以使用lambda表达式：  

```
list.sort((Employee e1, Employee e2) -> e1.getSalary() - e2.getSalary());
```  

### 4.3 精简版的lambda表达式
我们通过不指定类型定义来进一步简化表达式，因为编译器自己可以进行类型判断  

```
list.sort((e1, e2) -> e1.getSalary() - e2.getSalary());
```  

### 4.4 使用Comparator.comparing的方式
我们使用上述lambda表达式的时候，IDE会提示我们：can be replaced with comparator.comparing Int  

```
list.sort(Comparator.comparing(employee -> employee.getSalary()));
```  

### 4.5 使用静态方法的引用
java中的双冒号就是方法引用。::是JDK8里引入lambda后的一种用法，表示引用，比如静态方法的引用String::valueOf，比如构造器的引用，ArrayList::new。  


```
list.sort(Comparator.comparing(Employee::getSalary));
```  

### 4.6 排序反转
很多时候，想对排序进行反转，或者说逆序：  

```
list.sort(Comparator.comparing(Employee::getSalary).reversed());
```  

### 4.7 许多条件组合排序

```
        list.sort((e1, e2) -> {
            if(e1.getSalary() != e2.getSalary()) {
                return e1.getSalary() - e2.getSalary();
            } else {
                return e1.getName().compareTo(e2.getName());
            }
        });
```  

### 4.8 从JDK 8开始，我们现在可以把多个Comparator链在一起（chain together）去建造更复杂的比较逻辑

```
list.sort(Comparator.comparing(Employee::getSalary).thenComparing(Employee::getName));
```  
