## 1.spark sql简介
spark sql是为了处理结构化数据的一个spark 模块。不同于spark rdd的基本API，spark sql接口更多关于数据结构本身与执行计划等更多信息。在spark内部，sql sql利用这些信息去更好地进行优化。有如下几种方式执行spark sql：SQL，DataFramesAPI与Datasets API。当相同的计算引擎被用来执行一个计算时，有不同的API和语言种类可供选择。这种统一性意味着开发人员可以来回轻松切换各种最熟悉的API来完成同一个计算工作。  

## 2.DataFrame
首先看看官网上对DataFrames的介绍：  
A DataFrame is a distributed collection of data organized into named columns. It is conceptually equivalent to a table in a relational database or a data frame in R/Python, but with richer optimizations under the hood. DataFrames can be constructed from a wide array of sources such as: structured data files, tables in Hive, external databases, or existing RDDs.  
The DataFrame API is available in Scala, Java, Python, and R.  

翻译一把  
DataFrame是一个以命名列方式组织的分布式数据集。在概念上，它跟关系型数据库中的一张表或者1个Python(或者R)中的data frame一样，但是比他们更优化。DataFrame可以根据结构化的数据文件、hive表、外部数据库或者已经存在的RDD构造。  
DataFrame可以使用的API包括Scala,Java,Python,R。  

## 3.起始点：SQLContext
spark sql所有功能的入口是SQLContext类，或者SQLContext的子类。为了创建一个基本的SQLContext，需要一个SparkContext。  
接下来我们所有的操作与实验都是在spark-shell里进行的。首先cd到spark的目录里，执行./bin/spark-shell，将spark-shell 跑起来。spark-shell启动过程中，会输出这么一行：  

```
Spark context available as sc.
```  
其实这就是告诉我们，spark-shell启动时候，已经帮我们初始化了一个可用的spark context并且叫sc。  

```
scala> val sqlContext = new org.apache.spark.sql.SQLContext(sc)
sqlContext: org.apache.spark.sql.SQLContext = org.apache.spark.sql.SQLContext@1943a343

scala> import sqlContext.implicits._
import sqlContext.implicits._
```  

## 4.创建DataFrames

```
val df = sqlContext.read.json("file:///data/wanglei/soft/spark-1.6.0-bin-hadoop2.4/examples/src/main/resources/people.json")
```  

吧啦吧啦输出一堆东西以后，最后一行：  

```
df: org.apache.spark.sql.DataFrame = [age: bigint, name: string]
```  
可以看到一个DataFrame已经生成！  

注意的是：  
官网上面这一行是这么写的：  

```
val df = sqlContext.read.json("examples/src/main/resources/people.json")
```  
根据代码猜测，这样写应该是读取本地相对路径的文件。但是不知道为什么，在我的环境里这么写不行，只能用file的方式指定绝对路径。或许是哪个配置项没有配正确。  

## 5.操作DataFrame
DataFrames提供了特定的语言来操作结构化数据，包括scala，java，python，R。  
下面我们来一些基本的操作  

```
scala> val sqlContext = new org.apache.spark.sql.SQLContext(sc)
sqlContext: org.apache.spark.sql.SQLContext = org.apache.spark.sql.SQLContext@1943a343

scala> import sqlContext.implicits._
import sqlContext.implicits._

// Show the content of the DataFrame
df.show()
// age  name
// null Michael
// 30   Andy
// 19   Justin

// Print the schema in a tree format
df.printSchema()
// root
// |-- age: long (nullable = true)
// |-- name: string (nullable = true)

// Select only the "name" column
df.select("name").show()
// name
// Michael
// Andy
// Justin

// Select everybody, but increment the age by 1
df.select(df("name"), df("age") + 1).show()
// name    (age + 1)
// Michael null
// Andy    31
// Justin  20

// Select people older than 21
df.filter(df("age") > 21).show()
// age name
// 30  Andy

// Count people by age
df.groupBy("age").count().show()
// age  count
// null 1
// 19   1
// 30   1
```  

## 6.根据反射推断schema
Spark SQL的Scala接口支持将包括case class数据的RDD转换成DataFrame。  
case class定义表的schema，case class的属性会被读取并且成为列的名字，这里case class也可以被当成别的case class的属性或者是复杂的类型，比如Sequence或Array。RDD会被隐式转换成DataFrame并且被注册成一个表，这个表可以被用在查询语句中。  

```
// sc is an existing SparkContext.
val sqlContext = new org.apache.spark.sql.SQLContext(sc)
// this is used to implicitly convert an RDD to a DataFrame.
import sqlContext.implicits._

// Define the schema using a case class.
// Note: Case classes in Scala 2.10 can support only up to 22 fields. To work around this limit,
// you can use custom classes that implement the Product interface.
case class Person(name: String, age: Int)

// Create an RDD of Person objects and register it as a table.
scala> val people = sc.textFile("file:///data/wanglei/soft/spark-1.6.0-bin-hadoop2.4/examples/src/main/resources/people.txt").map(_.split(",")).map(p => Person(p(0), p(1).trim.toInt)).toDF()
//执行完毕以后，最后一行会输出如下：
//people: org.apache.spark.sql.DataFrame = [name: string, age: int]
people.registerTempTable("people")

// SQL statements can be run by using the sql methods provided by sqlContext.
val teenagers = sqlContext.sql("SELECT name, age FROM people WHERE age >= 13 AND age <= 19")

// The results of SQL queries are DataFrames and support all the normal RDD operations.
// The columns of a row in the result can be accessed by field index:
teenagers.map(t => "Name: " + t(0)).collect().foreach(println)

// or by field name:
teenagers.map(t => "Name: " + t.getAs[String]("name")).collect().foreach(println)

// row.getValuesMap[T] retrieves multiple columns at once into a Map[String, T]
teenagers.map(_.getValuesMap[Any](List("name", "age"))).collect().foreach(println)
// Map("name" -> "Justin", "age" -> 19)
```  

## 7.使用Programmatically的方式指定Schema
当case class不能提前确定（例如，记录的结构是经过编码的字符串，或者一个文本集合将会被解析，不同的字段投影给不同的用户），一个 DataFrame 可以通过三步来创建。  
1.从原来的 RDD 创建一个行的 RDD  
2.创建由一个 StructType 表示的模式与第一步创建的 RDD 的行结构相匹配  
3.在行 RDD 上通过 applySchema 方法应用模式  

```
// Create an RDD
scala> val people = sc.textFile("file:///data/wanglei/soft/spark-1.6.0-bin-hadoop2.4/examples/src/main/resources/people.txt")

// The schema is encoded in a string
val schemaString = "name age"

// Import Row.
import org.apache.spark.sql.Row;

// Import Spark SQL data types
import org.apache.spark.sql.types.{StructType,StructField,StringType};

// Generate the schema based on the string of schema
val schema =
  StructType(
    schemaString.split(" ").map(fieldName => StructField(fieldName, StringType, true)))

// Convert records of the RDD (people) to Rows.
val rowRDD = people.map(_.split(",")).map(p => Row(p(0), p(1).trim))

// Apply the schema to the RDD.
val peopleDataFrame = sqlContext.createDataFrame(rowRDD, schema)

// Register the DataFrames as a table.
peopleDataFrame.registerTempTable("people")

// SQL statements can be run by using the sql methods provided by sqlContext.
val results = sqlContext.sql("SELECT name FROM people")

// The results of SQL queries are DataFrames and support all the normal RDD operations.
// The columns of a row in the result can be accessed by field index or by field name.
results.map(t => "Name: " + t(0)).collect().foreach(println)
```  

## 8.spark sql整体文档结构
最后给大家截个图，可以清晰看到spark sql的整体文档结构  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/spark/sparkintellij/7.png)    
