## 1.ALS简介
在前面相关的文章中，已经详细介绍了ALS的原理。用最简单的一句话总结就是：ALS是通过将user与item分别表示为一个低维稠密向量来进行后续的使用。

## 2.基于spark的ALS实现
首先看一部分辅助代码  

```
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Set;
import java.util.TreeSet;

/**
 * Created by WangLei on 20-1-10.
 */
public class TimeUtils {

    private static final Logger LOGGER = LoggerFactory.getLogger(TimeUtils.class);

    public static final String DATE_FORMAT = "yyyyMMdd";
    public static final String TIME_FORMAT = "yyyyMMdd HH:mm:ss";
    public static final String HOUR_TIME_FORMAT = "yyyyMMdd HH";

    public static final long TIME_DAY_MILLISECOND = 86400000;

    /**
     * timestamp -> ymd
     * @param timestamp
     * @return
     */
    public static String timestamp2Ymd(long timestamp) {
        String format = "yyyyMMdd";
        return timestamp2Ymd(timestamp, format);
    }

    public static String timestamp2Ymd(long timestamp, String format) {
        SimpleDateFormat sdf;
        try {
            //支持输入10位的时间戳
            if(String.valueOf(timestamp).length() == 10) {
                timestamp *= 1000;
            }
            sdf = new SimpleDateFormat(format);
            return sdf.format(new Date(timestamp));
        } catch(Exception ex) {
            sdf = new SimpleDateFormat(DATE_FORMAT);
            try {
                return sdf.format(new Date(timestamp));
            } catch (Exception e){}
        }
        return null;
    }

    public static String timestamp2Hour(long timestamp) {
        String time = timestamp2Ymd(timestamp, TIME_FORMAT);
        return time.substring(9, 11);
    }

    /**
     * ymd -> Date
     * @param ymd
     * @return
     */
    public static Date ymd2Date(String ymd) {
        return ymd2Date(ymd, "yyyyMMdd");
    }

    public static Date ymd2Date(String ymd, String format) {
        try {
            SimpleDateFormat sdf = new SimpleDateFormat(format);
            return sdf.parse(ymd);
        } catch(ParseException ex) {
            LOGGER.error("parse ymd to timestamp error!", ex);
        } catch (Exception ex) {
            LOGGER.error("there is some problem when transfer ymd2Date!", ex);
        }
        return null;
    }

    /**
     * ymd -> timestamp
     * @param ymd
     * @return
     */
    public static long ymd2timestamp(String ymd) {
        return ymd2Date(ymd).getTime();
    }


    public static String genLastDayStr() {
        return timestamp2Ymd(System.currentTimeMillis() + TIME_DAY_MILLISECOND * (-1));
    }


    /**
     * get the datestr before or after the given datestr
     * attention transfer the num from int to long
     * @param ymd
     * @param num
     * @return
     */
    public static String genDateAfterInterval(String ymd, int num) {
        long timestamp = ymd2timestamp(ymd);
        long resTimeStamp = timestamp + TIME_DAY_MILLISECOND * Long.valueOf(num);
        return timestamp2Ymd(resTimeStamp);
    }

    public static String genLastDayStr(String ymd) {
        return genDateAfterInterval(ymd, -1);
    }


    public static Set<String> genYmdSet(long beginTs, long endTs) {
        TreeSet ymdSet = new TreeSet();
        for(long ts = beginTs; ts <= endTs; ts += 86400000L) {
            ymdSet.add(timestamp2Ymd(ts));
        }
        return ymdSet;
    }

    public static Set<String> genYmdSet(String beginYmd, String endYmd) {
        long beginTs = ymd2timestamp(beginYmd);
        long endTs = ymd2timestamp(endYmd);
        return genYmdSet(beginTs, endTs);
    }

    /**
     * end between begin days
     * if begin or end is not number format or end < begin, return Integer.MIN_VALUE
     * @param begin
     * @param end
     * @return
     */
    public static int getIntervalBetweenTwoDays(String begin, String end) {
        try {
            int begintmp = Integer.valueOf(begin), endtmp = Integer.valueOf(end);
            if(begintmp > endtmp) {
                LOGGER.error("we need end no smaller than end!");
                return Integer.MIN_VALUE;
            }
            Date d1 = ymd2Date(begin);
            Date d2 = ymd2Date(end);
            Long mils = (d2.getTime() - d1.getTime()) / TIME_DAY_MILLISECOND;
            return mils.intValue();
        } catch (NumberFormatException numformatex) {
            numformatex.printStackTrace();
            return Integer.MIN_VALUE;
        }
    }
}
```

里面包含了很多时间的处理方法，可以直接加入代码库。

```
/**
  * Created by WangLei on 20-1-13.
  */
object DateSpec extends Enumeration {
    type DateSpec = Value

    val YMD , Y_M_D, YMD2 = Value
}
```


HDFS相关的工具类

```
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.SparkContext
import org.joda.time.DateTime

/**
  * Created by WangLei on 20-1-10.
  */
object HDFSUtils {

    val conf = new Configuration()

    def delete(sc: SparkContext, path: String) = {
        FileSystem.get(sc.hadoopConfiguration).delete(new Path(path), true)
    }

    def isExist(sc: SparkContext, path: String) = {
        FileSystem.get(sc.hadoopConfiguration).exists(new Path(path))
    }

    def checkFileExist(conf: Configuration = conf, FileName: String): Boolean = {
        var isExist = false

        try {
            val hdfs = FileSystem.get(conf)
            val path = new Path(FileName)
            isExist = hdfs.exists(path)
        } catch {
            case e: Exception => e.printStackTrace()
        }

        isExist
    }

    def latestMidPath(conf: Configuration, basePath: String): Option[String] = {
        val today = new Date
        latestMidPath(conf, basePath, new DateTime(today.getTime), 7)
    }

    def latestMidPath(conf: Configuration, basePath: String, ymd: String) : Option[String] = {
        val timestamp = TimeUtils.ymd2timestamp(ymd)
        latestMidPath(conf, basePath, new DateTime(timestamp), 7, false, DateSpec.YMD2)
    }

    def latestMidPath(conf: Configuration = conf, basePath: String, date: DateTime, limit: Int,with_success_file:Boolean = true,dateSpec: DateSpec = DateSpec.YMD): Option[String] = {
        for (i <- 0 to limit) {
            val day = date.minusDays(i)
            val path = dateSpec match {
                case DateSpec.YMD => basePath + "/date=%04d%02d%02d".format(day.getYear, day.getMonthOfYear, day.getDayOfMonth)
                case DateSpec.Y_M_D => basePath + "/year=%04d/month=%02d/day=%02d".format(day.getYear, day.getMonthOfYear, day.getDayOfMonth)
                case DateSpec.YMD2 => basePath + "/%04d%02d%02d".format(day.getYear, day.getMonthOfYear, day.getDayOfMonth)
            }

            if (checkFileExist(conf, if(with_success_file) path + "/_SUCCESS" else path))
                return Some(path)
        }
        None
    }

}
```  


ALS训练相关代码  

```
import org.apache.spark.SparkConf
import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.recommendation.ALS
import org.apache.spark.sql.SparkSession
import org.slf4j.LoggerFactory

import scala.collection.JavaConversions._

object AlsTraining {
	
	val logger = LoggerFactory.getLogger(this.getClass)
	val separator = "\t"
	
	def genUserItemRdd(spark: SparkSession, ymd: String) = {
		val baseinput = PathUtils.user_item_click_path
		val (yesterday, daybegin) = (TimeUtils.genLastDayStr(ymd), TimeUtils.genDateAfterInterval(ymd, -29))
		val days = TimeUtils.genYmdSet(daybegin, yesterday)
		
		// userid itemid clicknum
		var rdd = spark.sparkContext.textFile(baseinput + ymd)
			.map(x => {
				val l = x.split("\t")
				(l(0), l(1), l(2))
			})
		
		for (day <- days) {
			val path = baseinput + day
			if (HDFSUtils.isExist(spark.sparkContext, path)) {
				val tmp = spark.sparkContext.textFile(path)
					.map(x => {
						val l = x.split("\t")
						(l(0), l(1), l(2))
					})
				rdd = rdd.union(tmp)
			}
		}
		rdd.cache
	}
	
	def genUserItemIndex(spark: SparkSession, ymd: String) = {
		val rdd = genUserItemRdd(spark, ymd)
		val userindex = rdd.map(x => x._1).distinct().sortBy(x => x).zipWithIndex().map(x => (x._1, x._2 + 1))
		val itemindex = rdd.map(x => x._2).distinct().sortBy(x => x).zipWithIndex().map(x => (x._1, x._2 + 1))
		
		(userindex, itemindex)
	}
	
	case class Rating(userid: Int, itemid: Int, rating: Float)
	
	def trainmodel(spark: SparkSession, ymd: String) = {
		import spark.implicits._
		
		val rdd = genUserItemRdd(spark, ymd)
		
		val userindexrdd = rdd.map(x => x._1).distinct().sortBy(x => x).zipWithIndex().map(x => (x._1, x._2 + 1))
		val itemindexrdd = rdd.map(x => x._2).distinct().sortBy(x => x).zipWithIndex().map(x => (x._1, x._2 + 1))
		
		val data = rdd.map(x => {
			val (userid, itemid, count) = (x._1, x._2, x._3.toInt)
			(userid + separator + itemid, count)
		})
			.reduceByKey(_ + _)
			.map(x => {
				val (userid, itemid, count) = (x._1.split(separator)(0), x._1.split(separator)(1), x._2)
				(userid, itemid + separator + count)
			})
			.join(userindexrdd)
			.map(x => {
				val (itemandcount, userindex) = (x._2._1, x._2._2)
				val (itemid, count) = (itemandcount.split(separator)(0), itemandcount.split(separator)(1))
				(itemid, userindex + separator + count)
			})
			.join(itemindexrdd)
			.map(x => {
				val (userandcount, itemindex) = (x._2._1, x._2._2)
				val (userindex, count) = (userandcount.split(separator)(0), userandcount.split(separator)(1))
				Rating(userindex.toInt, itemindex.toInt, count.toFloat)
			}).toDF()
		
		val Array(training, test) = data.randomSplit(Array(0.8, 0.2))
		val als = new ALS().setRank(128).setMaxIter(8).setRegParam(0.01).
			setUserCol("userid").setItemCol("itemid").setRatingCol("rating")
		val model = als.fit(training)
		
		model.setColdStartStrategy("drop")
		
		val predictions = model.transform(test)
		val evaluator = new RegressionEvaluator()
			.setMetricName("rmse")
			.setLabelCol("rating")
			.setPredictionCol("prediction")
		val rmse = evaluator.evaluate(predictions)
		
		logger.error("root-mean-square error is: {}", rmse)
		
		val userindex2userid = userindexrdd.map(x => (x._2, x._1))
		val userfactors = model.userFactors.rdd.map(x => {
			val (userid, userfactor) = (x.getInt(0).toLong, x.getList(1).toArray().mkString(","))
			(userid, userfactor)
		}).join(userindex2userid)
    		.map(x => {
				val (userindex, userfactor, userid) = (x._1, x._2._1, x._2._2)
				(userindex, userid, userfactor)
			})
    		.repartition(1)
    		.sortBy(x => x._1)
    		.map(x => "%s\t%s\t%s".format(x._1, x._2, x._3))
		
		val itemindex2itemid = itemindexrdd.map(x => (x._2, x._1))
		val itemfactors = model.itemFactors.rdd.map(x => {
			val (itemid, itemfactor) = (x.getInt(0).toLong, x.getList(1).toArray().mkString(","))
			(itemid, itemfactor)
		}).join(itemindex2itemid)
    		.map(x => {
				val (itemindex, itemfactor, itemid) = (x._1, x._2._1, x._2._2)
				(itemindex, itemid, itemfactor)
			})
    		.repartition(1)
    		.sortBy(x => x._1)
			.map(x => "%s\t%s\t%s".format(x._1, x._2, x._3))
		
		(userfactors, itemfactors)
	}
	
	def main(args: Array[String]): Unit = {
		val (ymd, operation) = (args(0), args(1))
		val sparkConf = new SparkConf()
		sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
		sparkConf.setAppName("user-item-als-training" + ymd)
		
		val spark = SparkSession.builder().config(sparkConf).getOrCreate()
		
		operation match {
			case "index" => {
				val useroutput = PathUtils.user_index_path + ymd
				val itemoutput = PathUtils.item_index_path + ymd
				val (userindex, itemindex) = genUserItemIndex(spark, ymd)
				userindex.repartition(1).sortBy(_._2).map(x => "%s\t%s".format(x._2, x._2)).saveAsTextFile(useroutput)
				itemindex.repartition(1).sortBy(_._2).map(x => "%s\t%s".format(x._2, x._2)).saveAsTextFile(itemoutput)
			}
			case "model" => {
				val (userfactors, itemfactors) = trainmodel(spark, ymd)
				val user_embedding_path = PathUtils.user_factor_path + ymd
				val item_embedding_path = PathUtils.item_factor_path + ymd
				HDFSUtils.delete(spark.sparkContext, user_embedding_path)
				HDFSUtils.delete(spark.sparkContext, item_embedding_path)
				
				userfactors.saveAsTextFile(user_embedding_path)
				itemfactors.saveAsTextFile(item_embedding_path)
			}
		}
		spark.stop()
	}
}

```  


## 3.代码分析

```
PathUtils.user_item_click_path
```  

这个是输入的数据集，包含三个字段：userid, itemid, 点击数  

```
genUserItemIndex
```  

这个方法是针对userid与itemid进行编码，注意是分开编码  


```
trainmodel
```  

这个方法的具体步骤如下：  

1.构造训练集  
2.得到als对象  
3.训练模型 als.fit  
4.根据得到的模型进行预测  
5.分别得到user向量与item向量。  

