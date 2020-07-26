注：以下源码都基于hadoop 2.5版本。  

hadoop里相关的配置在org.apache.hadoop.conf包里，Configuration类就在里面。关于配置类的相互关系，已经在：  

http://blog.csdn.net/bitcarmanlee/article/details/51454564中 有过详细的介绍。为了让大家更好地看清楚conf的东东，特意截个图：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/configure/2.png)    

## 1.温习一下前面的内容
在前面的文章中，我们已经介绍了这几者的关系，再给大伙梳理一下：  
Configurable是一个接口，里面就有一对set/get方法  

```
public interface Configurable {

  /** Set the configuration to be used by this object. */
  void setConf(Configuration conf);

  /** Return the configuration used by this object. */
  Configuration getConf();
}
```  
Configured则实现了Configurable接口，并在里面简单的重写了这对get/set方法：  

```
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

}
```  

## 2.Configuration闪亮登场
今天我们的主角是Configuration,首先来看看Configuration的继承关系：  

```
public class Configuration implements Iterable<Map.Entry<String,String>>,Writable
```  

在Configuration的类声明时，可以看出Configuration实现了Iterable接口与Writable接口。  

使用过hadoop的同学都知道，hadoop里的conf文件夹里有许多配置文件。拿http://blog.csdn.net/bitcarmanlee/article/details/51464886里提到的配置为例：  

```
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
	...
    <property>
        <name>fs.trash.interval</name>
        <value>1440</value>
    </property>
    <property>
        <name>fs.trash.checkpoint.interval</name>
        <value>1440</value>
    </property>
	...
</configuration>
```  

可以看出来，XML配置文件的根节点就是Configuration!然后下一级节点是property，每个property都有name，value，name自然就是配置项的key，value就是value了。  
等等，看到property的时候，同学们想起什么来没有？java里面是不是有个properties？用来干嘛的？不就是解析配置的嘛。别着急，后面还会提到这个。  

## 3.Configuration快速浏览
Configuration里的东西还是挺多的，源码里有二千六百多行，里面的各种属性，方法以及内部类太多了，实在列不过来。给大伙挑点重要的先看看吧  

```
  private ArrayList<Resource> resources = new ArrayList<Resource>();
  
  static final String UNKNOWN_RESOURCE = "Unknown";

  private Set<String> finalParameters = new HashSet<String>();
  
  private boolean loadDefaults = true;

  private static final WeakHashMap<Configuration,Object> REGISTRY = 
    new WeakHashMap<Configuration,Object>();
  
  private static final CopyOnWriteArrayList<String> defaultResources =
    new CopyOnWriteArrayList<String>();

  private static final Map<ClassLoader, Map<String, WeakReference<Class<?>>>>
    CACHE_CLASSES = new WeakHashMap<ClassLoader, Map<String, WeakReference<Class<?>>>>();

  private static final Class<?> NEGATIVE_CACHE_SENTINEL =
    NegativeCacheSentinel.class;

  private HashMap<String, String[]> updatingResource;
 
```  

为了保持篇幅不至于太过冗长，忍痛把源码中的注释给删了。好吧，其实注释信息非常关键。呜呜呜。。。  
resources是Configuration的一个内部静态类，ArrayList是保存这些resources的集合。finalParameters从名字就可以看出来，他存的是一些不可变的配置。loadDefaults我们前头提到过，Configuration会默认加载一些配置文件，这个开关应该就是他了。  
在源码六百多行的位置，还有Configuration里非常重要的两个属性  

```
  private Properties properties;
  private Properties overlay;
```  

没错，这个Properties，就是java.util.Properties，就是我们经常用来解析配置文件的那个Properties!  

就在这两行的上面，有一个static块，即代码初始块：  

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

写过java的同学都清楚，static块即代码初始化块的优先级是高于构造方法的，即在new出Configuration对象之前，这段代码就已经被执行了。很明显，新版的api是想告诉我们，让我们尽量别用hadoop-site.xml的配置文件，而是让我们分别使用core-site.xml,mapred-site.xml,hdfs-site.xml三个配置文件。初始化块的最后，调用了addDefaultResource()方法。  
来看看addDefaultResource是个什么鬼  

```
 public static synchronized void addDefaultResource(String name) {
    if(!defaultResources.contains(name)) {
      defaultResources.add(name);
      for(Configuration conf : REGISTRY.keySet()) {
        if(conf.loadDefaults) {
          conf.reloadConfiguration();
        }
      }
    }
  }
```  

首先，这个方法是synchronized修饰的。然后，这个REGISTRY在我们前面已经列出来了，是一个`static final WeakHashMap<Configuration,Object>`，后面我们看Configuration的构造方法的时候，会看到每产生一个Configuration对象，都会put到REGISTRY中去。由于REGISTRY是static final属性，所以全局都只有同一个REGISTRY。而这个defaultResources，则是`static final CopyOnWriteArrayList<String>`。代码的最后一行，是一个reloadConfiguration方法。继续看这个reloadConfiguration是个什么鬼：  

```
/**
   * Reload configuration from previously added resources.
   *
   * This method will clear all the configuration read from the added 
   * resources, and final parameters. This will make the resources to 
   * be read again before accessing the values. Values that are added
   * via set methods will overlay values read from the resources.
   */
  public synchronized void reloadConfiguration() {
    properties = null;                            // trigger reload
    finalParameters.clear();                      // clear site-limits
  }
```  

特意把注释给添加上。这个方法的作用，注释里面已经说得很清楚了，就是  
`This method will clear all the configuration read from the added resources, and final parameters.`  

## 4.三个构造方法
static代码块执行完以后，开始执行构造方法：  

```
/** A new configuration. */
  public Configuration() {
    this(true);
  }

  /** A new configuration where the behavior of reading from the default 
   * resources can be turned off.
   * 
   * If the parameter {@code loadDefaults} is false, the new instance
   * will not load resources from the default files. 
   * @param loadDefaults specifies whether to load from the default files
   */
  public Configuration(boolean loadDefaults) {
    this.loadDefaults = loadDefaults;
    updatingResource = new HashMap<String, String[]>();
    synchronized(Configuration.class) {
      REGISTRY.put(this, null);
    }
  }
  
  /** 
   * A new configuration with the same settings cloned from another.
   * 
   * @param other the configuration from which to clone settings.
   */
  @SuppressWarnings("unchecked")
  public Configuration(Configuration other) {
   this.resources = (ArrayList<Resource>) other.resources.clone();
   synchronized(other) {
     if (other.properties != null) {
       this.properties = (Properties)other.properties.clone();
     }

     if (other.overlay!=null) {
       this.overlay = (Properties)other.overlay.clone();
     }

     this.updatingResource = new HashMap<String, String[]>(other.updatingResource);
     this.finalParameters = new HashSet<String>(other.finalParameters);
   }
   
    synchronized(Configuration.class) {
      REGISTRY.put(this, null);
    }
    this.classLoader = other.classLoader;
    this.loadDefaults = other.loadDefaults;
    setQuietMode(other.getQuietMode());
  }
  
```  
里面一共有三个构造方法。如果我们直接new一个Configuration，首先会调用其中的无参构造方法，无参构造方法会调用第二个构造方法，就这么简单。到此为止，Configuration相关的前期工作就都完成了。  


## 5.属性延迟加载
前面我们啰啰嗦嗦讲了这么一大堆，又是static代码块又是构造函数，不知道大家发现一点没有，都已经new出新对象了，但是好像并没有真正解析配置文件里的内容，那到底什么时候才开始呢？请看getProps方法：  

```
 protected synchronized Properties getProps() {
    if (properties == null) {
      properties = new Properties();
      HashMap<String, String[]> backup = 
        new HashMap<String, String[]>(updatingResource);
      loadResources(properties, resources, quietmode);
      if (overlay!= null) {
        properties.putAll(overlay);
        for (Map.Entry<Object,Object> item: overlay.entrySet()) {
          String key = (String)item.getKey();
          updatingResource.put(key, backup.get(key));
        }
      }
    }
    return properties;
  }
```  
成员变量properties里的数据，只有真正需要的时候，才会被加载进来。在这个方法里，首先判断properties是否为空。如果为空，这时才执行loadResources()方法加载配置资源。这里其实采用了延迟加载的设计模式，当真正需要配置数据的时候，才开始分析配置文件。  

## 6.结束语  
博主的理解可能有所不对，或者有所偏差。如果有什么问题，欢迎大家指出。  
本文的部分思路以及内容，参考了以下同学的成果：  
1.http://blog.csdn.net/androidlushangderen/article/details/41599873  
2.http://blog.csdn.net/workformywork/article/details/17298689  