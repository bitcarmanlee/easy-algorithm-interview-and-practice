hive sql 中有时间戳转日期的函数  

from_unixtime(BIGINT unixtime [, STRING format])  

这里面的unixtime，输入单位是秒，也就一个十位的BIGINT。但是我们实际中用的时间戳，一般都是13位的到毫秒时间戳，如果直接将该时间戳输入方法中会有错误。  

如果是13位时间戳，可以这么使用  

```
from_unixtime(cast(timestamp/1000 as bigint)) as xxx_time
```  

timestamp/1000 是一个double类型，直接cast变成bigint就可以了。  

当然还可以在方法后面填入可选参数为日期格式。  