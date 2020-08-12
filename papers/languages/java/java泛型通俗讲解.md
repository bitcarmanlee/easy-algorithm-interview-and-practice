## 1.为什么需要泛型
我们知道java是属于强类型编程语言。变量在使用之前，需要先进行定义，而定义个变量时必须要指定其数据类型，这样编译器在编译阶段就能将很多类型错误消灭在萌芽状态。  

如果我们有这样一个需求：定义一个坐标类。但是该坐标类的数据类型可能是整数，也可以能是小数，还有可能是字符串。举个例子  
```
x=10; y=15;
x="东经116",y="北纬39"
x=10.01; y=15
```  

坐标有可能是整型，也有可能是字符串类型，还有可能是double类型。如果没有泛型，我们可能会这么做  

```
package edu.bit.test;

public class ObjectType {

    public static void main(String[] args) {
        Point p = new Point();
        p.setX(10);
        p.setY(15);

        //向下转型,此时没有问题,代码能正常运行
        int x = (Integer)p.getX();
        int y = (Integer)p.getY();
        System.out.println(p);

        p.setX("东经116");
        p.setY("北纬39");

        //此时向下转型会有问题
        double x1 = (Double)p.getX();
        double y1 = (Double)p.getY();
        System.out.println(p);
    }
}

class Point {
    Object x = 0;
    Object y = 0;

    public Object getX() {
        return x;
    }

    public void setX(Object x) {
        this.x = x;
    }

    public Object getY() {
        return y;
    }

    public void setY(Object y) {
        this.y = y;
    }

    @Override
    public String toString() {
        return "Point{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}
```  

将代码run起来  

```
Point{x=10, y=15}
Exception in thread "main" java.lang.ClassCastException: java.lang.String cannot be cast to java.lang.Double
	at edu.bit.test.ObjectType.main(ObjectType.java:22)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:497)
	at com.intellij.rt.execution.application.AppMain.main(AppMain.java:147)

Process finished with exit code 1
```  

在上面的示例代码中，用的是Object类型。这样，在调用set方法的时候是没有问题的。但是在使用get方法时，因为需要将Object类向下转型成其他类，这样容易带来问题。并且，这种问题在jdk编译阶段还不容易被发现，往往只有在运行的时候才会抛出异常！像我们上面的代码，在IDE中是不会报错的，但是代码run起来以后，会抛出一个ClassCastException的异常！  

## 2.泛型的使用方式
将上面的代码改用泛型的方式实现  

```
package edu.bit.test;

public class GenericType {

    public static void main(String[] args) {
        Point1<Integer,Integer> p1 = new Point1<Integer, Integer>();
        p1.setX(10);
        p1.setY(15);
        System.out.println(p1);

        Point1<String,String> p2 = new Point1<String,String>();
        p2.setX("东经116");
        p2.setY("北纬39");
        System.out.println(p2);
    }

}

class Point1<T1,T2> {
    T1 x;
    T2 y;

    public T1 getX() {
        return x;
    }

    public void setX(T1 x) {
        this.x = x;
    }

    public T2 getY() {
        return y;
    }

    public void setY(T2 y) {
        this.y = y;
    }

    @Override
    public String toString() {
        return "Point1{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}
```  

将代码run起来  

```
Point1{x=10, y=15}
Point1{x=东经116, y=北纬39}
```  

在上面的例子里，直接将Point1类定义为泛型类。泛型类的定义方法为类名后面用尖括号将<T1,T2>包起来，其中的T1,T2是我们自己定义的类标志符，用来表示数据的类型。并且注意的是，T1,T2只是类型标识的占位符，编译阶段并不会真正确定类型，只有在运行阶段才会替换为真正的数据类型。  

使用泛型的好处是：当我们在是使用泛型的时候，即指定了数据类型，又可以根据需要灵活使用不同数据类型，在使用严谨性与灵活性之间做了一个很好的兼顾。尤其是在各种框架中，泛型的使用非常广泛。  

## 3.限制泛型的使用类型
在我们上面的代码中，没有对参数类型做任何限制，可以使用任何类型的参数。然后在很多实际场景中，还是需要对参数类型做一定限制的，只能传递部分参数类型，传递其他类型则会引发错误。例如在前面的Point类中，我们希望用户只能传递数字类型，而不能传递字符串等其他类型：  

```
package edu.bit.test;

public class GenericSmallType {

    public static void main(String[] args) {
        Point2<Integer,Integer> p1 = new Point2<Integer,Integer>();
        p1.setX(10);
        p1.setY(15);
        System.out.println(p1);

        Point2<Double,Double> p2 = new Point2<Double,Double>();
        p2.setX(10.0);
        p2.setY(15.01);
        System.out.println(p2);
    }
}

class Point2<T1 extends Number,T2 extends Number> {
    public T1 x;
    public T2 y;

    public T1 getX() {
        return x;
    }

    public void setX(T1 x) {
        this.x = x;
    }

    public T2 getY() {
        return y;
    }

    public void setY(T2 y) {
        this.y = y;
    }

    @Override
    public String toString() {
        return "Point2{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}
```  

将代码run起来：  

```
Point2{x=10, y=15}
Point2{x=10.0, y=15.01}
```  

## 4.类型擦除(type erasure)
java字节码中不包含有泛型的类型信息。编译器在编译阶段去掉泛型信息，在运行的时候加上类型信息，这个过程被称为类型擦除。  
我们在使用泛型的过程中，如果没有指定数据类型，那么将会擦除泛型类型。  

```
package edu.bit.test;

public class TypeErasure {

    public static void main(String[] args) {
        Point3 p1 = new Point3();

        p1.setX("东经116");
        p1.setY("北纬39");

        //向下转型
        String longitude = (String)p1.getX();
        String latitude = (String)p1.getY();

        System.out.println(p1);
    }
}

class Point3<T1,T2> {
    public T1 x;
    public T2 y;

    public T1 getX() {
        return x;
    }

    public void setX(T1 x) {
        this.x = x;
    }

    public T2 getY() {
        return y;
    }

    public void setY(T2 y) {
        this.y = y;
    }

    @Override
    public String toString() {
        return "Point3{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}

```  

本例中，创建Point3对象的时候没有指定数据类型。编译器在处理的时候，会将所有数据向上变为Object类型。然而这样处理完以后，使用get方法的时候，又需要向下转型。这样的话，跟第一部分没有使用泛型就一样了！  