## 浮点数误差
浮点数一个普遍的问题就是在计算机的世界中，浮点数并不能准确地表示十进制。并且，即便是最简单的数学运算，也会带来不可控制的后果。因为，在计算机的世界中只认识0与1。  

```
>>> x = 4.20
>>> y = 2.10
>>> x + y
6.3000000000000007
>>> (x+y) == 6.3
False
>>> x = 1.2
>>> y = 2.3
>>> x + y
3.5
>>> (x + y) == 3.5
True
```  

上述种种问题，就来自于计算机的cpu与浮点数的表示方式，我们自己在代码层面是没法控制的。在有些需要精确表示浮点数的场合，例如财务结算，这些误差就不可接受。  

## decimal模块进行十进制数学计算
python中的decimal模块可以解决上面的烦恼  
decimal模块中，可以通过整数，字符串或原则构建decimal.Decimal对象。如果是浮点数，特别注意因为浮点数本身存在误差，需要先将浮点数转化为字符串。  

```
>>> from decimal import Decimal
>>> from decimal import getcontext
>>> Decimal('4.20') + Decimal('2.10')
Decimal('6.30')
>>> from decimal import Decimal
>>> from decimal import getcontext
>>> x = 4.20
>>> y = 2.10
>>> z = Decimal(str(x)) + Decimal(str(y))
>>> z
Decimal('6.3')
>>> getcontext().prec = 4 #设置精度
>>> Decimal('1.00') /Decimal('3.0')
Decimal('0.3333')
```  

当然精度提升的同时，肯定带来的是性能的损失。在对数据要求特别精确的场合（例如财务结算），这些性能的损失是值得的。但是如果是大规模的科学计算，就需要考虑运行效率了。毕竟原生的float比Decimal对象肯定是要快很多的。  