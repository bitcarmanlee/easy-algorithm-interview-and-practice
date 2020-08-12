## 1.枚举类 (enum)
1.在某些情况下，一个类的对象时有限且固定的，如季节类，它只有春夏秋冬4个对象这种实例有限且固定的类，在 Java 中被称为枚举类；  
2.在 Java 中使用 enum 关键字来定义枚举类，其地位与 class、interface 相同；  
3.枚举类是一种特殊的类，它和普通的类一样，有自己的成员变量、成员方法、构造器 (只能使用 private 访问修饰符，所以无法从外部调用构造器，构造器只在构造枚举值时被调用)；  
4.一个 Java 源文件中最多只能有一个 public 类型的枚举类，且该 Java 源文件的名字也必须和该枚举类的类名相同，这点和类是相同的；  
5.使用 enum 定义的枚举类默认继承了 java.lang.Enum 类，并实现了 java.lang.Seriablizable 和 java.lang.Comparable 两个接口;  
6.所有的枚举值都是 public static final 的，且非抽象的枚举类不能再派生子类；  
7.枚举类的所有实例(枚举值)必须在枚举类的第一行显式地列出，否则这个枚举类将永远不能产生实例。列出这些实例(枚举值)时，系统会自动添加 public static final 修饰，无需程序员显式添加。  

## 2.枚举类的使用

### 定义枚举类

```
// 定义一个星期的枚举类
public enum WeekEnum {
    // 在第一行显式地列出7个枚举实例(枚举值)，系统会自动添加 public static final 修饰
    SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY;
}
```  

### 枚举类的成员变量、成员方法、构造器

```
package enumtest;

public enum WeekEnum {

    // 因为已经定义了带参数的构造器，所以在列出枚举值时必须传入对应的参数
    SUNDAY("星期日"), MONDAY("星期一"), TUESDAY("星期二"), WEDNESDAY("星期三"), 
    THURSDAY("星期四"), FRIDAY("星期五"), SATURDAY("星期六");

    // 定义一个 private 修饰的实例变量
    private String date;

    // 定义一个带参数的构造器，枚举类的构造器只能使用 private 修饰
    private WeekEnum(String date) {
        this.date = date;
    }

    // 定义 get set 方法
    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

}
```  

### 枚举类中的常用方法
1.int compareTo(E o)： 该方法用于与制定枚举对象比较顺序，同一个枚举实例只能与相同类型的枚举实例比较。如果该枚举对象位于指定枚举对象之后，则返回正整数；反之返回负整数；否则返回零；  

```
public class Test01 {    
 public static void main(String[] args) {
     System.out.println(WeekEnum.FRIDAY.compareTo(WeekEnum.MONDAY));
     System.out.println(WeekEnum.FRIDAY.compareTo(WeekEnum.SUNDAY));
     System.out.println(WeekEnum.FRIDAY.compareTo(WeekEnum.SATURDAY));
 }
}
```  

运行结果：  
4  
5  
-1  

2.String name()： 返回此枚举实例的名称，即枚举值 ；  

3.static values()： 返回一个包含全部枚举值的数组，可以用来遍历所有枚举值；  

```
// 没有重写 toString 方法
for (WeekEnum we : WeekEnum.values()) {
         System.out.println(we);
     }
```  

运行结果：  
SUNDAY  
MONDAY  
TUESDAY  
WEDNESDAY  
THURSDAY  
FRIDAY  
SATURDAY  

4.String toString()： 返回枚举值的名称，与 name 方法类似，更常用；  

```
// 定义一个星期的枚举类
public enum WeekEnum {

 // 因为已经定义了带参数的构造器，所以在列出枚举值时必须传入对应的参数
 SUNDAY("星期日"), MONDAY("星期一"), TUESDAY("星期二"), WEDNESDAY("星期三"), 
 THURSDAY("星期四"), FRIDAY("星期五"), SATURDAY("星期六");

 // 定义一个 private 修饰的实例变量
 private String date;

 // 定义一个带参数的构造器，枚举类的构造器只能使用 private 修饰
 private WeekEnum(String date) {
     this.date = date;
 }

 // 定义 get set 方法
 public String getDate() {
     return date;
 }

 public void setDate(String date) {
     this.date = date;
 }

 // 重写 toString() 方法
 @Override
 public String toString(){
     return date;
 }
}
```  

```
// 重写了 toString 方法
for (WeekEnum we : WeekEnum.values()) {
         System.out.println(we);
     }
```  

运行结果：  
星期日  
星期一  
星期二  
星期三  
星期四  
星期五  
星期六  

结合上面3.4点，可以看到，重写 toString 方法前后所返回的枚举值不同！  

5.int ordinal()： 返回枚举值在枚举类中的索引值(从0开始)，即枚举值在枚举声明中的顺序，这个顺序根据枚举值声明的顺序而定；  

```
System.out.println(WeekEnum.SUNDAY.ordinal());
System.out.println(WeekEnum.FRIDAY.ordinal());
```  

运行结果：  
0  
5  

6.static valueOf()： 返回带指定名称的指定枚举类型的枚举常量，名称必须与在此类型中声明枚举常量所用的标识符完全匹配(不允许使用额外的空白字符)。这个方法与toString相对应，因此重写 toString() 方法，一定要重写 valueOf() 方法(我们可以重写 toString() 方法，但不能自己重写 valueOf() 方法，当我们重写 toString() 方法时，valueOf() 方法会自动重写，不用我们理会。)；  

```
public class Test01 {
 public static void main(String[] args) {
     System.out.println(WeekEnum.valueOf(WeekEnum.class, "MONDAY"));
     System.out.println(WeekEnum.valueOf(WeekEnum.class, "FRIDAY"));
     System.out.println(WeekEnum.valueOf(WeekEnum.class, "SUNDAY"));
 }
}
```  

运行结果：  
MONDAY  
FRIDAY  
SUNDAY  

7.boolean equals()方法： 比较两个枚举类对象的引用。  

使用枚举类实现接口  
与普通类一样，枚举类也可以实现一个或多个接口。枚举类实现接口时，同样要实现  
该接口的所有方法。  

```
public interface GenderDescription {

    public void info();

}
```  

上面定义了一个接口，该接口有一个 info() 方法，凡是实现该接口的类都需要实现该方法。    

```
public enum Gender implements GenderDescription {

    MALE,FEMALE;

    @Override
    public void info() {
        System.out.println("这是一个用于定义性别的枚举类");
    }

}
```  

```
public class Test02 {

    public static void main(String[] args) {
        Gender.MALE.info();
        Gender.FEMALE.info();
    }

}
```  

运行结果：  
这是一个用于定义性别的枚举类  
这是一个用于定义性别的枚举类  

## 3.包含抽象方法的枚举类
定义一个 Operation 枚举类，有4个枚举值PLUS、MINUS、TIMES、DIVIDE，分别代表加、减、乘、除，该枚举类有一个 calculate() 方法，用于完成计算。  

```
public enum Operation {

    // 用于执行加法运算
    PLUS { // 花括号部分其实是一个匿名内部子类

        @Override
        public double calculate(double x, double y) {
            return x + y;
        }

    },

    // 用于执行减法运算
    MINUS { // 花括号部分其实是一个匿名内部子类

        @Override
        public double calculate(double x, double y) {
            // TODO Auto-generated method stub
            return x - y;
        }

    },

    // 用于执行乘法运算
    TIMES { // 花括号部分其实是一个匿名内部子类

        @Override
        public double calculate(double x, double y) {
            return x * y;
        }

    },

    // 用于执行除法运算
    DIVIDE { // 花括号部分其实是一个匿名内部子类

        @Override
        public double calculate(double x, double y) {
            return x / y;
        }

    };

    //为该枚举类定义一个抽象方法，枚举类中所有的枚举值都必须实现这个方法
    public abstract double calculate(double x, double y);

}
```  

```
public class Test03 {

    public static void main(String[] args) {
        System.out.println("6 + 2 = " + Operation.PLUS.calculate(6, 3));
        System.out.println("6 - 2 = " + Operation.MINUS.calculate(6, 2));
        System.out.println("6 * 2 = " + Operation.TIMES.calculate(6, 2));
        System.out.println("6 / 2 = " + Operation.DIVIDE.calculate(6, 2));
    }

}
```  
运行结果：  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/enum/1.png)  


原文链接地址：  
http://www.jianshu.com/p/46dbd930f6a2  