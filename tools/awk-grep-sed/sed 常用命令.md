测试文件：filetest  
aaa bbb ccc  
ddd eee fff  
111 222 333  

## 1.在第一行中插入一行(即在文件头插入一行，经常用于描述文件字段信息)

```
sed -i '1i no1\tno2\tno3' filetest
```  

或者：  

```
sed -i '1 i\no1\tno2\tno3' filetest
```  

都可以在满足需求  

## 2.在最后一行追加一行

```
sed -i '$a 1\t2\t3' filetest
```  

或者：  

```
sed -i '$ a\1\t2\t3' filetest
```  

tips:\i是在当前行之前插入文本。如果要插入多行，不同行之间\n即可  
	 \c是用此符号后的新文本替换当前行中的文本  
	 \a是在当前行之后插入文本  

## 3.将匹配行替换：

```
sed -e '/aaa/c\888' filetest
```  

888  
ddd eee fff  
111 222 333  

## 4.字符串替换：

```
sed -e 's/aaa/ttt/g' filetest
```  

ttt bbb ccc  
ddd eee fff  
111 222 333  

g表示全部替换  

## 5.删除行首空格

```
sed 's/^[ ]*//g' filename
sed 's/^ *//g' filename
sed 's/^[[:space:]]*//g' filename
```  

## 6.替换单引号

```
sed "s/'//g" file
```  

## 7.删除第一行

```
sed -i '1d' file
```  

## 8.在每行行尾添加字符串

```
sed -i 's/$/\t1226/g'
```  
