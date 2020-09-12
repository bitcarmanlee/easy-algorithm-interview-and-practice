## 1.MultiPleOutputs简介

MapReduce job中，可以使用FileInputFormat和FileOutputFormat来对输入路径和输出路径来进行设置。在输出的时候，MR内部会对输出的文件进行重新命名，例如常见的形式为part-r-00000。  

但是很多情况下，我们希望将输出的文件分开，即所谓的多路输出。我们希望将输出的内容重新组织，输出到不同的目录或者文件夹中，方便我们后续进一步的处理。否则，我们还需要在job完成以后，再来编写相应的脚本进行相关的文本处理，这样就耗时耗力非常不方便。  

想要在MR中实现多路输出，MultiPleOutputs就能很好地帮助我们完成这个目标。  

## 2.能正常运行的代码
首先准备测试数据。  

```
1512,iphone5s,4inchs,A7,64,M7,lowerpower
1512,iphone5,4inchs,A6,IOS7
1512,iphone4s,3.5inchs,A5
50019780,Ipad,9.7,retina
50019780,yoga,lenovel,18hours
50019780,nexus,7,google
50019780,Ipad mini2,retina,7.9
1101,macbook air,OS X mavericks
1101,macbook pro,OS X lion
1101,thinkpad yoga,lenovel,windows 8
```  

我们想将相同id的数据输入到同一个文件中，将不同id的数据分开。  
二话不说，直接上源码  

```
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.LazyOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.MultipleOutputs;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;

/**
 * @author WangLei
 * @since 17-2-4
 */
public class MultiOutput extends Configured implements Tool{

    public static class MultiMapper extends Mapper<LongWritable,Text,Text,Text> {

        @Override
        protected void map(LongWritable key,Text value,Context context) throws IOException,InterruptedException {
            String line = value.toString().trim();
            if(line.length() > 0) {
                String[] lines = line.split(",");
                context.write(new Text(lines[0]),value);
            }
        }
    }

    public static class MultiReducer extends Reducer<Text,Text,NullWritable,Text> {
        //设置多文件输出
        private MultipleOutputs<NullWritable,Text> mos;

        @Override
        protected void setup(Context context) throws IOException,InterruptedException {
            mos = new MultipleOutputs<NullWritable,Text>(context);
        }

        @Override
        protected void cleanup(Context context) throws IOException,InterruptedException {
            //注意要调用close方法，否则会没有输出
            mos.close();
        }

        @Override
        protected void reduce(Text key,Iterable<Text> values,Context context) throws IOException,InterruptedException {
            for(Text value:values) {
                //指定写出不同文件的数据
                mos.write("BaseOnKey",NullWritable.get(),value,key.toString() + "/" + key.toString());
                //指定写出全部数据
                mos.write("All",NullWritable.get(),value);
            }
        }
    }

    public int run(String[] args) throws Exception{
        Configuration conf = new Configuration();
        Job job = new Job(conf);
        job.setJarByClass(MultiOutput.class);

        job.setMapperClass(MultiMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setReducerClass(MultiReducer.class);
        job.setOutputKeyClass(NullWritable.class);
        job.setOutputValueClass(Text.class);

        //BaseOnKey的输出
        MultipleOutputs.addNamedOutput(job,"BaseOnKey",TextOutputFormat.class,NullWritable.class,Text.class);
        //没有区分的所有输出
        MultipleOutputs.addNamedOutput(job,"All",TextOutputFormat.class,NullWritable.class,Text.class);

        job.setInputFormatClass(TextInputFormat.class);
        //取消part-r-00000新式文件输出
        LazyOutputFormat.setOutputFormatClass(job,TextOutputFormat.class);

        FileInputFormat.addInputPath(job,new Path(args[0]));
        Path outputPath = new Path(args[1]);
        FileSystem fs = FileSystem.get(job.getConfiguration());
        if(fs.exists(outputPath)) fs.delete(outputPath,true);
        FileOutputFormat.setOutputPath(job,outputPath);

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception{
        System.exit(ToolRunner.run(new MultiOutput(),args));
    }
}
```  

## 3.几个注意事项
应该注意的地方其实在代码的注释中已经写得相当详细了。这里再拎出来啰嗦一下。  
1.例子中reduce阶段输出是，先设置多文件输出mos。  
2.在cleanup方法中，需要调用mos的close方法，否则最后的输出为空。  
3.`LazyOutputFormat.setOutputFormatClass(job,TextOutputFormat.class);` 这一行是为了取消part-r-00000形式的文件输出。否则最终的输出目录中还会有空的part-r-00000输出。  