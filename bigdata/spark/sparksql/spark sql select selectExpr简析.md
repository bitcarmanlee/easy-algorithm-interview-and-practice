## 1.select方法
dataframe的select方法，最简单的使用方式为直接选择对应的列名。  

测试数据如下  
```
101	brand1
101	brand2
101	brand3
102	brand1
102	brand3
102	brand3
102	brand4
103	brand2
103	brand2
103	brand2
103	brand5
103	brand5
```  

```
  def parse() = {
    val sparkConf = new SparkConf().setMaster("local[2]")
    sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    val spark = SparkSession.builder().config(sparkConf).getOrCreate()

    val path = "xxx"

    val df = spark.read
      .option("header", "false")
      .option("sep", "\t")
      .csv(path)
      .toDF("appid", "brand")

    df.select("appid").show()
}
```  
上面的代码会选择appid这一列。  

如果是  

```
df.select("*")
```  
则会选中所有列  


```
df.select(expr("appid as newappid")).show()
```  

select方法还可以传入org.apache.spark.sql.functions中的expr方法，expr方法会将方法中的字符串解析成对应的sql语句并执行，上面的例子就是选中appid这一列，并将appid这一列重命名为newappid。  


```
df.select(col("appid")+1).show()
```  

上面的代码中，在select函数中传入了org.apache.spark.sql.functions的col方法(column方法效果同上)，col("appid")+1就实现了对appid列加1的效果。  

```
df.select($"appid" + 1).show()
```  

这行代码与上面的代码达到同样的效果，也是对appid列进行了加1操作。`$`符号需要`import spark.implicits._`，源码如下  

```
  implicit class StringToColumn(val sc: StringContext) {
    def $(args: Any*): ColumnName = {
      new ColumnName(sc.s(args: _*))
    }
  }
```  

本质就是将`$`符后面的字符串变成了一个Column对象。  

select方法中还可以输入聚合函数，例如  

```
df.select(avg("appid")).show()
```  

上面的代码就是对appid求平均值。  

## 2.selectExpr方法
selectExpr方法本质与select方法中使用expr函数是一样的，都是用来构建复杂的表达式，下面我们可以看几个例子。  

```
df.selectExpr("appid as newappid").show()
```  

上面这行代码，就是选择appid列并将appid重命名为newappid。  

```
df.selectExpr("count(distinct(appid)) as count1", "count(distinct(brand)) as count2").show()
```  

上面这行代码，就是计算appid去重后的数量，还有brand去重后的数量。  

## 3.总结
从上面总结的用法来看，select与selectExpr并没有本质区别，关键还是看使用习惯。  