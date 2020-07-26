在MR中，类似于join类的操作非常常见。在关系型数据库中，join就是最强大的功能之一。在hive中，jion操作也十分常见。现在，本博主就手把手教会大家怎么在MR中实现join操作。为了方便起见，本文就以left join为视角来实现。  

## 1.数据准备
关于什么是join，什么是left join，本文就先不讨论了。先准备如下数据：  

```
cat employee.txt
jd,david
jd,mike
tb,mike
tb,lucifer
elong,xiaoming
elong,ali
tengxun,xiaoming
tengxun,lilei
xxx,aaa
```  

```
cat salary.txt
jd,1600
tb,1800
elong,2000
tengxun,2200
```  

然后将两个文件分别put到hdfs上面  

```
hadoop fs -put employee.txt /tmp/wanglei/employee/employee.txt
hadoop fs -put salary.txt /tmp/wanglei/salary/salary.txt
```  

我们想用employee左关联salary。至此，数据准备已经完毕。  

## 2.新建一个maven项目
新建一个maven项目，pom文件如下：  

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>

	<groupId>leilei.bit.edu</groupId>
	<artifactId>testjoin</artifactId>
	<version>1.0</version>
	<packaging>jar</packaging>

	<name>testjoin</name>
	<url>http://maven.apache.org</url>

	<properties>
		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
		<jarfile.name>testjoin</jarfile.name>
		<jar.out.dir>jar</jar.out.dir>
	</properties>

	<dependencies>
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.11</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.apache.hadoop</groupId>
			<artifactId>hadoop-common</artifactId>
			<version>2.5.0</version>
		</dependency>
		<dependency>
			<groupId>org.apache.hadoop</groupId>
			<artifactId>hadoop-mapreduce-client-core</artifactId>
			<version>2.5.0</version>
		</dependency>
		<dependency>
			<groupId>org.apache.mrunit</groupId>
			<artifactId>mrunit</artifactId>
			<version>1.0.0</version>
			<classifier>hadoop2</classifier>
		</dependency>
		<dependency>
			<groupId>org.anarres.lzo</groupId>
			<artifactId>lzo-hadoop</artifactId>
			<version>1.0.2</version>
		</dependency>
	</dependencies>

	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-jar-plugin</artifactId>
				<version>2.4</version>
				<configuration>
					<finalName>${jarfile.name}</finalName>
					<outputDirectory>${jar.out.dir}</outputDirectory>
				</configuration>
			</plugin>
			
			<plugin>
			
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<version>3.1</version>
				<configuration>
					<source>1.6</source>
					<target>1.6</target>
					<encoding>UTF-8</encoding>
					<descriptorRefs>
						<descriptorRef>jar-with-dependencies</descriptorRef>
					</descriptorRefs>
				</configuration>
			</plugin>
		</plugins>
	</build>

</project>

```  

然后开始实现left join的逻辑：  

```
package leilei.bit.edu.testjoin;

import java.io.IOException;
import java.util.Vector;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class LeftJoin extends Configured implements Tool{
	
	public static final String DELIMITER = ",";
	
	public static class LeftJoinMapper extends
		Mapper<LongWritable,Text,Text,Text> {
		
		protected void map(LongWritable key, Text value, Context context)
			throws IOException,InterruptedException {
			/*
			 * 拿到两个不同文件，区分出到底是哪个文件，然后分别输出
			 */
			String filepath = ((FileSplit)context.getInputSplit()).getPath().toString();
			String line = value.toString();
			if (line == null || line.equals("")) return; 
			
			if (filepath.indexOf("employee") != -1) {
				String[] lines = line.split(DELIMITER);
				if(lines.length < 2) return;
				
				String company_id = lines[0];
				String employee = lines[1];
				context.write(new Text(company_id),new Text("a:"+employee));
			}
			
			else if(filepath.indexOf("salary") != -1) {
				String[] lines = line.split(DELIMITER);
				if(lines.length < 2) return;
				
				String company_id = lines[0];
				String salary = lines[1];
				context.write(new Text(company_id), new Text("b:" + salary));
			}
		}
	}
	
	public static class LeftJoinReduce extends 
			Reducer<Text, Text, Text, Text> {
		protected void reduce(Text key, Iterable<Text> values,
				Context context) throws IOException, InterruptedException{
			Vector<String> vecA = new Vector<String>();
			Vector<String> vecB = new Vector<String>();
			
			for(Text each_val:values) {
				String each = each_val.toString();
				if(each.startsWith("a:")) {
					vecA.add(each.substring(2));
				} else if(each.startsWith("b:")) {
					vecB.add(each.substring(2));
				}
			}

			for (int i = 0; i < vecA.size(); i++) {
				/*
				 * 如果vecB为空的话，将A里的输出，B的位置补null。
				 */
				if (vecB.size() == 0) {
					context.write(key, new Text(vecA.get(i) + DELIMITER + "null"));
				} else {
					for (int j = 0; j < vecB.size(); j++) {
						context.write(key, new Text(vecA.get(i) + DELIMITER + vecB.get(j)));
					}
				}
			}
		}
	}
	
	public int run(String[] args) throws Exception {
		Configuration conf = getConf();
		GenericOptionsParser optionparser = new GenericOptionsParser(conf, args);
		conf = optionparser.getConfiguration();
		
		Job job = new Job(conf,"leftjoin");
		job.setJarByClass(LeftJoin.class);
		FileInputFormat.addInputPaths(job, conf.get("input_dir"));
		Path out = new Path(conf.get("output_dir"));
		FileOutputFormat.setOutputPath(job, out);
		job.setNumReduceTasks(conf.getInt("reduce_num",2));
				
		job.setMapperClass(LeftJoinMapper.class);
		job.setReducerClass(LeftJoinReduce.class);
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        conf.set("mapred.textoutputformat.separator", ",");
        
        return (job.waitForCompletion(true) ? 0 : 1);
	}
	
	public static void main(String[] args) throws Exception{
		int res = ToolRunner.run(new Configuration(),new LeftJoin(),args);
		System.exit(res);
	}

}

```  

稍微说一下处理逻辑：  
1.map阶段，把所有输入拆分为k,v形式。其中k是company_id，即我们要关联的字段。如果输入是employee相关的文件，那么map阶段的value加上标识符"a",表示是employee的输出。对于salary文件，加上标识符"b"。  
2.reduce阶段，将每个k下的value列表拆分为分别来自employee和salary的两部分，然后双层循环做笛卡尔积即可。  
3.注意的是，因为是left join，所以在reduce阶段，如果employee对应的company_id有，而salary没有，注意要输出此部分数据。  

## 3.打包
将上面的项目用maven打包，并上传到服务器上。  

## 4.使用shell脚本run起来
在服务器上写一个最简单的shell脚本，将代码run起来：  

```
vim run_join.sh

#!/bin/bash

output=/tmp/wanglei/leftjoin

if hadoop fs -test -d $output
then
    hadoop fs -rm -r $output
fi

hadoop jar testjoin.jar leilei.bit.edu.testjoin.LeftJoin \
    -Dinput_dir=/tmp/wanglei/employee,/tmp/wanglei/salary \
    -Doutput_dir=$output \
    -Dmapred.textoutputformat.separator=","
```  

执行此shell脚本：  

```
./run_join.sh
```  

## 5.最终输出
等job跑完以后，查看最终的输出结果：  

```
hadoop fs -cat /tmp/wanglei/leftjoin/*
elong,ali,2000
elong,xiaoming,2000
tengxun,lilei,2200
tengxun,xiaoming,2200
jd,mike,1600
jd,david,1600
tb,lucifer,1800
tb,mike,1800
xxx,aaa,null
```  

最终的输出结果，准确无误！至此，我们用mr完美实现了left join的功能！  