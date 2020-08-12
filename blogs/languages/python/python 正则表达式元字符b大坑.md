在所有介绍正则表达式元字符的资料中，都会提到\b，表示单词边界的意思。在python里写了一段小测试代码测试一下\b:  

```
#!/usr/bin/env python

import re

def t1():
    pattern = re.compile("\bprint\b")
    search = pattern.search('aaa print 123 hello')
    if search:
        print search.group(0)
    else:
        print "NO"

t1()
```  

运行此脚本以后，控制台华丽丽地输出一个大大的"NO",瞬间懵逼了。咋回事，难道我理解能力太差。又换了好多种自认为没问题的方式，都华丽丽地跟预期不对头。  

经过长时间的google（百度你是查不出来滴骚年们），终于找到了问题所在。各位同学请先看代码：  

```
#!/usr/bin/env python

import re

def t2():
    pattern = re.compile(r"\bprint\b")
    search = pattern.search('aaa print 123 hello')
    if search:
        print "YES"
        print search.group(0)
    else:
        print "NO"

t2()
```  

各位看官看出区别来了么。没错，就"\bprint\b"前头多了个"r"。为什么会酱紫呢。  

这是python字符串与正则表达式最糟糕，没有之一的冲突。在python字符串中，"b"是反斜杠字符，ASCII值是8。如果你没有使用 raw 字符串时，那么 Python 将会把 "\b" 转换成一个回退符，你的 RE 将无法象你希望的那样匹配它了。  
所以同学们，在使用python做正则的时候，当你想使用\b元字符的时候，一定得注意咯。怎么做，不用我再说了吧。  
为了解决这个问题，花了大概得有一个半小时查资料。所以虽然时间已经很晚了，还是赶紧记下来再睡觉，心里才踏实。  