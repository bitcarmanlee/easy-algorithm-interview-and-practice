## 1.前言
虽然用python有一些年头了，但是在处理中文字符串的时候还是经常会遇到UnicodeEncodeError，UnicodeDecodeError等问题。每次都是随便调一调，程序能正常run以后就不管了。不巧今天又遇到了同样的状况，于是痛下决心，一定要把python中的字符编码问题搞清楚。  

## 2.字节与字符  
计算机存储的任何数据，包括各种文本、图片、音视频文件等等，实际上都是一串二进制数字01字节序列组成的。相信大家都知道，一个字节Byte(B)是8个比特bit(b)。  

而字符，自然就是符号了。比如说二十六个英文字母，阿拉伯数字，以及在python中最坑爹的汉字都是字符。python中遇到的字符编码问题，大部分都与汉字有关系。  

写过java的小伙伴都知道，java中的IO模块，从大的方向来说，就可以分为字节流与字符流。字节流包括InputStream与OutputStream，字符流包括Writer与Reader。  

有的同学会有疑问，为什么要搞这么复杂？统一用字节或者字符不就行了？  

字节一般用来存储与网络传输，这样可以节省存储空间与网络传输带宽。而字符主要是用于显示，方便大家阅读。试想你正在debug，结果所有的输出是一堆01011100这种，那你还不得疯了。  

## 3.编码(encoding)与解码(decoding)
字符编码（Character encoding）、字集码是把字符集中的字符编码为指定集合中某一对象（例如：比特模式、自然数序列、8位组或者电脉冲），以便文本在计算机中存储和通过通信网络的传递。常见的例子包括将拉丁字母表编码成摩斯电码和ASCII。其中，ASCII将字母、数字和其它符号编号，并用7比特的二进制来表示这个整数。通常会额外使用一个扩充的比特，以便于以1个字节的方式存储。(参考文献1)  

encoding是将字符转换为字节，那么反过来将字节转换为字符则是decoding，两者是可逆的。编码主要是为了存储传输，而解码是为了方便阅读。  

## 4.utf-8与unicode区别
在正式讲python字符编码问题之前，还需要先扯清除unicode跟utf-8的关系。  
简单来说，unicode是一个字符集，而utf-8是一个编码规则，两者并不是同一维度的东西。  
字符集：为每一个字符分配一个唯一的 ID（学名为码位 / 码点 / Code Point）  
编码规则：将码位转换为字节序列的规则（编码/解码 可以理解为 加密/解密 的过程）  


## 4.python 2.7中的字符串
python2x中的字符串实际有两种类型: str与unicode。很多时候出现的各种问题，就是出现在这上面。  
下面我们在python解释器中简单测试一下  
```
>>> s = "你好"
>>> s
'\xe4\xbd\xa0\xe5\xa5\xbd'
>>> type(s)
<type 'str'>
```  
上面的代码可以看出，s是str类型，在内部的存储方式就是一堆01二进制字节序列，显示出来是一串十六进制字符。  
很多时候我们看到定义字符串的时候会在前面加上一个前缀u，这个u其实就是表示这个字符串是unicode形式：  

```
>>> s = u"你好"
>>> s
u'\u4f60\u597d'
>>> type(s)
<type 'unicode'>
```  

我们看看编码的过程，大家记住编码是从字符->字节  

```
>>> s = u"你好"
>>> s
u'\u4f60\u597d'
>>> type(s)
<type 'unicode'>
>>> s.encode('utf-8')
'\xe4\xbd\xa0\xe5\xa5\xbd'
```  

再看看解码过程，解码自然就是从字节-> 字符  

```
>>> s = "你好"
>>> s
'\xe4\xbd\xa0\xe5\xa5\xbd'
>>> type(s)
<type 'str'>
>>> s.decode("utf-8")
u'\u4f60\u597d'
```  

## 5.UnicodeEncodeError  
既然是UnicodeEncodeError，那么应该是在字符->字节的环节出现了问题。来看下面的例子。  

```
def t1():
    f = open("ttt", "w")
    u1 = u'你好'
    f.writelines(u1 + "\n")

t1()
```  

运行这段代码以后，会有如下问题：  

```
TypeError: writelines() argument must be a sequence of strings
```  

这个问题比较好解释，writelines方法需要的是一个字符串序列，而u1是个unicode。  
将代码稍作修改  

```
def t1():
    f = open("ttt", "w")
    u1 = u'你好'
    f.write(u1)

t1()
```  

```
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```  

调用write方法时，如果传入的是字符串，就直接将该str写入文件，无需编码，因为str本身就是一堆二进制的01字节序列。  
如果是unicode，那需要先用encode方法将unicode字符串转换为二进制形式的str，才能保存。  

重点来了，刚刚我们有提到，unicode -> str是encode过程。既然是encode，肯定需要指定encode的方法，比如最常用的utf-8。坑爹就在于，python2中如果不指定encode的形式，默认是用ASCII码来进行编码。  
很明显，ASCII只有128个拉丁字母，是木有处理中文字符能力的。所以报错里面的信息就是`ordinal not in range(128)`  

解决方法很简单，将encode方式指定为utf-8即可。  

```
def t1():
    f = open("ttt", "w")
    u1 = u'你好'.encode("utf-8")
    f.write(u1)

t1()
```  

## 6.UnicodeDecodeError  
与UnicodeEncodeError对应的，UnicodeDecodeError肯定就是出现在字节->字符的环节。  

```
def t2():
    u1 = u"啦啦啦"
    print repr(u1)
    byte1 = u1.encode("utf-8")
    print repr(byte1)
    byte1.decode("gbk")

t2()
```  

```
u'\u5566\u5566\u5566'
'\xe5\x95\xa6\xe5\x95\xa6\xe5\x95\xa6'
...
UnicodeDecodeError: 'gbk' codec can't decode byte 0xa6 in position 8: incomplete multibyte sequence
```  
把一个经过 UTF-8编码后生成的字节序列 '\xe5\x95\xa6\xe5\x95\xa6\xe5\x95\xa6'用GBK解码成unicode的时候，因为GBK编码只有两字节，而UTF-8是三字节，多出来一个字节，肯定无法解析。因此，要防止出现UnicodeDecodeError，主要就是保持编码与解码的时候所用的编码方式一致。  

## 7.coding:utf-8
python代码在开头位置，一般都有这么一行：  

```
# -*- coding: utf-8
```  

作用是定义源代码的编码. 如果没有定义, 此源码中是不可以包含中文字符串的.  

## 8.setdefaultencoding
在源码中经常还可以看到如下代码:

```
import sys
reload(sys)
sys.setdefaultencoding('utf8')
```  
上面几行代码的作用是设置默认的string的编码格式为utf8，在2.7以后已经不推荐使用这种方式了  




参考文献
1.https://zh.wikipedia.org/wiki/%E5%AD%97%E7%AC%A6%E7%BC%96%E7%A0%81