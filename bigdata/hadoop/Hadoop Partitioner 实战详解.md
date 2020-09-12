Partitioner是MR中非常重要的组件。Partitioner的作用是针对Mapper阶段的中间数据进行切分，然后将相同分片的数据交给同一个reduce处理。Partitioner过程其实就是Mapper阶段shuffle过程中关键的一部分。    

在老版本的hadoop中，Partitioner是个接口。而在后来新版本的hadoop中，Partitioner变成了一个抽象类（本人目前使用的版本为2.6）。  

```
@InterfaceAudience.Public
@InterfaceStability.Stable
public abstract class Partitioner<KEY, VALUE> {
  
  /** 
   * Get the partition number for a given key (hence record) given the total 
   * number of partitions i.e. number of reduce-tasks for the job.
   *   
   * <p>Typically a hash function on a all or a subset of the key.</p>
   *
   * @param key the key to be partioned.
   * @param value the entry value.
   * @param numPartitions the total number of partitions.
   * @return the partition number for the <code>key</code>.
   */
  public abstract int getPartition(KEY key, VALUE value, int numPartitions);
  
}
```  

hadoop中默认的partition是HashPartitioner。根据Mapper阶段输出的key的hashcode做划分：  

```
public class HashPartitioner<K, V> extends Partitioner<K, V> {

  /** Use {@link Object#hashCode()} to partition. */
  public int getPartition(K key, V value,
                          int numReduceTasks) {
    return (key.hashCode() & Integer.MAX_VALUE) % numReduceTasks;
  }

}
```  

在很多场景中，我们是需要通过重写Partitioner来实现自己需求的。例如，我们有全国分省份的数据，我们经常需要将相同省份的数据输入到同一个文件中。这个时候，通过重写Partitioner就可以达到上面的目的。  


给大家上完整的源码  

```
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by WangLei on 17-3-2.
 */
public class PartitionTest extends Configured implements Tool{

    static class TestMapper extends Mapper<LongWritable,Text,Text,IntWritable> {

        @Override
        protected void map(LongWritable key,Text value, Context context) throws IOException,InterruptedException{
            String result = value.toString().trim();
            context.write(new Text(result),new IntWritable(1));
        }
    }

    static class TestReducer extends Reducer<Text,IntWritable,Text,IntWritable> {

        @Override
        protected void reduce(Text key,Iterable<IntWritable> values,Context context) throws IOException,InterruptedException {
            int sum = 0;
            for(IntWritable each:values) {
                sum += Integer.parseInt(each.toString());
            }
            context.write(key,new IntWritable(sum));
        }
    }

    public static class ProvincePartition extends Partitioner<Text,IntWritable> {

        private Map<String,Integer> getProvinceMap() {
	        //测试数据里包含有四个省
            String[] provinces = {"湖南","湖北","北京","上海"};
            Map<String,Integer> map = new HashMap<String,Integer>();
            for(int i=0; i<provinces.length; i++) {
                map.put(provinces[i],i);
            }
            return map;
        }

        @Override
        public int getPartition(Text key,IntWritable value, int numPartitions) {
            Map<String,Integer> map = getProvinceMap();
            //根据省份对应的序号输入到对应的文件中
            if(map.containsKey(key.toString())) {
	            //湖南输入到part-r-00000部分，以此类推
                return map.get(key.toString()) % numPartitions;
            }
            return 0;
        }
    }

    @Override
    public int run(String[] args) throws Exception{
        Configuration conf = new Configuration();
        String inputPath = args[0];
        String outputPath = args[1];

        Job job = Job.getInstance(conf,"PartitionTest");
        job.setJarByClass(PartitionTest.class);
        job.setMapperClass(TestMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job,new Path(inputPath));
        job.setPartitionerClass(ProvincePartition.class);

        job.setReducerClass(TestReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        //因为有4个省的数据，所有numReduceTasks设为4
        job.setNumReduceTasks(4);

        FileSystem fs = FileSystem.get(job.getConfiguration());
        if(fs.exists(new Path(outputPath))) fs.delete(new Path(outputPath),true);
        FileOutputFormat.setOutputPath(job,new Path(outputPath));
        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception{
        System.exit(ToolRunner.run(new PartitionTest(),args));
    }
}
```  

测试数据：  

```
湖南
湖北
北京
上海
上海
上海
湖北
湖北
湖北
北京 
```  

测试数据put到hdfs上，然后将代码运行起来，最后得到的结果：  


![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hadoop/partition/1.png)    

可见最后生成了4个文件，每个文件存的是省份跟对应的count值。  