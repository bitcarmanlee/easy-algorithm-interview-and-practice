## 1. 什么是SequenceFile
1.1.sequenceFile文件是Hadoop用来存储二进制形式的[Key,Value]对而设计的一种平面文件(Flat File)。  
1.2.可以把SequenceFile当做是一个容器，把所有的文件打包到SequenceFile类中可以高效的对小文件进行存储和处理。  
1.3.SequenceFile文件并不按照其存储的Key进行排序存储，SequenceFile的内部类Writer提供了append功能。  
1.4.SequenceFile中的Key和Value可以是任意类型Writable或者是自定义Writable。  
1.5.在存储结构上，SequenceFile主要由一个Header后跟多条Record组成，Header主要包含了Key  classname，value classname，存储压缩算法，用户自定义元数据等信息，此外，还包含了一些同步标识，用于快速定位到记录的边界。每条Record以键值对的方式进行存储，用来表示它的字符数组可以一次解析成：记录的长度、Key的长度、Key值和value值，并且Value值的结构取决于该记录是否被压缩。

## 2.SequenceFile支持数据压缩
2.1.SequenceFIle的内部格式取决于是否启用压缩，如果是压缩，则又可以分为记录压缩和块压缩。  
2.2.有一下三种类型的压缩：  
A.无压缩类型：如果没有启用压缩(默认设置)那么每个记录就由它的记录长度(字节数)、键的长度，键和值组成。长度字段为4字节。  
B.记录压缩类型：记录压缩格式与无压缩格式基本相同，不同的是值字节是用定义在头部的编码器来压缩。注意：键是不压缩的。下图为记录压缩：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/sequence/1.png)  

C.块压缩类型：块压缩一次压缩多个记录，因此它比记录压缩更紧凑，而且一般优先选择。当记录的字节数达到最小大小，才会添加到块。该最小值由io.seqfile.compress.blocksize中的属性定义。默认值是1000000字节。格式为记录数、键长度、键、值长度、值。下图为块压缩：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/sequence/2.png)  

## 3.优缺点
SequenceFile优点：  
A.支持基于记录(Record)或块(Block)的数据压缩。  
B.支持splitable，能够作为MapReduce的输入分片。  
C.修改简单：主要负责修改相应的业务逻辑，而不用考虑具体的存储格式。  

SequenceFile的缺点  
A.需要一个合并文件的过程，且合并后的文件不方便查看。  

## 4.具体代码实现
以下代码实现了读写SequenceFile的需求。   

```
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.util.ReflectionUtils;

import java.io.IOException;


public class SequenceTest {

    public static final String output_path = "xxx";
    private static final String[] DATA = { "a", "b", "c", "d"};

    @SuppressWarnings("deprecation")
    public static void write(String pathStr) throws IOException {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path path = new Path(pathStr);

        SequenceFile.Writer writer = SequenceFile.createWriter(fs, conf, path, Text.class, IntWritable.class);
        Text key = new Text();
        IntWritable value = new IntWritable();
        for(int i = 0; i < DATA.length; i++) {
            key.set(DATA[i]);
            value.set(i);
            System.out.printf("[%s]\t%s\t%s\n", writer.getLength(), key, value);
            writer.append(key, value);
        }
        IOUtils.closeStream(writer);
    }

    @SuppressWarnings("deprecation")
    public static void read(String pathStr) throws IOException {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path path = new Path(pathStr);
        SequenceFile.Reader reader = new SequenceFile.Reader(fs, path, conf);

        Writable key = (Writable) ReflectionUtils.newInstance(reader.getKeyClass(), conf);
        Writable value = (Writable) ReflectionUtils.newInstance(reader.getValueClass(), conf);
        while (reader.next(key, value)) {
            System.out.printf("%s\t%s\n", key, value);
        }
        IOUtils.closeStream(reader);
    }

    public static void main(String[] args) throws IOException {
        write(output_path);
        read(output_path);
    }
}

```  

第一个方法为往hdfs上面写，第二个方法则为读。  
