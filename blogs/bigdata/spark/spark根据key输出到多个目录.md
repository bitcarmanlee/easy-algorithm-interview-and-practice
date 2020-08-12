项目中需要将spark的输出按id输出到不同的目录中，即实现在spark中的多路输出。我们可以调用saveAsHadoopFile函数并自定义一个OutputFormat类，就可以达到上述目的。  

```
import org.apache.commons.lang3.StringUtils
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.mapred.lib.MultipleTextOutputFormat
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Created by WangLei on 17-6-2.
  */
object genSpecifiedUserData {

    val inputPath = "xxx"

    def genData(sc:SparkContext) = {
        sc.textFile(inputPath)
            .filter(x => StringUtils.split(x, "\t").length == 7)
            .map(x => {
                val lines = StringUtils.split(x, "\t")
                val (id, aid, title, desc) = (lines(0), lines(1), lines(5), lines(6))
                (id, aid, title, desc)
            })
            .filter(x => StringUtils.isNotBlank(x._1))
            .map(x => {
                val (id, aid, title, desc) = (x._1, x._2, x._3, x._4)
                val pattern = Array(aid, title, desc).mkString("\t")
                (id, pattern)
            })
            .partitionBy(new org.apache.spark.HashPartitioner(10))
    }

    def main(args: Array[String]): Unit = {
        val sparkConf = new SparkConf().setAppName("gen_specified_user_data")
        sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        val sc = new SparkContext(sparkConf)
        
        val output = "/data/xxx/specified/"
        val fileSystem = FileSystem.get(sc.hadoopConfiguration)
        fileSystem.delete(new Path(output), true)
        findSpecifiedUser(sc).saveAsHadoopFile(
            output,
            classOf[String],
            classOf[String],
            classOf[RDDMultipleTextOutputFormat[_, _]])

        sc.stop()
    }
}

class RDDMultipleTextOutputFormat[K, V]() extends MultipleTextOutputFormat[K, V]() {
    override def generateFileNameForKeyValue(key: K, value: V, name: String) : String = {
        (key + "/" + name)
    }
}
```  

其中，输入的数据是以"\t"分隔一共七列，第一列为用户id。我们希望将输出的时候，相同的用户id输出到同一个目录下面，不同的用户id分开。  

RDDMultipleTextOutputFormat类中的generateFileNameForKeyValue函数有三个参数，key和value就是我们RDD的Key和Value，而name参数是每个Reduce的编号。上面的代码中没有使用该参数，而是直接将同一个Key的数据输出到同一个文件中。  

最后生成的结果在HDFS上为：  

```
/data/xxx/specified/idA/...
/data/xxx/specified/idB/...
/data/xxx/specified/idC/...
```