python是搞数据同学的不二选择。因此面对redis集群，自然就想到怎么用python去操作redis集群了。  

## 1.python的redis模块无法操作redis集群
之前用python里的redis模块操作过redis实例。但redis模块操作的不是redis集群，不知道能否实现操作集群的功能。写个简单的代码测试一下先：  

```
import redis

def redis_node():
    node =redis.StrictRedis(host='192.168.222.66',port=6379)
    node.set("name_test","admin")
    print node.get("name_test")
    
redis_node()
```  
运行代码，不出所料报错了：  

```
...
 File "/Library/Python/2.7/site-packages/redis/connection.py", line 582, in read_response
    raise response
redis.exceptions.ResponseError: MOVED 12285 192.168.222.66:6384
```  

## 2.安装redis-py-cluster模块
既然redis模块不能搞集群，那咱们再找找别的。通过google爸爸，找到了redis-py-cluster，咱们试试。  
先安装：  

```
sudo pip install redis-py-cluster
```  

稍等片刻，安装好上面的模块。  

## 3.使用redis-py-cluster模块操作redis集群
先上一个简单的代码  

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年7月7日

@author: lei.wang
'''

from rediscluster import StrictRedisCluster
import sys

def redis_cluster():
    redis_nodes =  [{'host':'192.168.222.66','port':6378},
                    {'host':'192.168.222.66','port':6380},
                    {'host':'192.168.222.66','port':6381},
                    {'host':'192.168.222.66','port':6382},
                    {'host':'192.168.222.66','port':6383},
                    {'host':'192.168.222.66','port':6384},
                    {'host':'192.168.222.66','port':6385}
                   ]
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception,e:
        print "Connect Error!"
        sys.exit(1)
        
    redisconn.set('name','admin')
    redisconn.set('age',18)
    print "name is: ", redisconn.get('name')
    print "age  is: ", redisconn.get('age')

redis_cluster()
```  

让代码run起来：  

```
name is:  admin
age  is:  18
```  

OK，这就是最简单的操作redis集群的方式！  

## 4.值得注意的小地方
测试的时候，故意将某几个host写错，发现照样能连接上redis集群。经过测试发现，只要有一个host写正确，都能连上redis集群。只有当所有host都不正确时候，才会连接失败。具体原因，以及影响，后续再进行观察了解。  