Hbase里的数据量一般都小不了，因此MapReduce跟Hbase就成了天然的好搭档。本文中，本博主将给出最详细的用MR读取Hbase中数据的实例。  


## 1.ZK授权表
首先一点来说，Hbase是强依赖于ZK的。博主所在的team，就经常出现ZK连接数太多被打爆然后Hbase挂了的情况。一般在访问Hbase表之前，需要通过访问ZK得到授权：  

```
    /**
     * 为hbase表授权。
     *
     * @param tableConfigKey 任意一个字符串。
     * @param tableName 需要授权的表名, scan涉及到的表不需要额外授权。
     * @param job 相关job。
     * @throws IOException
     */
    public static void initAuthentication(String tableConfigKey, String tableName, Job job) throws IOException {
        Configuration peerConf = job.getConfiguration();
        peerConf.set(tableConfigKey, tableName);
        ZKUtil.applyClusterKeyToConf(peerConf, tableName);
        if (User.isHBaseSecurityEnabled(peerConf)) {
            LOGGER.info("Obtaining remote user authentication token with table:{}", tableName);
            try {
                User.getCurrent().obtainAuthTokenForJob(peerConf, job);
            } catch (InterruptedException ex) {
                LOGGER.info("Interrupted obtaining remote user authentication token");
                LOGGER.error("Obtained remote user authentication token with table:{}, error:\n", tableName, ex);
                Thread.interrupted();
            }
            LOGGER.info("Obtained remote user authentication token with table:{}", tableName);
        }
    }
```  

代码相对比较简单，都是Hbase与ZK提供的一些辅助工具类。不解释。  

## 2.thrift对象转化
本例中操作的对象为XX表，Column Family为"P", Qualifer 为"P"与"C"，里面对应的value都是thrift对象。其中"P"对应的thrift对象为:  

```
struct UserProfile {
    1: optional byte sex; 
    2: optional i32 age;
    3: optional string phoneBrand;
    4: optional string locationProvince;
}
```  

"C"对应的thrift对象为:  

```
struct UserClickInfo {
    1: required i32 totolAck;
    2: required i32 totalClick;
    3: optional map<i64, map<string, i32>> ackClick;
}
```  

这个时候我们就需要经常将Bytes转化为thrift对象，通用的方法为：  

```
    /**
     * convert byte array to thrift object.
     *
     * @param <T> type of thrift object.
     * @param thriftObj an thrift object.
     * @return byte array if convert succeeded, <code>null</code> if convert failed.
     * @throws TException
     */
    public static final <T extends TBase<T, ?>> T convertBytesToThriftObject(byte[] raw, T thriftObj) throws TException {
        if (ArrayUtils.isEmpty(raw)) {
            return null;
        }
        Validate.notNull(thriftObj, "thriftObj");

        TDeserializer serializer = new TDeserializer(new TBinaryProtocol.Factory());
        serializer.deserialize(thriftObj, raw);
        return thriftObj;
    }
```  

## 3.Map阶段读取Hbase里的数据
在Map阶段对Hbase表扫描，得出数据  

```
	//输出的KV均为Text
    static class ReadMapper extends TableMapper<Text,Text> {

        @Override
        protected void map(ImmutableBytesWritable key, Result res, Context context) throws IOException,InterruptedException{
            String uuid = StringUtils.reverse(Bytes.toString(key.copyBytes()));
            if (res == null || res.isEmpty()) return;
            res.getFamilyMap(USER_FEATURE_COLUMN_FAMILY);


            for(KeyValue kv:res.list()) {
                String qualifier = Bytes.toString(kv.getQualifier());
                //String qualifier = kv.getKeyString();
                if(qualifier.equals("P")) {

                    try {
                        UserProfile userProfile = new UserProfile();
                        convertBytesToThriftObject(kv.getValue(), userProfile);
                        String profileRes = userProfile.getAge() + "," + userProfile.getSex() + ","
                                + userProfile.getPhoneBrand() + "," + userProfile.getLocationProvince();
                        context.write(new Text(uuid),new Text(profileRes));
                    } catch (Exception ex) {}
                }
                else if(qualifier.equals("C")) {
                    UserClickInfo userClickInfo = new UserClickInfo();
                    try {
                        convertBytesToThriftObject(kv.getValue(), userClickInfo);
                        Map<Long,Map<String,Integer>> resMap = userClickInfo.getAckClick();
                        for(Map.Entry<Long,Map<String,Integer>> entry:resMap.entrySet()) {
                            String appid = String.valueOf(entry.getKey());
                            int click = entry.getValue().get("click");
                            int ack = entry.getValue().get("ack");
                            String all = appid + "," + String.valueOf(click) + "," + String.valueOf(ack);
                            context.write(new Text(uuid),new Text(all));
                        }
                        int allClick = userClickInfo.getTotalClick();
                        int allAck = userClickInfo.getTotolAck();
                        String allNum = "999," + String.valueOf(allClick) + "," + String.valueOf(allAck);
                        context.write(new Text(uuid),new Text(allNum));
                    } catch (Exception ex) {}
                }
            }
        }
    }
```  

## 4.run方法里配置相关驱动
run方法里需要配置一些相关的参数，保证任务的顺利进行。  
其中，`TableMapReduceUtil.addDependencyJars`方法添加了完成任务一些必要的类。  

```
    public int run(String[] args) throws Exception{
        Configuration conf = HBaseConfiguration.create();

        Job job = Job.getInstance(conf,"read_data_from_hbase");
        job.setJarByClass(ReadDataFromHbase.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setReducerClass(ReadReducer.class);
        job.setSpeculativeExecution(false);

        TableMapReduceUtil.addDependencyJars(job.getConfiguration(),StringUtils.class, TimeUtils.class, Util.class,
                CompressionCodec.class, TStructDescriptor.class, ObjectMapper.class, CompressionCodecName.class, BytesInput.class);

        Scan scan = new Scan();
        //对整个CF扫描
        scan.addFamily(USER_FEATURE_COLUMN_FAMILY);

        String table = "XXX";
        initAuthentication(table,table,job);
        TableMapReduceUtil.initTableMapperJob(table,
                scan,
                ReadMapper.class,
                Text.class,
                Text.class,
                job);

        String output = "";
        FileSystem.get(job.getConfiguration()).delete(new Path(output), true);
        FileOutputFormat.setOutputPath(job,new Path(output));

        return job.waitForCompletion(true) ? 0 : 1;
    }
```  

##5.完整的代码

```
package XXX.XXX.XXX.mr_job_and_tools.task;

import com.twitter.elephantbird.thrift.TStructDescriptor;
import XXX.XXX.XXX.XXX.common.util.TimeUtils;
import XXX.XXX.XXX.thrift.UserClickInfo;
import XXX.XXX.XXX.thrift.UserProfile;
import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.Validate;
import org.apache.commons.lang3.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.KeyValue;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.security.User;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.zookeeper.ZKUtil;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.parquet.bytes.BytesInput;
import org.apache.parquet.format.CompressionCodec;
import org.apache.parquet.format.Util;
import org.apache.parquet.hadoop.metadata.CompressionCodecName;
import org.apache.thrift.TBase;
import org.apache.thrift.TDeserializer;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import shaded.parquet.org.codehaus.jackson.map.ObjectMapper;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Created by WangLei on 17-3-13.
 */
public class ReadDataFromHbase extends Configured implements Tool{

    private static final Logger LOGGER = LoggerFactory.getLogger(ReadDataFromHbase.class);
    public static final byte[] USER_FEATURE_COLUMN_FAMILY = Bytes.toBytes("P");

    /**
     * convert byte array to thrift object.
     *
     * @param <T> type of thrift object.
     * @param thriftObj an thrift object.
     * @return byte array if convert succeeded, <code>null</code> if convert failed.
     * @throws TException
     */
    public static final <T extends TBase<T, ?>> T convertBytesToThriftObject(byte[] raw, T thriftObj) throws TException {
        if (ArrayUtils.isEmpty(raw)) {
            return null;
        }
        Validate.notNull(thriftObj, "thriftObj");

        TDeserializer serializer = new TDeserializer(new TBinaryProtocol.Factory());
        serializer.deserialize(thriftObj, raw);
        return thriftObj;
    }


    /**
     * 为hbase表授权。
     *
     * @param tableConfigKey 任意一个字符串。
     * @param tableName 需要授权的表名, scan涉及到的表不需要额外授权。
     * @param job 相关job。
     * @throws IOException
     */
    public static void initAuthentication(String tableConfigKey, String tableName, Job job) throws IOException {
        Configuration peerConf = job.getConfiguration();
        peerConf.set(tableConfigKey, tableName);
        ZKUtil.applyClusterKeyToConf(peerConf, tableName);
        if (User.isHBaseSecurityEnabled(peerConf)) {
            LOGGER.info("Obtaining remote user authentication token with table:{}", tableName);
            try {
                User.getCurrent().obtainAuthTokenForJob(peerConf, job);
            } catch (InterruptedException ex) {
                LOGGER.info("Interrupted obtaining remote user authentication token");
                LOGGER.error("Obtained remote user authentication token with table:{}, error:\n", tableName, ex);
                Thread.interrupted();
            }
            LOGGER.info("Obtained remote user authentication token with table:{}", tableName);
        }
    }

    static class ReadMapper extends TableMapper<Text,Text> {

        @Override
        protected void map(ImmutableBytesWritable key, Result res, Context context) throws IOException,InterruptedException{
            String uuid = StringUtils.reverse(Bytes.toString(key.copyBytes()));
            if (res == null || res.isEmpty()) return;
            res.getFamilyMap(USER_FEATURE_COLUMN_FAMILY);


            for(KeyValue kv:res.list()) {
                String qualifier = Bytes.toString(kv.getQualifier());
                //String qualifier = kv.getKeyString();
                if(qualifier.equals("P")) {

                    try {
                        UserProfile userProfile = new UserProfile();
                        convertBytesToThriftObject(kv.getValue(), userProfile);
                        String profileRes = userProfile.getAge() + "," + userProfile.getSex() + ","
                                + userProfile.getPhoneBrand() + "," + userProfile.getLocationProvince();
                        context.write(new Text(uuid),new Text(profileRes));
                    } catch (Exception ex) {}
                }
                else if(qualifier.equals("C")) {
                    UserClickInfo userClickInfo = new UserClickInfo();
                    try {
                        convertBytesToThriftObject(kv.getValue(), userClickInfo);
                        Map<Long,Map<String,Integer>> resMap = userClickInfo.getAckClick();
                        for(Map.Entry<Long,Map<String,Integer>> entry:resMap.entrySet()) {
                            String appid = String.valueOf(entry.getKey());
                            int click = entry.getValue().get("click");
                            int ack = entry.getValue().get("ack");
                            String all = appid + "," + String.valueOf(click) + "," + String.valueOf(ack);
                            context.write(new Text(uuid),new Text(all));
                        }
                        int allClick = userClickInfo.getTotalClick();
                        int allAck = userClickInfo.getTotolAck();
                        String allNum = "999," + String.valueOf(allClick) + "," + String.valueOf(allAck);
                        context.write(new Text(uuid),new Text(allNum));
                    } catch (Exception ex) {}
                }
            }
        }
    }

    static class ReadReducer extends Reducer<Text,Text,Text,Text> {
        @Override
        protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException,InterruptedException{
            List<String> resultList = new ArrayList<String>();
            for(Text each:values) {
                resultList.add(each.toString());
            }
            String res = StringUtils.join(resultList,":");
            context.write(key,new Text(res));
        }
    }

    @Override
    public int run(String[] args) throws Exception{
        Configuration conf = HBaseConfiguration.create();

        Job job = Job.getInstance(conf,"read_data_from_hbase");
        job.setJarByClass(ReadDataFromHbase.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setReducerClass(ReadReducer.class);
        job.setSpeculativeExecution(false);

        TableMapReduceUtil.addDependencyJars(job.getConfiguration(),StringUtils.class, TimeUtils.class, Util.class,
                CompressionCodec.class, TStructDescriptor.class, ObjectMapper.class, CompressionCodecName.class, BytesInput.class);

        Scan scan = new Scan();
        //对整个CF扫描
        scan.addFamily(USER_FEATURE_COLUMN_FAMILY);

        String table = "XXX";
        initAuthentication(table,table,job);
        TableMapReduceUtil.initTableMapperJob(table,
                scan,
                ReadMapper.class,
                Text.class,
                Text.class,
                job);

        String output = "";
        FileSystem.get(job.getConfiguration()).delete(new Path(output), true);
        FileOutputFormat.setOutputPath(job,new Path(output));

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception{
        System.exit(ToolRunner.run(new ReadDataFromHbase(),args));
    }
}

```  

然后将代码打包，提交到集群上运行对应的shell脚本即可。  

## 6.版本信息
本文中的代码，对应的hadoop版本为2.6,Hbase版本为0.98。  