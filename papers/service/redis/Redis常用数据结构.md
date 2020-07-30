## 1.Redis数据结构概览  
Redis总共包含有五种数据结构：  
1.String，单个key，单个value，一个redis字符串中最大有512M。  
2. Hash 是一个键值对的集合  
3. List 是一个链表结构  
4. Set 是一个无序集合，并且无重复  
5. Zset(sort set)　是一个有序集合，无重复  

## 2.String
value是字符串类型  

常用的命令包括  

```
set key value：设置key、value
setex key seconds value：设置key、value，有效期seconds秒
setnx key value：设置key、value，如果key存在则setnx失败，返回 0 （set key value nx等价）
get key：获取key的值
getset key value：设置key、value，并返回value
mset key value key value：批量设置key、value
mget key key：批量获取key的值
incr key：key对应的value自增，如果key对应value不是整数返回错误，如果key不存在，将value设置为 1
decr key:key对应的value自减
incrby key increment：key对应的value增加increment
decrby key increment：key对应的value减少increment
incrbyfloat key increment：key对应的浮点数value增加increment（只有incrbyfloat命令，没有decrbyfloat命令，可以用incrbyfloat一个负数实现decrbyfloat命令）
```  

在服务器上测试  

```
xxx:7001> set abc 10
-> Redirected to slot [7638] located at 10.38.164.94:7004
OK
xxx:7004> get abc
"10"
xxx:7004> incr abc
(integer) 11
xxx:7004> incrby abc 20
(integer) 31
xxx:7004>  object encoding abc
"int"
xxx:7004> set a1 helloworldandredisandjava
OK
xxx:7004>  object encoding a1
"embstr"
xxx:7004> set a2 helloworldandredisandjavaandpythonandscalaandcandshell
-> Redirected to slot [11786] located at 10.38.164.94:7002
OK
10.38.164.94:7002>  object encoding a2
"raw"
```  

String的内部编码方式  

int：8 个字节的长整型  
embstr：小于等于 39 个字节的字符串  
raw：大于 39 个字节的字符串  

其中，incr命令可用于计数，mget、mset命令可以在多条命令时减少网络层传输时间，setnx命令可用于分布式锁的一种实现方案，保证只有一个客户端能请求成功。  


## 3.Hash
即value是Hash的类型，value={f1:v1, f2:v2}这种样子。  
经常使用的命令  

```
HSET key field value　设置hash
HSETNX key field value　将哈希表 key 中的域 field 的值设置为 value ，当且仅当域 field 不存在。若域 field 已经存在，该操作无效。如果 key 不存在，一个新哈希表被创建并执行 HSETNX 命令。设置成功，返回 1 。如果给定域已经存在且没有操作被执行，返回 0 。
HMSET key field value [field value ...]　同时将多个 field-value (域-值)对设置到哈希表 key 中
HGET key field　返回哈希表 key 中给定域 field 的值。
HGETALL key　返回哈希表 key 中，所有的域和值
HKEYS key　返回哈希表 key 中的所有域。
HVALS key　返回哈希表 key 中所有域的值。
HLEN key　返回哈希表 key 中域的数量。
HEXISTS key field　给定域 field 是否存在
HDEL key field [field ...]　删除哈希表 key 中的一个或多个指定域，不存在的域将被忽略。
HINCRBY key field increment　为哈希表 key 中的域 field 的值加上增量 increment 
```  

在服务器上测试  

```
xx:7004> HSET people name zhangsan
(integer) 1
xx:7004> HSET people age 18
(integer) 1
xx:7004> HSET people sex male
(integer) 1
xx:7004> HGET people name
"zhangsan"
xx:7004> HKEYS people
1) "name"
2) "age"
3) "sex"
xx:7004> HVALS people
1) "zhangsan"
2) "18"
3) "male"
xx:7004> HLEN people
(integer) 3
```  

hash对象底层存储结构为ziplist（压缩列表）和hashtable。当对象满足一下两条时，hash对象使用ziplist编码。  
1.hash对象保存的所有kv对的k与v的字符串长度都小于64Byte。  
2.hash对象的kv数量小于512个。  


由上面的分析，hash类型十分适合对象类数据的存储，field就是对象的各个属性，而field的值为对象属性的值。  

## 4.List
list 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）。  

List常用的命令包括  

```
LPUSH key value [value ...]　将一个或多个值 value 插入到列表 key 的表头。
LPUSHX key value　将 value 插入到列表 key 的表头　当 key 不存在时， LPUSHX 命令什么也不做
RPUSH key value [value ...]　将一个或多个值 value 插入到列表 key 的表尾(最右边)。
RPUSHX key value　将值 value 插入到列表 key 的表尾　当 key 不存在时， RPUSHX 命令什么也不做
LPOP key　移除并返回列表 key 的头元素。
RPOP key　移除并返回列表 key 的尾元素。
LLEN key　返回列表 key 的长度。
LRANGE key start stop　返回列表 key 中指定区间内的元素，区间以偏移量 start 和 stop 指定。
LINDEX key index　返回列表 key 中，下标为 index 的元素。
LSET key index value　将列表 key 下标为 index 的元素的值设置为 value 。
LINSERT key BEFORE|AFTER pivot value　将值 value 插入到列表 key 当中，位于值 pivot 之前或之后。
LTRIM key start stop　对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
BLPOP key [key ...] timeout　它是 LPOP 命令的阻塞版本，当给定列表内没有任何元素可供弹出的时候，连接将被 BLPOP 命令阻塞，直到等待超时或发现可弹出元素为止。当给定多个 key 参数时，按参数 key 的先后顺序依次检查各个列表，弹出第一个非空列表的头元素
BRPOP key [key ...] timeout　与BLPOP类似
```  

list在内部的编码有两种方式:ziplist与linkedlist。ziplist使用更加紧凑的结构实现多个元素的连续存储，在内存方便比linkedlist优秀；linkedlist在读写效率方面会比ziplist高。  
当元素数量小于512，或者所有元素占用的字节数都小于64Byte时，会使用ziplist存储。  

list的使用场景：  
1.消息队列，使用lpush + rpop就可以。如果是lpush+brpop可以实现阻塞队列。  
2.栈，使用lpush + lpop就可以。  
3. list 结构的数据查询两端附近的数据性能非常好，适合一些需要获取最新数据的场景，比如取最新的新闻，最近的topN等操作。  

## 5.Set  
set 是string类型的无序集合，可以方便进行求交集，并集，差集等工作。set中的元素是无序的，所以增加，删除，查找的炒作都是O(1)时间复杂度。  

```
SADD key member [member ...]　在集合key中插入一个或多个元素。如果key不存在则先创建集合key。
SCARD key　返回集合中的元素个数。
SDIFF key [key ...] 返回多个集合的差集，如果某些集合key不存在认为是空集
SDIFFSTORE destination key [key ...] 计算多个集合的差集并存储在 destination 中
SINTER key [key ...] 返回多个集合的交集
SUNION key [key ...] 返回多个集合的并集
SISMEMBER key member 判断member是否存在于集合key中。
SMEMBERS key 返回集合key的所有元素。如果key不存在认为是空集。
SREM key member [member ...] 从集合key中移除一个或多个元素。
```  

set 的内部实现是一个 value永远为null的HashMap，实际就是通过计算hash的方式来快速排重的，这也是set能提供判断一个成员是否在集合内的原因。  


使用场景：  
1.一个用户关注的所有人。  
2.一个用户的所有粉丝。  
3.两个用户的共同关注，共同喜好，二度好友等。  

## 6.Zset
Zset有序集合和Set一样不能有重复的元素，并且可以对元素进行排序。  
在 set 的基础上给集合中每个元素关联了一个分数(score)，往有序集合中插入数据时会自动根据这个分数排序。  

```
zadd key score member [score member …]：添加成员
zcard key：计算成员数量
zscore key member：计算某个成员的分数
zrank key member：计算成员的排名，从低到高计算
zrevrank key member：计算成员的排名，从高到低计算
zrem key member [member …]：删除成员
zincrby key increment member：增加成员的分数
zrange key start end [withscores]：从低到高排序取指定元素，如果带上withscores则同时返回score
zrevrange key start end [withscores]：从高到低排序取指定元素，如果带上withscores则同时返回score
zrangebyscore key min max [withscores]：从低到高排序显示分值在min到max之间的成员（包括min和max）
zrevrangebyscore key min max [withscores]：从高到低排序显示分值在min到max之间的成员（包括min和max）
zcount key min max：统计分值在min到max之间的成员（包括min和max）个数
```  

Zset 内部编码有两种方式 1.ziplist 2.skiplist  
当元素数量小于128，每个元素都小于64Byte时，使用ziplist存储可以节约内存。  

使用场景：  
1.排行榜。排行榜一般都是唯一id，并且需要进行排序。  
2.带权重的消息队列  