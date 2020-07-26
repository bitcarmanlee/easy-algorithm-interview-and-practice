在用java写MR的时候，定义类的第一行一般都是如下方式：  

```
public class XXX extends Configured implements Tool
```  

run方法的一个实例如下：  

```
public int run(String[] args) throws Exception {
        Configuration conf = getConf();
        GenericOptionsParser optionparser = new GenericOptionsParser(conf, args);
        conf = optionparser.getConfiguration();

        @SuppressWarnings("deprecation")
		Job job = new Job(conf, "JudgeIfOrder");
        ...
        ...
        ...
        return (job.waitForCompletion(true) ? 0 : 1);
	}
```  

main方法如下：  

```
	public static void main(String[] args) throws Exception {
		int res = ToolRunner.run(new Configuration(), new JudgeIfOrder(),args);
		System.exit(res);
	}
```  

为什么要这么写？这些类与接口内部是怎样实现的？他们之间是什么关系？相信不少小伙伴都对此会有疑问。为此，我结合相关源码，试图为大家缕缕hadoop里的作业具体是怎样配置的。这些Configured,Configrable,Tool等等又都是些什么鬼。  

首先上一部分源码  
Configurable接口  

```
@InterfaceAudience.Public
@InterfaceStability.Stable
public interface Configurable {

  /** Set the configuration to be used by this object. */
  void setConf(Configuration conf);

  /** Return the configuration used by this object. */
  Configuration getConf();
}

```  

Configured类  

```
/** Base class for things that may be configured with a {@link Configuration}. */
@InterfaceAudience.Public
@InterfaceStability.Stable
public class Configured implements Configurable {

  private Configuration conf;

  /** Construct a Configured. */
  public Configured() {
    this(null);
  }
  
  /** Construct a Configured. */
  public Configured(Configuration conf) {
    setConf(conf);
  }

  // inherit javadoc
  @Override
  public void setConf(Configuration conf) {
    this.conf = conf;
  }

  // inherit javadoc
  @Override
  public Configuration getConf() {
    return conf;
  }
```  

Tool接口：  

```
@InterfaceAudience.Public
@InterfaceStability.Stable
public interface Tool extends Configurable {
  /**
   * Execute the command with the given arguments.
   * 
   * @param args command specific arguments.
   * @return exit code.
   * @throws Exception
   */
  int run(String [] args) throws Exception;
}
```  

从源码上来看，首先我们可以明确的一点是：  
Configurable是这三者底层的接口，Configured类简单地实现了Configurable接口，而Tool接口继承了Configurable接口。  

run方法中，第一句是  

```
Configuration conf = getConf();

```  

因为类XXX已经继承了Configured，所以实际上是调用Configured里的getConf()方法，得到了一个Configuration对象。 Configuration类是配置模块中的最底层的类，从它的package信息就可以看出：  

```
package org.apache.hadoop.conf;
```  

Configuration到底有多底层？咱们看看它源码的一小部分：  

```
  static{
    //print deprecation warning if hadoop-site.xml is found in classpath
    ClassLoader cL = Thread.currentThread().getContextClassLoader();
    if (cL == null) {
      cL = Configuration.class.getClassLoader();
    }
    if(cL.getResource("hadoop-site.xml")!=null) {
      LOG.warn("DEPRECATED: hadoop-site.xml found in the classpath. " +
          "Usage of hadoop-site.xml is deprecated. Instead use core-site.xml, "
          + "mapred-site.xml and hdfs-site.xml to override properties of " +
          "core-default.xml, mapred-default.xml and hdfs-default.xml " +
          "respectively");
    }
    addDefaultResource("core-default.xml");
    addDefaultResource("core-site.xml");
  }
```  

同学们请看最后两行，它会加载core-default.xml与core-site.xml这两个最基础的配置文件。  

GenericOptionsParser这个类，一看就知道是解析参数用的。  

```
       GenericOptionsParser optionparser = new GenericOptionsParser(conf, args);
        conf = optionparser.getConfiguration();
```  

上面这两行代码，自然就是用来解析输入参数用的。。。  

咱们来看最后一行代码  

```
int res = ToolRunner.run(new Configuration(), new JudgeIfOrder(),args);

```  

上ToolRunner的源码  

```
public static int run(Configuration conf, Tool tool, String[] args) 
    throws Exception{
    if(conf == null) {
      conf = new Configuration();
    }
    GenericOptionsParser parser = new GenericOptionsParser(conf, args);
    //set the configuration back, so that Tool can configure itself
    tool.setConf(conf);
    
    //get the args w/o generic hadoop args
    String[] toolArgs = parser.getRemainingArgs();
    return tool.run(toolArgs);
  }

public static int run(Tool tool, String[] args) 
    throws Exception{
    return run(tool.getConf(), tool, args);
  }
```  
ToolRunner中与run相关的方法是这两个。我们的代码里给run方法传了三个参数，实际上执行的就是ToolRunner里第一个run方法了，ToolRunner会调用tool接口中的run方法。而我们自己写的XXX类实现了tool接口，重写了run方法。所以最后实际上调用的是我们自己写的run()方法了！  


写到这里，同学们应该差不多明白里头的来龙去脉了吧。。。  

在stackoverflow里看到了一段相关的描述，直接copy过来，就不翻译了，请自行阅读  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/configure/1.png)