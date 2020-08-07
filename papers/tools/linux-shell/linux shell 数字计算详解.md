代码中免不了要进行各种数据计算。抛开科学计算不提，普通的计算占地，百分比，同比，环比等需求就很常见。linux shell中进行数字计算，主要有如下几种方式：  

## 1.bc
bc是比较常用的linux计算工具了，而且支持浮点运算：  

```
[webopa@namenode-backup expensive_user]$ a=`echo 1+1 | bc`
[webopa@namenode-backup expensive_user]$ echo $a
2
```  

但是浮点数运算的精度问题，暂时还没明白什么情况：  

```
[webopa@namenode-backup expensive_user]$ b=`echo "1.2*1.2" | bc`
[webopa@namenode-backup expensive_user]$ echo $b
1.4
[webopa@namenode-backup expensive_user]$ c=`echo "5.0/3.0" | bc`
[webopa@namenode-backup expensive_user]$ echo $c
1
[webopa@namenode-backup expensive_user]$ d=`echo "scale=2;5.0/3.0" | bc`
[webopa@namenode-backup expensive_user]$ echo $d
1.66
[webopa@namenode-backup expensive_user]$ e=`echo "scale=2;5.0/6.0" | bc`
[webopa@namenode-backup expensive_user]$ echo $e
.83
```  

尤其最后一个，这到底什么鬼，小数点前的那个0跑哪里去了。。。  

## 2.expr
不支持浮点数计算。这又是个大坑.而且要注意数字与运算符中的空格  

```
[webopa@namenode-backup expensive_user]$ a=`expr 1+1`
[webopa@namenode-backup expensive_user]$ echo $a
1+1
[webopa@namenode-backup expensive_user]$ a=`expr 1 + 1`
[webopa@namenode-backup expensive_user]$ echo $a
2
[webopa@namenode-backup expensive_user]$ b=`expr 10 / 2`
[webopa@namenode-backup expensive_user]$ echo $b
5
```  

## 3.$(())
同expr，不支持浮点数运算  

```
[webopa@namenode-backup expensive_user]$ a=$((1+1))
[webopa@namenode-backup expensive_user]$ echo $a
2
[webopa@namenode-backup expensive_user]$ b=$((1 + 3 ))
[webopa@namenode-backup expensive_user]$ echo $b
4
```  

## 4.let
不支持浮点数运算，而且不支持直接输出，只能赋值  

```
[webopa@namenode-backup expensive_user]$ let a=1+1
[webopa@namenode-backup expensive_user]$ echo $a
2
[webopa@namenode-backup expensive_user]$ let b=50/5
[webopa@namenode-backup expensive_user]$ echo $b
10
[webopa@namenode-backup expensive_user]$ let c=1.2*2
-bash: let: c=1.2*2: syntax error: invalid arithmetic operator (error token is ".2*2")
```  

## 5.awk
普通的运算：  

```
[webopa@namenode-backup expensive_user]$ a=`echo | awk '{print 1.0/2.0}'`
[webopa@namenode-backup expensive_user]$ echo $a
0.5
```  

控制精度：  

```
[webopa@namenode-backup expensive_user]$ b=`echo | awk '{printf("%.2f",1.0/2.0)}'`
[webopa@namenode-backup expensive_user]$ echo $b
0.50
```  

传递参数：  

```
[webopa@namenode-backup expensive_user]$ c=`echo | awk -v a=1 -v b=3 '{printf("%.4f",a/b)}'`
[webopa@namenode-backup expensive_user]$ echo $c
0.3333
```  

综合来看，还是awk最靠谱，其他的方式都有这样那样的问题。所以我平时一般都用awk来搞数学计算。  
