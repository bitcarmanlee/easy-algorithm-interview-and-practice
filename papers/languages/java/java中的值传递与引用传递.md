在java中，如果参数类型是原始类型，那么传过来的就是这个参数的一个副本，也就是这个原始参数的值，如果在函数中改变了副本的 值不会改变原始的值。  

如果参数类型是引用类型，那么传过来的就是这个引用参数的副本，这个副本存放的是参数的地址。如果在函数中没有改变这个副本的地址，而是改变了地址中的 值，那么在函数内的改变会影响到传入的参数。如果在函数中改变了副本的地址，如new一个，那么副本就指向了一个新的地址，此时传入的参数还是指向原来的 地址，所以不会改变参数的值。  

传递值的数据类型：八种基本数据类型和String(这样理解可以，但是事实上String也是传递的地址,只是string对象和其他对 象是不同的，string对象是不能被改变的，内容改变就会产生新对象。那么StringBuffer就可以了，但只是改变其内容。不能改变外部变量所指 向的内存地址)。  

传递地址值的数据类型：除String以外的所有复合数据类型，包括数组、类和接口  

为了对上面参数传递有更清楚的认识，可以参考如下的测试代码：  

```
public class ParamTransferTest {

    public static void swapnum(int a, int b) {
        int tmp = a;
        a = b;
        b = tmp;
    }

    public static class Person {
        public String name;
        public int age;
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }

        public void changeattr(Person p, String name, int age) {
            p.name = name;
            p.age = age;
        }

        public void printp() {
            System.out.println(this.name + ", " + this.age);
        }

    }

    public static void main(String[] args) {
        int a = 1, b = 2;
        System.out.println("before swap, a is: " + a + ", b is: " + b);
        swapnum(a, b);
        System.out.println("after swap, a is: " + a + ", b is: " + b);

        Person p = new Person("zhangsan", 15);
        System.out.println("\nbefore change, person is: ");
        p.printp();
        p.changeattr(p, "lisi", 16);
        System.out.println("after change, person is: ");
        p.printp();
    }
}

```  

将代码run起来以后，得到的结果为：  

```
before swap, a is: 1, b is: 2
after swap, a is: 1, b is: 2

before change, person is: 
zhangsan, 15
after change, person is: 
lisi, 16

```  

简单总结起来就是：  
1.如果传入的参数是基本数据类型，方法里的操作不会对原始值做改变。  
2.如果传入的参数是一个对象或者数组或者接口等复杂类型，方法里的操作可以改变这个对象里面的具体内容，但是不会改变对象的内存地址。(如果方法里没做相应操作的话)  