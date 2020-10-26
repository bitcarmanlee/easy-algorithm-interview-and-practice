
## 1.dataframe默认的列名
spark sql去读取文本生成dataframe时，如果该文本没有自带schema信息，默认的列名为_c0, _c1这种形式，我们可以看个例子。  

数据如下  

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

如果我们读取上述的csv文本然后生成dataframe， schema信息如下  

```
  @Test
  def parse2() = {
    val sparkConf = new SparkConf().setMaster("local[2]")
    sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    val spark = SparkSession.builder().config(sparkConf).getOrCreate()

    val path = "file:///Users/wanglei/wanglei/data/push/purchase/123"

    val df = spark.read
      .option("header", "false")
      .option("sep", "\t")
      .csv(path)

    df.printSchema()
  }
```  

最后输出为  

```
root
 |-- _c0: string (nullable = true)
 |-- _c1: string (nullable = true)
```  

文本默认两列的列名即为_c0, _c1。  

## 2.用withColumnRenamed重命名
实际开发过程中，我们一般会给各列一个名字，这样能方便我们后续开发。其中方法之一就可以使用withColumns方法。  

```
    val df = spark.read
      .option("header", "false")
      .option("sep", "\t")
      .csv(path)
      .withColumnRenamed("_c0", "appid")
      .withColumnRenamed("_c1", "brand")

    df.printSchema()
```  

withColumns方法每次重命名一列，当列比较多的时候，显然不是特别方便，此时可以使用后面的方法。  

## 3.toDF方法

```
    val df1 = spark.read
      .option("header", "false")
      .option("sep", "\t")
      .csv(path)
      .toDF("appid", "brand")
```  

toDF后面直接跟列名，就可以达到重命名的目的。  

toDF还有另外一种使用方法  

```
    val names = Seq("appid", "brand")
    val df = spark.read
      .option("header", "false")
      .option("sep", "\t")
      .csv(path)
      .toDF(names: _*)

    df.printSchema()
```  


其中，`_*`作为一个整体，告诉编译器你希望将某个参数当作参数序列处理。toDF的方法签名为`def toDF(colNames: String*)`，参数为可变长度的字符串序列，刚好`names: _*`就可以将seq当成一个参数序列来处理。  