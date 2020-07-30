## 1.redis安装
在ubuntu上安装redis非常简单  

```
sudo apt-get install redis-server
```  
安装完成后，Redis服务器会自动启动。  

```
ps -aux | grep redus
redis    31087  0.0  0.0  56348 19084 ?        Ssl   8月27   1:00 /usr/bin/redis-server *:6379               
```  

## 2.访问redis

安装Redis服务器，会自动地一起安装Redis命令行客户端程序。  
输入redis-cli命令以后就可以启动客户端程序了。  

```
$ redis-cli 
127.0.0.1:6379> 

```  

## 3.查看redis相关信息  
在redis-cli中输入info命令，可以查看到很多redis相关的指标  

```
127.0.0.1:6379> info
# Server
redis_version:2.8.4
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:645b61b5aa39f6b1
redis_mode:standalone
os:Linux 4.2.0-27-generic x86_64
arch_bits:64
multiplexing_api:epoll
gcc_version:4.8.4
process_id:31087
run_id:86c05b8353730892d696855760a8a503895d99d8
tcp_port:6379
uptime_in_seconds:191989
uptime_in_days:2
hz:10
lru_clock:1517536
config_file:/etc/redis/redis.conf

# Clients
connected_clients:1
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0

# Memory
used_memory:12588176
used_memory_human:12.01M
used_memory_rss:19542016
used_memory_peak:12608144
used_memory_peak_human:12.02M
used_memory_lua:33792
mem_fragmentation_ratio:1.55
mem_allocator:jemalloc-3.5.1
...
```  

可以看出，info命令会输出很多相关的指标。挑选几个比较重要的指标参考一下  

```
connected_clients:68  #连接的客户端数量
used_memory_rss_human:847.62M
used_memory_peak_human:794.42M 
total_connections_received:619104 #服务器已接受的连接请求数量
instantaneous_ops_per_sec:1159 #服务器每秒钟执行的命令数量
instantaneous_input_kbps:55.85 #redis网络入口kps
instantaneous_output_kbps:3553.89 #redis网络出口kps
rejected_connections:0 #因为最大客户端数量限制而被拒绝的连接请求数量
expired_keys:0 #因为过期而被自动删除的数据库键数量
evicted_keys:0 #因为最大内存容量限制而被驱逐（evict）的键数量
keyspace_hits:0 #查找数据库键成功的次数
keyspace_misses:0 #查找数据库键失败的次数
```  

然后重点关注一下内存相关的参数。  

```
# Memory
used_memory: //数据占用了多少内存（字节）
used_memory_human: //数据占用了多少内存（带单位的，可读性好）
used_memory_rss:  //redis占用了多少内存
used_memory_peak: //占用内存的峰值（字节）
used_memory_peak_human: //占用内存的峰值（带单位的，可读性好）
used_memory_lua:  //lua引擎所占用的内存大小（字节）
mem_fragmentation_ratio:  //内存碎片率
mem_allocator: //redis内存分配器版本，在编译时指定的。有libc、jemalloc、tcmalloc这3种
```  

## 4.jedis连接redis  
项目中一般会用各种代码去操作redis，而redis也提供了各种语言的客户端接口。以java中常用的jedis为例看看怎么操作。  
首先引入jedis的依赖  

```
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>2.9.0</version>
</dependency>
```  

```
    public void test1() {
        Jedis jedis = new Jedis("xxx.xxx.xxx.xxx", 6379);
        jedis.set("key1", "jedis");
        String result = jedis.get("key1");
        System.out.println(result);
        jedis.close();
    }
```  

上面的方式在每次使用时，构建Jedis对象即可。在Jedis对象构建好之后，Jedis底层会打开一条Socket通道和Redis服务进行连接。所以在使用完Jedis对象之后，需要调用Jedis.close()方法把连接关闭，不如会占用系统资源。当然，频繁的创建和销毁Jedis对象，对应用的性能是很大影响的，因为构建Socket的通道是很耗时的(类似数据库连接)。我们应该使用连接池来减少Socket对象的创建和销毁过程。  

```
    public void test2() {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxIdle(8);
        config.setMaxTotal(18);
        JedisPool pool = new JedisPool(config, "xxx.xxx.xxx.xxx", 6379, 2000);
        Jedis jedis = pool.getResource();
        long start = System.currentTimeMillis();
        for(int i=0; i<100000; i++) {
            String key = "key" + i;
            String value = "jedis" + i;
            jedis.set(key, value);
        }
        long end = System.currentTimeMillis();
        System.out.println("cost time is: " + (end - start) / 1000.0 + "s");
        jedis.close();
        pool.close();

    }
}
```  
上面就是采用连接池的方式进行操作。在本机测试，串行写入10w个key耗时为1.2s，还是比较快的。  

