shell中判断字符串为空的几种方式，一一列举  


```
#!/bin/bash

test_str=""

if [ "$test_str" = "" ];then
    echo "NULL!"
fi

if [ x"$test_str" = x ];then
    echo "NULL!"
fi

if [ -z "$test_str" ]; then
    echo "NULL!"
fi


$ ./judge_null.sh
NULL!
NULL!
NULL!
```  


可以看出，以上三种方式，都可以达到目的