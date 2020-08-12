java中实例化Class类对象的三种方式:  
第一种、通过forName();  
第二种、类.class  
第三种、对象.getClass()  

测试案例：  

```
package com.lfl.demo;

public class GetClassDemo1 {
 public static void main(String[] args) {
  Class<?> c1 = null;// ?是泛型中的通配符
  Class<?> c2 = null;// ?是泛型中的通配符
  Class<?> c3 = null;// ?是泛型中的通配符
  try {
   c1 = Class.forName("com.lfl.demo.Test");// 此方式在开发中较为常用
  } catch (ClassNotFoundException e) {
   e.printStackTrace();
  }
    c2 = Test.class;// 通过类.class实例化
    c3 = new Test().getClass();// 通过Object类中的方法实例化
    System.out.println("类名称：" +c1.getName());
    System.out.println("类名称：" +c2.getName());
    System.out.println("类名称：" +c3.getName());
 }
}

class Test {
};
```  

Class类是什么？  
==每个类被加载后，系统会为该类生成一个对应的Class对象，通过该Class对象就可以访问到JVM中的这个类。  
==Java程序中的各个java类属于同一个事物，描述这类事物的java类名就是Class。  
Class类描述了类的名字，类的访问属性，类所属的包名，字段名称的列表，方法名称的列表等等。  
创建Class类的实例，其实例为类被加载后的字节码。  

