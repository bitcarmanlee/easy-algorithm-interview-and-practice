博主项目实践中，经常需要用spark从hbase中读取数据。其中，spark的版本为1.6，hbase的版本为0.98。现在记录一下如何在spark中操作读取hbase中的数据。  

对于这种操作型的需求，没有什么比直接上代码更简单明了的了。so，show me the code!  

```
object Demo extends Logging{

  val CF_FOR_FAMILY_USER = Bytes.toBytes("U");
  val CF_FOR_FAMILY_DEVICE = Bytes.toBytes("D")
  val QF_FOR_MODEL = Bytes.toBytes("model")
  val HBASE_CLUSTER = "hbase://xxx/"
  val TABLE_NAME = "xxx";
  val HBASE_TABLE = HBASE_CLUSTER + TABLE_NAME

  def genData(sc:SparkContext) = {
    //20161229的数据,rowkey的设计为9999-yyyyMMdd
    val filter_of_1229 = new RowFilter(CompareFilter.CompareOp.EQUAL, new SubstringComparator("79838770"))
    //得到qf为w:00-23的数据
    val filter_of_qf = new QualifierFilter(CompareFilter.CompareOp.EQUAL,new SubstringComparator("w"))

    val all_filters = new util.ArrayList[Filter]()
    all_filters.add(filter_of_1229)
    all_filters.add(filter_of_qf)

	//hbase多个过滤器
    val filterList = new FilterList(all_filters)

    val scan = new Scan().addFamily(CF_FOR_FAMILY_USER)
    scan.setFilter(filterList)
    scan.setCaching(1000)
    scan.setCacheBlocks(false)

    val conf = HBaseConfiguration.create()
    conf.set(TableInputFormat.INPUT_TABLE,HBASE_TABLE )
    conf.set(TableInputFormat.SCAN, Base64.encodeBytes(ProtobufUtil.toScan(scan).toByteArray()))
       sc.newAPIHadoopRDD(conf,classOf[TableInputFormat],classOf[ImmutableBytesWritable],classOf[Result])
    //后面是针对hbase查询结果的具体业务逻辑
    .map()
    ...

  def main(args: Array[String]): Unit = {
    val Array(output_path) = args

    val sparkConf = new SparkConf().setAppName("demo")
    sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    val sc = new SparkContext(sparkConf)

	genUuidWifi(sc).saveAsTextFile(output_path)
	sc.stop()
  }
}
```  

需要注意的一个小点就是如果hbase里有多个过滤器，注意需要使用FilterList。

