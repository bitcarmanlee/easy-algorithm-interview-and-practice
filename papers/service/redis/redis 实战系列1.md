最近新接手的项目，要把数据最终推到线上的redis集群里。正好趁着这次项目的机会，彻底梳理一下redis相关的东东。  

个人观点是：凡是与数据相关的项目，实践性都特别强。对于这种特点的内容，我遵循的学习原则是先搞明白what，即搞清楚这东西到底是个什么鬼，有什么用。接下来就是how，即搞清楚这个东东怎么用，怎么最快速的搭建环境，并且让代码run起来。最后一步则是why，在有一定实践经验的基础上，来搞清楚这东西到底为什么要这么搞，跟其他同类产品相比有什么优缺点，适用的场景等等。  

## 1.what，redis到底是个什么鬼
要搞清楚一个东西到底是什么鬼，最简单最方便也最可靠的方法自然就是google（这个必须要用谷歌爸爸）。都使用redis关键字进行搜素，对比一下谷歌爸爸与某搜索引擎的结果：  
谷歌爸爸搜索结果：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/service/redis/1.png)  
第一条redis官网，第二条github官方地址，第三条redis维基百科中文版，第四条维基百科英文版，结果排序堪称完美。。。基本通过这几个页面就能对redis有个清晰快速的了解。  


这是某搜索引擎的搜素结果：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/service/redis/2.png)  

第一条也是redis官网。至于后面的内容，也不能说太差。只是相比google爸爸的搜索结果，好像还是感觉差那么一个档次。。。  

看看维基百科上是怎么介绍redis的：  
Redis是一个开源、支持网络、基于内存、键值对存储数据库，使用ANSI C编写。从 2015 年 6 月开始，Redis 的开发由Redis Labs赞助，在 2013 年 5 月至 2015 年 6 月期间，其开发由Pivotal赞助。在2013年5月之前，其开发由VMware赞助。根据月度排行网站DB-Engines.com的数据显示，Redis是最流行的键值对存储数据库。  

简单总结起来一句话：redis是目前最流行的基于内存的kv对非关系型数据库。  

## 2.查看redis集群信息
QA同学已经帮忙给分配了一个测试环境的redis集群。关于redis集群的搭建，后面会专门有文章介绍。咱们先查看一下redis的信息：  
cd 到rediscluster目录，然后执行./redis-cli info  
```
/home/work/rediscluster$ ./redis-cli info
# Server
redis_version:3.0.7
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:70563032b83216cf
redis_mode:cluster
os:Linux 2.6.32-358.el6.x86_64 x86_64
arch_bits:64
multiplexing_api:epoll
gcc_version:4.4.7
process_id:18697
run_id:921ef4b414662ab0767ffffdf31ec1f16dfb6168
tcp_port:6379
uptime_in_seconds:174297
uptime_in_days:2
hz:10
lru_clock:8258346
config_file:/home/work/rediscluster/6379/conf/./redis.conf
...
```  

信息太长，咱们只查看一下server部分的信息。很容易看出来redis的版本为3.0.7。  

## 3.查看redis实例
因为是redis集群，所以集群起的redis实例不止一个。查看一下集群中redis进程有多少：  

```
ps -ef | grep redis
root     18697     1  0 Jul05 ?        00:04:30 ../bin/redis-server *:6379 [cluster]
root     18701     1  0 Jul05 ?        00:06:45 ../bin/redis-server *:6380 [cluster]
root     18705     1  0 Jul05 ?        00:06:19 ../bin/redis-server *:6381 [cluster]
root     18709     1  0 Jul05 ?        00:05:48 ../bin/redis-server *:6382 [cluster]
root     18714     1  0 Jul05 ?        00:06:15 ../bin/redis-server *:6383 [cluster]
root     18718     1  0 Jul05 ?        00:07:02 ../bin/redis-server *:6384 [cluster]
root     18722     1  0 Jul05 ?        00:05:10 ../bin/redis-server *:6385 [cluster]
tester   21770 21654  0 15:28 pts/1    00:00:00 grep --color redis
```  
由此可见，整个集群有7个redis实例，分别对应了6379-6385端口。