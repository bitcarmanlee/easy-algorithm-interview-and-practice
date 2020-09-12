单例模式是实际项目中使用最多的一种设计模式，有着非常广泛的使用场景。下面我们就结合一个实际项目中的例子，来说说单例模式的使用方式。  

## 1.经典单例模式之懒汉模式

```
import java.util.HashMap;
import java.util.Map;

public class Singleton {

    private static Map<String, String> testMap = new HashMap<String, String>();

    private static Singleton instance;

    private Singleton() {
        initTestMap();
    }

    public static void initTestMap() {
        for(int i=0; i<10; i++) {
            String value = "a" + String.valueOf(i);
            testMap.put(String.valueOf(i), value);
        }
    }

    public static Singleton getInstance() {
        if(instance == null) {
            instance = new Singleton();
        }
        return instance;
    }

}

```  

这个单例对象里面有一个testMap，我们希望Singleton对象初始化的时候testMap就已经初始化。  
注意的几个点是：  
1.instance对象与testMap对象均为static对象，这样可以直接用类名调用。  
2.在构造方法中，将testMap初始化。  

## 2.饿汉模式

```
import java.util.HashMap;
import java.util.Map;

public class Singleton {

    private static Map<String, String> testMap = new HashMap<String, String>();

    private static Singleton instance = new Singleton();

    private Singleton() {
        initTestMap();
    }

    public static void initTestMap() {
        for(int i=0; i<10; i++) {
            String value = "a" + String.valueOf(i);
            testMap.put(String.valueOf(i), value);
        }
    }

    public static synchronized Singleton getInstance() {
        return instance;
    }

}
```  

饿汉模式与懒汉模式相比较起来，一上来就直接将实例初始化，不存在延迟加载的问题。  

上面的两种写法，没有考虑多线程的情况。如果是在多线程的场景下使用，请参考后面的文章。  

## 3.双重锁校验(double checked locking pattern)
双重检验锁模式（double checked locking pattern），是一种使用同步块加锁的方法。程序员称其为双重检查锁，因为会有两次检查 instance == null，一次是在同步块外，一次是在同步块内。为什么在同步块内还要再检验一次？因为可能会有多个线程一起进入同步块外的 if，如果在同步块内不进行二次检验的话就会生成多个实例了。  

```
public class Singleton {

    private static Singleton instance;

    private Singleton() {}

    public static  Singleton getInstance() {
        if(instance == null) {
            synchronized(Singleton.class) {
                if(instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```  

这段代码看起来很完美，很可惜，它是有问题。主要在于instance = new Singleton()这句，这并非是一个原子操作，事实上在 JVM 中这句话大概做了下面 3 件事情。  

1.给 instance 分配内存  
2.调用 Singleton 的构造函数来初始化成员变量  
3.将instance对象指向分配的内存空间（执行完这步 instance 就为非 null 了）  
但是在 JVM 的即时编译器中存在指令重排序的优化。也就是说上面的第二步和第三步的顺序是不能保证的，最终的执行顺序可能是 1-2-3 也可能是 1-3-2。如果是后者，则在 3 执行完毕、2 未执行之前，被线程二抢占了，这时 instance 已经是非 null 了（但却没有初始化），所以线程二会直接返回 instance，然后使用，然后顺理成章地报错。  

我们只需要将 instance 变量声明成 volatile 就可以了。  

```
public class Singleton {

    private volatile static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if(instance == null) {
            synchronized(Singleton.class) {
                if(instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```  

volatile用在多线程，同步变量。 线程为了提高效率，将某成员变量(如A)拷贝了一份（如B），线程中对A的访问其实访问的是B。只在某些动作时才进行A和B的同步。因此存在A和B不一致的情况。volatile就是用来避免这种情况的。volatile告诉jvm， 它所修饰的变量不保留拷贝，直接访问主内存中的（也就是上面说的A)   

参考文章：  
http://wuchong.me/blog/2014/08/28/how-to-correctly-write-singleton-pattern/