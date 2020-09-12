## 1.常用的模块

```
from datetime import datetime
import time
from dateutil.parser import parse
```  

## 2.得到当前时间

```
def getCurrentTime():
    now = datetime.now()
    print(now)
    print(type(now))
```  

结果为  

```
2020-05-07 09:39:02.318002
<class 'datetime.datetime'>
```  

## 3.得到datetime对象

```
def genDateTimeObj():
    date = datetime(2020, 4, 19, 15, 30)
    print(date)
    print(type(date))
```  

```
2020-04-19 15:30:00
<class 'datetime.datetime'>
```  

## 4.datetime转时间戳

```
def datetime_2_timestamp():
    now = datetime.now()
    now_timetuple = now.timetuple()
    now_second = time.mktime(now_timetuple)
    now_millisecond =  int (now_second * 1000 + now.microsecond / 1000)

    print(now.timestamp())
    print(now_millisecond)
```  

```
1588815680.100948
1588815680100
```  

注意如果直接用timestamp()方法得到的是一个浮点数，且时间戳是十位，单位为秒。下面的方法得到的时间戳为十三位，毫秒。  

## 5.时间戳转datetime

```
def timestamp_2_datetime():
    timestamp = 1588761521787 / 1000
    date = datetime.fromtimestamp(timestamp)
    print(date)
```  

```
2020-05-06 18:38:41.787000
```  

## 6.datetime转字符串

```
def datetime_2_str():
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    print(date)
```  

```
2020-05-07 09:44:22
```  

## 7.字符串转datetime

```
def str_2_datetime():
    datestr = "2020-05-06 18:42:26"
    date = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
    print(date)
    print(type(date))
```  

```
2020-05-07 09:44:22
```  

## 8.求两个时间差

```
def get_interview():
    t1 = "2020-05-05 23:56:45"
    t2 = "2020-05-06 00:00:31"
    date1 = parse(t1)
    date2 = parse(t2)
    result = (date2 - date1).total_seconds()
    print(result)
```  

```
226.0
```  

上面的方法，求得的是两个时间之间差的秒数。  
