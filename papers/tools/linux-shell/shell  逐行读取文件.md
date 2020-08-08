很常见的需求，话不多说，直接上代码  

```
#!/bin/bash

#cat出来，for循环
function f1()
{
    IFS="
"
    for line in `cat test.txt`
    do
        echo $line
    done
    echo '------------------'
}

#文章重定向给read处理
function f2()
{
    cat test.txt | while read line
    do
        echo $line
    done
    echo '------------------'
}

#用read读取文件重定向
function f3()
{
    while read line
    do
        echo $line
    done <test.txt
}

f1
f2
f3



$ ./read_file.sh
aaa 123
bbb 123
ccc 123
------------------
aaa 123
bbb 123
ccc 123
------------------
aaa 123
bbb 123
ccc 123
```  



注意方法一中要制定分隔符IFS为换行符，否则输出结果不对

