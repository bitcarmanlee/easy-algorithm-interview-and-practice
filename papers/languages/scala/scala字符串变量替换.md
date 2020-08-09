在scala中，字符串可以带s,f,raw前缀。这几个前缀都可以用来进行变量替换。下面来简单分析实验一下。  

## 1.s前缀
s前缀的作用就是用来表示变量替换。  

```
    def test() = {
        val word = "hello"
        println(s"$word, world")
    }
```  

函数运行的结果为：  

```
hello, world
```  

## 2.f前缀
f前缀在表示变量替换的同时，还可以在变量名后面添加格式化参数。  
```
    def test() = {
        val year1 = 2017
        println(f"hello, $year1%.2f")
        val year2 = "2017"
        println(f"hello, $year2%.3s")
    }
```  

输出的结果为：  

```
hello, 2017.00
hello, 201
```  

## 3.raw前缀
raw前缀在表示变量替换的同事，不对特殊字符转义。  

```
    def t6() = {
        val year = 2017
        println(raw"hello\t$year")
    }
```  

输出结果为：  

```
hello\t2017
```  
