## 1.java中的线程状态
在java中，线程通常有五种状态：创建，就绪，运行，阻塞与死亡。  
1：创建(NEW)  
在生成线程对象的时候，并没有调用start方法，这是线程的创建状态。  
2：就绪(RUNABLE)  
当调用线程对象的start方法以后，线程就进入了就绪状态。但是此时线程调度程序还没有把该线程设置为当前线程，此时处于就绪状态。在线程运行之后，从等待或者睡眠中回来之后，也会处于就绪状态。  
3：运行(RUNNING)  
线程调度程序将处于就绪状态的线程设置为当前线程，此时线程就进入了运行状态，开始运行run函数当中的代码。  
4：阻塞(BLOCKED)  
线程正在运行的时候，被暂停，通常是为了等待某个时间的发生(比如说某项资源就绪)之后再继续运行。sleep,suspend，wait等方法都可以导致线程阻塞。  
5：死亡(TERMINATED)  
如果一个线程的run方法执行结束或者调用stop方法后，该线程就会死亡。对于已经死亡的线程，无法再使用start方法令其进入就绪。  


## 2.Thread中的start()方法与run()方法
java中的线程是通过java.lang.Thread类来实现的。JVM启动时会有一个由主方法所定义的线程，同时可以通过创建Thread的实例来创建新的线程。每个线程都是通过某个特定Thread对象所对应的方法run()来完成其操作的，方法run()称为线程体。通过调用Thread类的start()方法来启动一个线程。  

看下jdk中的源码  

```
   /**
     * If this thread was constructed using a separate
     * <code>Runnable</code> run object, then that
     * <code>Runnable</code> object's <code>run</code> method is called;
     * otherwise, this method does nothing and returns.
     * <p>
     * Subclasses of <code>Thread</code> should override this method.
     *
     * @see     #start()
     * @see     #stop()
     * @see     #Thread(ThreadGroup, Runnable, String)
     */
    @Override
    public void run() {
        if (target != null) {
            target.run();
        }
    }
```  

再参考一下start方法  

```
   /**
     * Causes this thread to begin execution; the Java Virtual Machine
     * calls the <code>run</code> method of this thread.
     * <p>
     * The result is that two threads are running concurrently: the
     * current thread (which returns from the call to the
     * <code>start</code> method) and the other thread (which executes its
     * <code>run</code> method).
     * <p>
     * It is never legal to start a thread more than once.
     * In particular, a thread may not be restarted once it has completed
     * execution.
     *
     * @exception  IllegalThreadStateException  if the thread was already
     *               started.
     * @see        #run()
     * @see        #stop()
     */
    public synchronized void start() {
        /**
         * This method is not invoked for the main method thread or "system"
         * group threads created/set up by the VM. Any new functionality added
         * to this method in the future may have to also be added to the VM.
         *
         * A zero status value corresponds to state "NEW".
         */
        if (threadStatus != 0)
            throw new IllegalThreadStateException();

        /* Notify the group that this thread is about to be started
         * so that it can be added to the group's list of threads
         * and the group's unstarted count can be decremented. */
        group.add(this);

        boolean started = false;
        try {
            start0();
            started = true;
        } finally {
            try {
                if (!started) {
                    group.threadStartFailed(this);
                }
            } catch (Throwable ignore) {
                /* do nothing. If start0 threw a Throwable then
                  it will be passed up the call stack */
            }
        }
    }
```  

从源码以及当中的注释可以看出，run()其实是个普通方法，只不过当线程调用了start( )方法后，一旦线程被CPU调度，处于运行状态，那么线程才会去调用这个run()方法；  
同时，run方法就是一个普通的方法，并不是需要调用start()方法以后才能调用run()方法，线程对象可以随时调用run()方法。  


## 3.示例

```
public class ThreadDemo1 extends Thread {

    public ThreadDemo1() {
        this.setName("ThreadDemo1");
    }

    public static void printThreadInfo() {
        System.out.println("current thread name is: " + Thread.currentThread().getName());
    }

    @Override
    public void run() {
        while (true) {
            printThreadInfo();
            try {
                Thread.sleep(100);
            } catch (Exception ex) {
                throw new RuntimeException(ex);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Thread t1 = new Thread(new Task(1));
        Thread t2 = new Thread(new Task(2));

        t1.start();
        t2.start();
    }
}
```

```
public class Task implements Runnable {

    int count;

    public Task(int count) {
        this.count = count;
    }

    @Override
    public void run() {
        System.out.println("count is: " + count);
    }
}
```  

上面的运行结果有可能是：  

```
count is: 1
count is: 2
```  
也有可能是  

```
count is: 2
count is: 1
```  

但是如果将  

```
        t1.start();
        t2.start();
```  

换成  

```
        t1.run();
        t2.run();
```  

那么结果一定是  

```
count is: 1
count is: 2
```  

再看另外一个示例，模拟两个线程运行。  

```
public class ThreadDemo2 {
    public static void main(String[] args) {
        Thread t1 = new Thread(new C1());
        Thread t2 = new Thread(new C2());

        t1.start();
        t2.start();
        //t1.run();
        //t2.run();
    }
}


class C1 implements Runnable {

    @Override
    public void run() {
        try {
            for (int i = 0; i < 10; i++) {
                System.out.println(i);
                Thread.sleep(1000);
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }
    }
}

class C2 implements Runnable {

    public void run() {
        try {
            for (int j = 0; j > -10; j--) {
                System.out.println(j);
                Thread.sleep(1000);
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }
    }
}
```  

如果是调用start方法，输出为

```
0
0
1
-1
2
-2
-3
3
-4
4
-5
5
-6
6
7
-7
8
-8
9
-9
```  

如果调用的是run方法，结果为  

```
0
1
2
3
4
5
6
7
8
9
0
-1
-2
-3
-4
-5
-6
-7
-8
-9
```  

## 4.简单小结  
start方法是用于启动线程的，可以实现并发，而run方法只是一个普通方法，是不能实现并发的，只是在并发执行的时候会调用。  
