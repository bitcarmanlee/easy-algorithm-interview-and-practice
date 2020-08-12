做性能测试的时候，经常需要得到程序运行时间。  

写了个简答的shell脚本，供同学们参考。  


```
#!/bin/bash

function handle()
{
    start=$(date +%s%N)
    start_ms=${start:0:16}
    awk '{a[$1]++} END{print length(a)}' breakfast_all receptions_all cheap_all
    end=$(date +%s%N)
    end_ms=${end:0:16}
    echo "cost time is:"
    echo "scale=6;($end_ms - $start_ms)/1000000" | bc
}

handle

```  

代码思路比较清晰 %s是精确到秒，%N是纳秒，取字符串前16位，得到的是秒后小数点六位。再除以1000000，最终的结果为以s为单位，精确到小数点后6位。  

需要不同的精度，调整字符串截取的位数即可。