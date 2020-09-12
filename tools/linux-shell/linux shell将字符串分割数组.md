经常用将字符串分割为数组的需求。在shell中常用的方式为以下两种  

```
#!/bin/bash

function split_1()
{
    x="a,b,c,d"

    OLD_IFS="$IFS"
    IFS=","
    array=($x)
    IFS="$OLD_IFS"

    for each in ${array[*]}
    do
        echo $each
    done
}

function split_2()
{
    x="a,b,c,d"

    echo $x | awk '{split($0,arr,",");for(i in arr) print i,arr[i]}'
}

split_1
split_2
```  


对于方法一，将系统IFS临时替换为分隔符，然后再换回去，达到分割字符串为数组的目的  

对于方法二，采用awk的split函数分割，注意awk中的数组为关联数组，不清楚的同学们请查阅相关资料。  

