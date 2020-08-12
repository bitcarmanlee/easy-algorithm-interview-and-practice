## 1.线程池相关的类
1.Executor接口，将任务提交与任务的细节解耦开。Executor接口只有一个execute方法  

```
public interface Executor {

    /**
     * Executes the given command at some time in the future.  The command
     * may execute in a new thread, in a pooled thread, or in the calling
     * thread, at the discretion of the {@code Executor} implementation.
     *
     * @param command the runnable task
     * @throws RejectedExecutionException if this task cannot be
     * accepted for execution
     * @throws NullPointerException if command is null
     */
    void execute(Runnable command);
}
```  

2.ExcutorService接口，继承了Executor接口，提供Service的管理功能，比如中断，`    List<Runnable> shutdownNow();`方法。同事，还提供了·`<T> Future<T> submit(Callable<T> task)`等方法。  

3.ThreadPoolExecutor类，继承了AbstractExecutorService类，AbstractExecutorService类继承了ExcutorService接口，所以ThreadPoolExecutor是ExcutorService的实现，我们平时常用的线程池就是ThreadPoolExecutor创建的。  

4.Excutors类，这是个工厂类，提供了常用的创建ExcutorService的静态工厂方法。里面有个静态类DefaultThreadFactory，DefaultThreadFactory类实现了ThreadFactory。  

5.ThreadFactory接口。只有一个方法newThread。  

```
public interface ThreadFactory {

    /**
     * Constructs a new {@code Thread}.  Implementations may also initialize
     * priority, name, daemon status, {@code ThreadGroup}, etc.
     *
     * @param r a runnable to be executed by new thread instance
     * @return constructed thread, or {@code null} if the request to
     *         create a thread is rejected
     */
    Thread newThread(Runnable r);
}
```  

## 2.ThreadPoolExecutor  
我们先看ThreadPoolExecutor的一个构造函数  

```
    /**
     * Creates a new {@code ThreadPoolExecutor} with the given initial
     * parameters and default rejected execution handler.
     *
     * @param corePoolSize the number of threads to keep in the pool, even
     *        if they are idle, unless {@code allowCoreThreadTimeOut} is set
     * @param maximumPoolSize the maximum number of threads to allow in the
     *        pool
     * @param keepAliveTime when the number of threads is greater than
     *        the core, this is the maximum time that excess idle threads
     *        will wait for new tasks before terminating.
     * @param unit the time unit for the {@code keepAliveTime} argument
     * @param workQueue the queue to use for holding tasks before they are
     *        executed.  This queue will hold only the {@code Runnable}
     *        tasks submitted by the {@code execute} method.
     * @param threadFactory the factory to use when the executor
     *        creates a new thread
     * @throws IllegalArgumentException if one of the following holds:<br>
     *         {@code corePoolSize < 0}<br>
     *         {@code keepAliveTime < 0}<br>
     *         {@code maximumPoolSize <= 0}<br>
     *         {@code maximumPoolSize < corePoolSize}
     * @throws NullPointerException if {@code workQueue}
     *         or {@code threadFactory} is null
     */
    public ThreadPoolExecutor(int corePoolSize,
                              int maximumPoolSize,
                              long keepAliveTime,
                              TimeUnit unit,
                              BlockingQueue<Runnable> workQueue,
                              ThreadFactory threadFactory) {
        this(corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue,
             threadFactory, defaultHandler);
    }
```  

corePoolSize：线程池核心线程大小 。将一个待执行的任务放到线程池中的时候，如果待执行的任务数小于该参数，线程池就会创建一个线程来执行该任务。反之，不再创建新的线程。在线程池刚刚创建后，线程并不是立即启动的。如果事先调用了prestartCoreThread()或者prestartAllCoreThreads()方法则会立即启动核心线程。  

maximumPoolSize:线程池允许的最大线程数量。  

keepAliveTime：是否允许线程超时退出   

workQueue：用来保存待执行任务的阻塞队列 。包括ArrayBlockingQueue，SynchronousQueue，LinkedBlockingQueue，PriorityBlockingQueue等。  

ThreadFactory：创建线程的工厂类。  

RejectedExecutionHandler：饱和处理策略。  

## 3.饱和处理策略
如果使用的是有界队列，有可能出现队列和线程池饱和的情况。上面的RejectedExecutionHandler就是用来处理这种情况的。  

JDK中内置有四种策略来实现  
1.AbortPolicy 直接抛出异常，defaultHandler就是这种方式。  
2.CallerRunsPolicy   

```
 /**
     * A handler for rejected tasks that runs the rejected task
     * directly in the calling thread of the {@code execute} method,
     * unless the executor has been shut down, in which case the task
     * is discarded.
     */
public static class CallerRunsPolicy implements RejectedExecutionHandler {
        /**
         * Creates a {@code CallerRunsPolicy}.
         */
        public CallerRunsPolicy() { }

        /**
         * Executes task r in the caller's thread, unless the executor
         * has been shut down, in which case the task is discarded.
         *
         * @param r the runnable task requested to be executed
         * @param e the executor attempting to execute this task
         */
        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
            if (!e.isShutdown()) {
                r.run();
            }
        }
    }
```  

3.DiscardPolicy  

```
    /**
     * A handler for rejected tasks that silently discards the
     * rejected task.
     */
    public static class DiscardPolicy implements RejectedExecutionHandler {
        /**
         * Creates a {@code DiscardPolicy}.
         */
        public DiscardPolicy() { }

        /**
         * Does nothing, which has the effect of discarding task r.
         *
         * @param r the runnable task requested to be executed
         * @param e the executor attempting to execute this task
         */
        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
        }
    }

```  
直接丢弃的策略  

4.DiscardOldestPolicy  

```
    /**
     * A handler for rejected tasks that discards the oldest unhandled
     * request and then retries {@code execute}, unless the executor
     * is shut down, in which case the task is discarded.
     */
    public static class DiscardOldestPolicy implements RejectedExecutionHandler {
        /**
         * Creates a {@code DiscardOldestPolicy} for the given executor.
         */
        public DiscardOldestPolicy() { }

        /**
         * Obtains and ignores the next task that the executor
         * would otherwise execute, if one is immediately available,
         * and then retries execution of task r, unless the executor
         * is shut down, in which case task r is instead discarded.
         *
         * @param r the runnable task requested to be executed
         * @param e the executor attempting to execute this task
         */
        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
            if (!e.isShutdown()) {
                e.getQueue().poll();
                e.execute(r);
            }
        }
    }
}
```  

## 4.Executors类创建线程池
Executors类里面提供了一些静态工厂，生成一些常用的线程池。  

1.newFixedThreadPool：创建固定大小的线程池。线程池的大小一旦达到最大值就会保持不变。  

```
    public static ExecutorService newFixedThreadPool(int nThreads) {
        return new ThreadPoolExecutor(nThreads, nThreads,
                                      0L, TimeUnit.MILLISECONDS,
                                      new LinkedBlockingQueue<Runnable>());
    }
```  

2.newCachedThreadPool：创建一个可缓存的线程池。如果线程池的大小超过了处理任务所需要的线程，那么就会回收部分空闲（60秒不执行任务）的线程。  

```
    public static ExecutorService newCachedThreadPool() {
        return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
                                      60L, TimeUnit.SECONDS,
                                      new SynchronousQueue<Runnable>());
    }
```  

3.newSingleThreadExecutor：顾名思义，创建一个单线程的线程池。  

```
    /**
     * Creates an Executor that uses a single worker thread operating
     * off an unbounded queue. (Note however that if this single
     * thread terminates due to a failure during execution prior to
     * shutdown, a new one will take its place if needed to execute
     * subsequent tasks.)  Tasks are guaranteed to execute
     * sequentially, and no more than one task will be active at any
     * given time. Unlike the otherwise equivalent
     * {@code newFixedThreadPool(1)} the returned executor is
     * guaranteed not to be reconfigurable to use additional threads.
     *
     * @return the newly created single-threaded Executor
     */
    public static ExecutorService newSingleThreadExecutor() {
        return new FinalizableDelegatedExecutorService
            (new ThreadPoolExecutor(1, 1,
                                    0L, TimeUnit.MILLISECONDS,
                                    new LinkedBlockingQueue<Runnable>()));
    }
```  

4.newScheduledThreadPool，相当于创建一个定时任务，实际中相当有用。  

```
    /**
     * Creates a thread pool that can schedule commands to run after a
     * given delay, or to execute periodically.
     * @param corePoolSize the number of threads to keep in the pool,
     * even if they are idle
     * @param threadFactory the factory to use when the executor
     * creates a new thread
     * @return a newly created scheduled thread pool
     * @throws IllegalArgumentException if {@code corePoolSize < 0}
     * @throws NullPointerException if threadFactory is null
     */
    public static ScheduledExecutorService newScheduledThreadPool(
            int corePoolSize, ThreadFactory threadFactory) {
        return new ScheduledThreadPoolExecutor(corePoolSize, threadFactory);
    }
```  

5.newSingleThreadScheduledExecutor：创建一个单线程的线程池  

```
    public static ScheduledExecutorService newSingleThreadScheduledExecutor() {
        return new DelegatedScheduledExecutorService
            (new ScheduledThreadPoolExecutor(1));
    }
```
