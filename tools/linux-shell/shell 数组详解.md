数组是shell中常用的一个东东。现在对shell中的数组做一个小结，方便以后使用。  

## 1.初始化数组
初始化数组有两种方式，直接上代码  

```
array=(0 1 2)

arr[0]=0
arr[1]=1
arr[2]=2

```  

这两种方式都能初始化数组，达到的效果是一致的。需要注意的一点是，用第二种方式初始化的时候，不需要先声明arr，否则shell运行的时候会提示找不到arr命令。  

## 2.求数组的长度

```
echo ${#arr[@]}
echo ${#arr[*]}
```  

以上两种方式都能得到数组的长度。  

## 3.遍历数组

```
for i in ${arr[@]}
do
    echo $i
done

for i in ${arr[*]}
do
    echo $i
done
```  

以上两种方式都能遍历数组  

## 4.带下标遍历数组

```
index=0
while [ $index -lt ${#arr[@]} ]
do
    echo ${arr[$index]}
    let index++
done
```  

或者用c风格的代码也能达到目的：  

```
i=0
for (( i=0; i<${#arr[@]}; i++ ))
do
    echo ${arr[$i]}
done
```  