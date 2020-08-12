## 1.花一天半时间配置spark开发环境
RD同学开发代码肯定需要开发环境。为了配置好spark的本地开发测试环境，宝宝前后花了一天半的时间。各种踩坑各种无奈各种崩溃。文章以下内容都是宝宝一天半时间的实践吐血总结。绝对值得同学们学习收藏。  
  

## 2.大坑eclipse不适合spark
因为宝宝之前一直用的是eclipse，所以自然想搭建eclipse+scala+maven+spark的开发测试环境。但是经过一天的折腾，宝宝终于放弃了。得出的结论是：还是按照spark官方的提示，用IntelliJ吧。  

简单描述一下过程：宝宝各种搜资料，大部分的教程甚至还有歪果仁写的pdf教程，都是推荐使下载eclipse的scala插件，然后再下载net.alchim31.maven组织出的插件，最后再新建一个maven项目即可。但是宝宝把所有步骤完成以后，最后出来的项目始终有错误，pom.xml文件直接报错：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/1.png)  

这个错误在maven里相当棘手。如果有不太熟悉的同学可以google一把这个错误。反正宝宝是尝试了各种方法，折腾了很久，都没能搞定。。。最后，gg了。  

## 3.重新安装IntelliJ环境
本来宝宝不太想换IDE的，换个IDE又得重新学习重新适应。。最重要的是，又要特么重新记快捷键。但是，现在没办法了，为了spark，换吧。。。  
上IntelliJ官网，下载安装自己机器OS对应的版本即可。。。  

## 4.安装scala插件
安装好IntelliJ以后，在IntelliJ->Preferences->Plugins里，点击对话框右边下方中间位置的Browse repositories按钮，然后在弹出的对话框中，输入scala，选择安装次数最多的那个安装。。。  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/2.png)  

根据自己的网络情况，安装时间不定。安装完毕，重启IDE，这时候再进IntelliJ->Preferences->Languages&Frameworks，可以看到已经有Scala选项。  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/3.png)  


## 5.大坑之spark版本与scala版本
我用的spark版本是1.6。最开始时候scala版本为2.11，然后代码提交以后，代码一直报错：  

```
Exception in thread “main” java.lang.NoSuchMethodError: scala.collection.immutable.HashSet$.empty()Lscala/collection/immutable/HashSet;
```  

宝宝表示之前对scala也不熟，一下就懵逼了。赶紧查查。发现大部分同学说是scala版本的问题。好吧，那赶紧把scala版本改了。妈的又临时下了scala的2.10版本，然后在IntelliJ里配置上  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/4.png)  

后续再运行代码，就不报相关的错误了。。。  

同时将spark的相关jar包也加上。暂时我们只需要添加spark-assembly-1.6.0-hadoop2.4.0.jar，在spark的lib目录中就可以找到。  
点开File->Libraries，然后点击上面的"+"，将jar包添加：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/5.png)  

添加即可。  

## 6.SparkPi代码
将spark中自带的SparkPi程序稍作改动拿过来：  

```
/**
  * Created by lei.wang on 16/7/26.
  */

import org.apache.spark._

import scala.math.random

object SparkPi {
  def main(args: Array[String]):Unit = {
    val conf = new SparkConf().setAppName("Spark Pi").setMaster("spark://192.168.16.93:7077").setJars(List("/Users/lei.wang/code/scala/demo/out/artifacts/first/first.jar"))
    val spark = new SparkContext(conf)
    val slices = if (args.length > 0) args(0).toInt else 2
    val n = math.min(100000L * slices, Int.MaxValue).toInt // avoid overflow
    val count = spark.parallelize(1 until n, slices).map { i =>
      val x = random * 2 - 1
      val y = random * 2 - 1
      if (x*x + y*y < 1) 1 else 0
    }.reduce(_+_)
    println("Pi is roughly " + 4.0 * count / n)
    spark.stop()
  }
}
```  

将setMaster与setJars里的参数换成你自己的参数即可。  

## 7.大坑之打jar包技巧
spark自带的SparkPi代码中conf这一行是这样的：  

```
val conf = new SparkConf().setAppName("Spark Pi")
```  

本宝宝因为经验不足，最开始就是这么写的:  

```
val conf = new SparkConf().setAppName("Spark Pi").setMaster("spark://192.168.16.93:7077")
```  

最后在IntelliJ里run的时候，一直报如下错误：  

```
Caused by: java.lang.ClassNotFoundException: SparkPi$$anonfun$1
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	at java.lang.Class.forName0(Native Method)
	at java.lang.Class.forName(Class.java:348)
	...
```  

宝宝又懵逼了。是按官方代码来写的好么。宝宝花了大半天时间调试，在shell里面直接运行时OK的。各种代码逻辑调试也是OK的。试来试去可以确认的是代码逻辑没有问题，最后确定应该是IDE的开发环境引起的。  

但是为什么找不到这个SparkPi的类了？宝宝又花了很长时间各种搜素，终于找出了原因：  
File->Project Structure->Artifacts，这里会将咱们的代码打成jar包，打成jar以后，在IDE里再调用setJars方法指定jar包路径，IntelliJ才能正常运行！    
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/6.png)  

## 8.大坑之slaves设置
spark conf里slaves.template里默认设置的一般是localhost。但是宝宝发现在本机执行start-all.sh以后，光起了一个master，一个worker没有。相当于是一光杆司令，地下没干活的小兵。后来发现，是localhost有时候不能完美替换本机地址。所以保险起见，将localhost换成你本机的ip地址更为稳妥。  