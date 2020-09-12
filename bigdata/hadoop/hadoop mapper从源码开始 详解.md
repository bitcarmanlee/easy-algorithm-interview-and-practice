hadoop的mapreduce计算框架中，最重要的两个部分自然就是mapper跟reducer了。写了这么久的MR，一直没有机会研究源码，也挺遗憾的。趁着这波有一些要深入了解的需求，加上周末的一些时间，仔细阅读了一下mapper相关源码，有了自己的一些小小心得，权当笔记。写得不好或者有不对的地方，请童鞋们指出  

## 1.mapper源码

```
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.hadoop.mapreduce;

import java.io.IOException;

import org.apache.hadoop.classification.InterfaceAudience;
import org.apache.hadoop.classification.InterfaceStability;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.RawComparator;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.mapreduce.task.MapContextImpl;

@InterfaceAudience.Public
@InterfaceStability.Stable
public class Mapper<KEYIN, VALUEIN, KEYOUT, VALUEOUT> {

  /**
   * The <code>Context</code> passed on to the {@link Mapper} implementations.
   */
  public abstract class Context
    implements MapContext<KEYIN,VALUEIN,KEYOUT,VALUEOUT> {
  }
  
  /**
   * Called once at the beginning of the task.
   */
  protected void setup(Context context
                       ) throws IOException, InterruptedException {
    // NOTHING
  }

  /**
   * Called once for each key/value pair in the input split. Most applications
   * should override this, but the default is the identity function.
   */
  @SuppressWarnings("unchecked")
  protected void map(KEYIN key, VALUEIN value, 
                     Context context) throws IOException, InterruptedException {
    context.write((KEYOUT) key, (VALUEOUT) value);
  }

  /**
   * Called once at the end of the task.
   */
  protected void cleanup(Context context
                         ) throws IOException, InterruptedException {
    // NOTHING
  }
  
  /**
   * Expert users can override this method for more complete control over the
   * execution of the Mapper.
   * @param context
   * @throws IOException
   */
  public void run(Context context) throws IOException, InterruptedException {
    setup(context);
    try {
      while (context.nextKeyValue()) {
        map(context.getCurrentKey(), context.getCurrentValue(), context);
      }
    } finally {
      cleanup(context);
    }
  }
}

```  

为了避免太过冗长，把源码里的一些注释以及说明拿掉了，后面再跟大家一一道来。  

## 2.mapper类的基本结构
mapper类里的结构其实不太复杂，总共四个方法，一个抽象类，具体的结构如下图所示：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/mapper/1.png)  

这几个方法的功能相对也很好理解：setup()方法一般就是用来做一些在map真正开始干活之前的准备工作，例如相关配置文件的读取，参数的传递等；clean()方法则是用来做一些擦屁股的活。当然，这两个函数在实际中也是可以不写的。如果你不用传参不用读配置，代码逻辑也相对简单没有要后续擦屁股的活，自然也就用不着这两函数。  

既然是mapper类，那map()方法肯定就是我们真正干活的地方了。  
以mapper源码中的wordcount例子中的map方法为例：  

```
public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
    StringTokenizer itr = new StringTokenizer(value.toString());
    while (itr.hasMoreTokens()) {
      word.set(itr.nextToken());
      context.write(word, one);
     }
}
```  

相信有点java基础的同学都能看懂上面这个方法。就是将输入的一行文本，每次拆分成一个(word,one)的k,v对，然后分发给reducer做进一步的处理。如果是wordcount，那就是相同的word被分发到相同的reduce端，然后做count操作。  


run()方法则是驱动整个代码按照setup(),map(),cleanup()的流程正常工作的一个方法。里面的可配置项相对也比较多比较杂。后面有用的时候跟大家专门讲讲run()方法里的相关配置。  

context是mapper里的一个内部类，主要是为了在map任务或者reduce任务中跟踪task的相关状态。在mapper类中，这个context就可以存储一些job conf有关的信息。在setup()方法中，就可以用context读取相关的配置信息。（这部分的源码还没有仔细研究，如果有什么问题欢迎大家指出)  

context是一个抽象类，具体的继承层次关系如下图所示：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/mapper/2.png)

## 3.mapper类的一些子类
mapper类其实类似于一个接口，里面没有任何具体实现，实际开发场景中肯定需要我们至少实现map()方法来满足业务需求。同时，hadoop中也有一些mapper的子类，具体有哪些，请看下图  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/mapper/3.png)  

由图可知，mapper一共有九个子类。我们挑其中的几个子类来稍做分析。  

### 3.1 InverseMapper
首先上源码  

```
@InterfaceAudience.Public
@InterfaceStability.Stable
public class InverseMapper<K, V> extends Mapper<K,V,V,K> {

  /** The inverse function.  Input keys and values are swapped.*/
  @Override
  public void map(K key, V value, Context context
                  ) throws IOException, InterruptedException {
    context.write(value, key);
  }
  
}

```  

从InverseMapper的源码很容易看出，他就做了一件很简单的事情：重写map()方法，将map阶段的k,v掉换了个，然后输出(v,k)对。  

### 3.2 TokenCounterMapper

```
public class TokenCounterMapper extends Mapper<Object, Text, Text, IntWritable>{
    
  private final static IntWritable one = new IntWritable(1);
  private Text word = new Text();
  
  @Override
  public void map(Object key, Text value, Context context
                  ) throws IOException, InterruptedException {
    StringTokenizer itr = new StringTokenizer(value.toString());
    while (itr.hasMoreTokens()) {
      word.set(itr.nextToken());
      context.write(word, one);
    }
  }
}
```  

wordcount的mapper阶段实现，不解释。  

### 3.3 RegexMapper

```
public class RegexMapper<K> extends Mapper<K, Text, Text, LongWritable> {

  public static String PATTERN = "mapreduce.mapper.regex";
  public static String GROUP = "mapreduce.mapper.regexmapper..group";
  private Pattern pattern;
  private int group;

  public void setup(Context context) {
    Configuration conf = context.getConfiguration();
    pattern = Pattern.compile(conf.get(PATTERN));
    group = conf.getInt(GROUP, 0);
  }

  public void map(K key, Text value,
                  Context context)
    throws IOException, InterruptedException {
    String text = value.toString();
    Matcher matcher = pattern.matcher(text);
    while (matcher.find()) {
      context.write(new Text(matcher.group(group)), new LongWritable(1));
    }
  }
}

```  

从源码比较容易看出，这是正则版的wordcount。  

## 4.mapper阶段流程小结
总结起来，mapper阶段的工作流程如下：  
1.先把输入的文件，按照一定的标准和方法做切分(InputSplit)。这个切分的过程很关键，因为MR的核心思想就是将一个巨大的任务切分成多个小任务分发给不同节点计算，每一个输入片对应的就是一个mapper。如果切分没有做好，后面的工作自然就无从谈起。后续有时间再专门阐述一下切分相关的具体细节。  
2.对切分完的输入按照一定的规则解析成(k,v)对。  
3.调用Mapper类中的map()方法，对第二步解析出来的(k,v)对进行操作。这也是我们需要实现真正逻辑的地方。每调用一次map()方法，就会输出0个或1个或多个(k,v)对。  
4.对第三步输出的(k,v)对进行partition 。partition是基于k进行的，这样就保证相同的k落在同一个分区之中。  
5.对第四步产生的(k,v)对排序。首先是按k排序，如果k相同，则按v排序。如果后续还有combiner阶段，则继续进行combiner；如果没有，则直接将数据输出到磁盘。  
6.combiner阶段。其实跟reduce的实现逻辑是一样的。比如在wordcount中，reducer类都不用实现，直接在run()方法中用`job.setReducerClass(IntSumReducer.class)`设置即可。  