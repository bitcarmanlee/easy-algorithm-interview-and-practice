关于hive的udf介绍，就不多啰嗦了。网上的教程一抓一大把，也可以上apache的官网去查阅相关资料，我就省了翻译的时间了。重点给大家带来干货，手把手教会你怎样开发一个udf函数，已经如何部署到服务器上的hive环境中运行。用最简单的话来说，就是教大家怎么让自己开发的udf跑起来。。。  

## 1.项目需求
做数据挖掘项目中，常见的需求之一就是分析节假日订单跟平时订单的区别。于是，我们需要统计节假日订单的分布情况。但是hive中显然没有内置，也不可能内置此函数，因为每年的节假日都是变得嘛。于是，我们就需要自己开发一个udf来满足需求了。  

## 2.配置文件
考虑到每年的节假日其实并不多，也就那么二十多天，于是采用配置文件的方式，直接将节假日写死在配置文件中。如果需要添加，改配置文件就行。毕竟一年也就这么二十多天，工作量并不大。。。
  
自己写的配置文件如下：    

```
20140101=元旦
20140131=春节
20140201=春节
20140202=春节
20140203=春节
20140204=春节
20140205=春节
20140206=春节
20140405=清明节
20140406=清明节
20140407=清明节
20140501=五一劳动节
20140502=五一劳动节
20140503=五一劳动节
20140531=端午节
20140601=端午节
20140602=端午节
20140906=中秋节
20140907=中秋节
20140908=中秋节
20141001=国庆节
20141002=国庆节
20141003=国庆节
20141004=国庆节
20141005=国庆节
20141006=国庆节
20141007=国庆节

20150101=元旦
20150102=元旦
20150103=元旦
20150218=春节
20150219=春节
20150220=春节
20150221=春节
20150222=春节
20150223=春节
20150224=春节
20150404=清明节
20150405=清明节
20150406=清明节
20150501=五一劳动节
20150502=五一劳动节
20150503=五一劳动节
20150620=端午节
20150621=端午节
20150622=端午节
20150926=中秋节
20150927=中秋节
20151001=国庆节
20151002=国庆节
20151003=国庆节
20151004=国庆节
20151005=国庆节
20151006=国庆节
20151007=国庆节

20160101=元旦
20160102=元旦
20160103=元旦
20160207=春节
20160208=春节
20160209=春节
20160210=春节
20160211=春节
20160212=春节
20160213=春节
20160402=清明节
20160403=清明节
20160404=清明节
20160430=五一劳动节
20160501=五一劳动节
20160502=五一劳动节
20160609=端午节
20160610=端午节
20160611=端午节
20160915=中秋节
20160916=中秋节
20160917=中秋节
20161001=国庆节
20161002=国庆节
20161003=国庆节
20161004=国庆节
20161005=国庆节
20161006=国庆节
20161007=国庆节
```  

以上包含有2014，2015，2016三年的假期。如果想增加，继续往此文件里添加就是。。。  

## 3.新建maven项目
现在的java项目必须是用maven管理，方便又实用，谁用谁知道，不多解释。maven项目自然只需要知道pom.xml即可。pom文件如下：  

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>udf.leilei.elong.com</groupId>
  <artifactId>festival</artifactId>
  <version>1.0</version>
  
  <name>hive</name>
  <url>http://maven.apache.org</url>
  
  <properties>
  	<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
  
  <dependencies>
  	<dependency>
  		<groupId>org.apache.hive</groupId>
  		<artifactId>hive-exec</artifactId>
  		<version>0.13.0</version>
  	</dependency>
  	<dependency>
  		<groupId>org.apache.hadoop</groupId>
  		<artifactId>hadoop-common</artifactId>
  		<version>2.5.0</version>
  	</dependency>
  </dependencies>
  <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>2.2</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
 </build>
</project>
```  

提醒对maven不是很熟的同学们：因为我们项目里有依赖的jar包，所以必须加上 maven-shade-plugin 插件。当然你用 maven-assembly-plugin 也是没有问题的。如果你对maven不是那么熟悉，别管了，先粘过去，跑起来再说吧。。。  

## 4.UDF具体代码开发

```
package festival;

import java.io.InputStreamReader;
import java.text.NumberFormat;
import java.util.HashMap;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.hive.ql.exec.UDF;

public class FestivalType extends UDF{

	private HashMap<String,String> festivalMap = new HashMap<String, String>();
	
	public FestivalType() throws Exception {
		InputStreamReader propFile = new InputStreamReader(getClass().getClassLoader().getResourceAsStream("festival_date.properties"), "UTF-8");
		Properties prop = new Properties();
		prop.load(propFile);
		for(Object key:prop.keySet()) {
			festivalMap.put(key.toString(), prop.getProperty(key.toString()));
		}
	}
	
	//解决double转string的科学计数法的问题
	public String double_to_string(double dou) {
		Double dou_obj = new Double(dou);
		NumberFormat nf = NumberFormat.getInstance();
		nf.setGroupingUsed(false);
		String dou_str = nf.format(dou_obj);
		return dou_str;
	}
	
	public String evaluate(double date_dou) {
		String date_str = this.double_to_string(date_dou);
		return evaluate(date_str);
	}
	
	public int evaluate(double date_dou,String flag) {
		String date_str = this.double_to_string(date_dou);
		return evaluate(date_str,flag);
	}
	
	public String evaluate(String date_str) {
		if (! this.match_date(date_str).equals("null")) {
			date_str = this.match_date(date_str);
			return festivalMap.get(date_str) == null ? "null" : festivalMap.get(date_str);
		} else {
			return "null";
		}
	}
	
	public int evaluate(String date_str, String flag) {
		if (flag.equals("count") && ! this.match_date(date_str).equals("null")) {
			date_str = this.match_date(date_str);
			return festivalMap.get(date_str) == null ? 0 :1;
		} else {
			return 0;
		}
	}
	
	public String match_date(String date_str) {
		//匹配20160101这种日期格式
		Pattern pat_common = Pattern.compile("\\d{8}");
		Matcher mat_common = pat_common.matcher(date_str);
		
		//匹配2016-01-01这种日期格式
		Pattern pat_strike = Pattern.compile("\\d{4}-\\d{2}-\\d{2}");
		Matcher mat_strike = pat_strike.matcher(date_str);
		
		//匹配 2016-01-01 10:35:46 这种日期格式
		Pattern pat_colon = Pattern.compile("\\d{4}-\\d{2}-\\d{2}(\\s)+\\d{2}:\\d{2}:\\d{2}");
		Matcher mat_colon = pat_colon.matcher(date_str);
		
		if (mat_colon.find()) {
			return date_str.replace("-", "").substring(0, 8);
		} else if(mat_strike.find()) {
			return date_str.replace("-", "");
		} else if (mat_common.find()) { 
			return date_str;
		} else {
			return "null";
		}
	}

	//测试的main方法
	public static void main(String[] args) throws Exception{
		FestivalType fes = new FestivalType();
		String date_str = "20150101";
		System.out.println(fes.evaluate(date_str));
		
		String date_str1 = "20160101";
		String result = fes.evaluate(date_str1);
		System.out.println("result is:" + result);
		
		double date_dou = 20160101;
		int result_dou = fes.evaluate(date_dou,"count");
		System.out.println(result_dou);
		System.out.println(date_dou);
	}
}

```  

将之前的配置文件放在src/main/resources下面，然后运行此代码，输出如下：  

```
节日类型是:元旦
节日天数:1
```  

因为我们这篇文章的目的是让udf以最快的速度跑起来，所以udf具体实现细节以及原理就不多写了。大家记住下面一句话就可以：继承UDF类，重写evaluate方法，就可以了。  

## 5.maven打包
上面代码测试通过以后，然后用maven打成jar包。如果是老司机，自然知道怎么做。如果是新司机，我偷偷告诉大家，eclipse里在项目上右击，选择 run as，然后maven install，maven就开始帮你打包了。如果是第一次，maven还会帮你把依赖的jar下载到本地仓库。打包完了以后，你就可以看到target目录下面出现了一个jar包，festival-1.0.jar。OK，这就是我们需要的jar包。  

## 6.将jar包上传
接下来，我们将前面的jar包上传到服务器上的任何一个位置。比如我就是用scp命令，不多说。  

## 7.使用udf查询

```
#!/bin/bash

hive -e "add jar /home/xxx/lei.wang/festival-1.0.jar;
         create temporary function festival as 'festival.FestivalType';
         set mapred.reduce.tasks = 10;
         select cast(a.create_date_wid as int) create_date_wid,sum(a.festival_order_num) from
            (select create_date_wid,festival(create_date_wid,'count') as festival_order_num from ora_dw_rewrite.olap_b_dw_hotelorder_f
                where create_date_wid>=20160101 and create_date_wid<=20160406)a
            where a.festival_order_num > 0
                group by a.create_date_wid
                    order by create_date_wid;"
```  

为了达到快速上手的目的，直接上代码。  

```
add jar /home/xxx/lei.wang/festival-1.0.jar;
```  

这一行是将jar包加进来，后面是你前面上传的路径地址  

```
create temporary function festival as 'festival.FestivalType';
```  

创建一个临时函数，用来查询，festival.FestivalType是package名+类名，无需多解释。  
后面的查询语句，也不多解释了。有点sql基础的同学，应该都能看明白。  

最后查询结果  

```
..........
Stage-Stage-1: Map: 62  Reduce: 10   Cumulative CPU: 1547.44 sec   HDFS Read: 29040366442 HDFS Write: 1298 SUCCESS
Stage-Stage-2: Map: 8  Reduce: 1   Cumulative CPU: 23.88 sec   HDFS Read: 4608 HDFS Write: 205 SUCCESS
Total MapReduce CPU Time Spent: 26 minutes 11 seconds 320 msec
OK
20160101	xxx
20160102	xxx
20160103	xxx
20160207	xxx
20160208	xxx
20160209	xxx
20160210	xxx
20160211	xxx
20160212	xxx
20160213	xxx
20160402	xxx
20160403	xxx
20160404	xxx
Time taken: 159.805 seconds, Fetched: 13 row(s)
```  

后面的具体数值是公司机密，不能透露，嘻嘻。  
稍微注意一点是`cast(a.create_date_wid as int) `，这里因为create_date_wid存的是double类型，如果不做转化的话，会显示成科学计数法，`2.0150326E7`这种形式。所以为了好看一些，将其强转成int类型。  

还有就是这种add的方式的有效期是session级别，就是在此seession有效，session关闭以后就无效。所以如果要将其固话的话，可以加到hive的classpath里头。这样hive启动的时候，就将其加到classpath里了，无需再手动add jar。  

## 8.结束语
至此，一个完整的hive udf开发过程就结束了。当然还可以开发UDAF，限于时间有限，就不再详细介绍。欢迎有搞数据，算法的志同道合的同学们一起研究讨论  
