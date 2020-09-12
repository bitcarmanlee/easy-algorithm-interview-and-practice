## 1.使用rev命令

```
7040:~$ echo "123456" | rev
654321
```  

## 2.使用python工具

```
7040:~$ echo "123456" | python -c 'print raw_input()[::-1]'
654321
```  

tips：  
1.python中实现字符串反转非常容易，[::-1]就可以。具体原理为Extended Slices，可以参考  
https://docs.python.org/2/whatsnew/2.3.html#extended-slices  
2. -c command: 表示运行时以命令性字符串提交Python脚本  
3. raw_input()将管道传过过来的值作为字符串输入   

## 3.使用awk

```
7040:~$ echo "123456" | awk '{for(i=1; i<=length;i++) {line = substr($0, i, 1) line}} END{print line}'
654321
```  

tips:  
1.length为当前字符串的长度  
2.substr(\$0,i,1),表示取当前字符从索引i开始，取当前位  
3.line=substr(\$0,i,1) line；将六个值分别保持在内存栈中，到时候打印出来就成654321  
substr(\$3,6,2)   --->  表示是从第3个字段里的第6个字符开始，截取2个字符结束.  
substr(\$3,6)     --->  表示是从第3个字段里的第6个字符开始，一直到结尾  