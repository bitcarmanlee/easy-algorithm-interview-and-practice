现在有如下格式的json串：  
```
"detail_time":"2016-03-30 16:00:00","device_id":"123456","os":"Html5Wap","session_flow_id":"1d1819f3-8e19-4597-b50d-ba379adcd8e5","user_longitude":0.0000,"user_latitude":0.0000,"search_id":xxx,"search_guid":-543326548,"search_type":7,"AAA":4,"BBB":-1,"CCC":[],"DDD":3,"EEE":2,"FFF":1459267200,"GGG":1459353600,"aaa":90954603,"bbb":[{"xxx":1500848,"x":1,"bf":0,"pp":2,"sroom":2,"ppp":108,"cost":97.2,"coupon":108,"drr":108},{"xxx":1500851,"x":1,"bf":0,"pp":1,"sroom":2,"ppp":108,"cost":97.2,"coupon":108,"drr":108},{"xxx":2336691,"x":1,"bf":1,"pp":1,"sroom":3,"ppp":199,"cost":169.15,"coupon":191,"drr":199},{"xxx":2336692,"x":1,"bf":1,"pp":2,"sroom":4,"ppp":102,"cost":91.8,"coupon":102,"drr":102},{"xxx":1500848,"x":1,"bf":0,"pp":2,"sroom":3,"ppp":118,"cost":106.2,"coupon":118,"drr":118},{"xxx":1500851,"x":1,"bf":0,"pp":1,"sroom":3,"ppp":118,"cost":106.2,"coupon":118,"drr":118},{"xxx":2336693,"x":1,"bf":1,"pp":1,"sroom":5,"ppp":199,"cost":169.15,"coupon":191,"drr":199},{"xxx":2336694,"x":1,"bf":1,"pp":2,"sroom":6,"ppp":112,"cost":100.3,"coupon":112,"drr":112},{"xxx":1500848,"x":1,"bf":0,"pp":2,"sroom":1,"ppp":98,"cost":88.2,"coupon":98,"drr":98},{"xxx":1500851,"x":1,"bf":0,"pp":1,"sroom":1,"ppp":98,"cost":88.2,"coupon":98,"drr":98},{"xxx":2336687,"x":1,"bf":1,"pp":1,"sroom":1,"ppp":189,"cost":160.65,"coupon":182,"drr":189},{"xxx":2336689,"x":1,"bf":1,"pp":2,"sroom":2,"ppp":93,"cost":83.3,"coupon":93,"drr":93},{"xxx":1500848,"x":1,"bf":0,"pp":2,"sroom":4,"ppp":128,"cost":115.2,"coupon":128,"drr":128},{"xxx":1500851,"x":1,"bf":0,"pp":1,"sroom":4,"ppp":128,"cost":115.2,"coupon":128,"drr":128},{"xxx":2336695,"x":1,"bf":1,"pp":1,"sroom":7,"ppp":239,"cost":203.15,"coupon":230,"drr":239},{"xxx":2336696,"x":1,"bf":1,"pp":2,"sroom":8,"ppp":121,"cost":108.8,"coupon":121,"drr":121}],"ppp_min":93.00,"ppp_max":239.00,"ppp_avg":134.88,"ppp_med":118.00,"ppp_min_cost":83.30,"ppp_min_promotion_type":-1,"ppp_min_promotion_amount":-1,"bf_ppp_min":149.00,"bf_ppp_min_cost":83.30,"bf_ppp_min_promotion_type":-1,"bf_ppp_min_promotion_amount":-1}
```  

现在想拿到device_id的具体值。最简单的方式就是用解析json串的方式得到，代码如下：  

```
#!/usr/bin/env python
#coding:utf-8

import json
import sys
import collections
import time

def t1():
    start = time.clock()
    for line in sys.stdin:
        try:
            line = line.strip()
            decoded = json.loads(line)
            device_id = decoded["device_id"]
            print device_id
        except Exception,ex:
            pass

    end = time.clock()
    print "The cost time is: %f" %(end - start)

t1()
```  

以上代码能顺利完成任务。  

不幸的是，现在是大数据时代，数据量嘛，自然都很大。用了一万条数据做测试，耗时达到了惊人的。。。将近10s。  

转换下思路，采用正则匹配的方式  

```
#!/usr/bin/env python

import re
import sys
import time

def t1():
    start = time.clock()
    count = 0
    for line in sys.stdin:
        line = line.strip()
        pattern = re.compile("(?:\"device_id\":\")([^\"]+)")
        search = pattern.search(line)
        if search:
            count += 1
            #print search.groups()[0]
    end = time.clock()
    print "The count is: %d" %(count)
    print "The cost time is: %f" %(end - start)

t1()
```  

注意匹配的时候  

`re.compile("(?:\"device_id\":\")([^\"]+)")`  
第一个分组表示不捕获，只捕获后面的分组。  
同样一万条数据，运行耗时是。。。0.05s。效率提高了多少倍，表示算不过来了。  
