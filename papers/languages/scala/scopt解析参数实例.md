## 1.简介
scopt是github上有人开发的一个用来解析参数的轻量级小工具，对于日常解析参数的场景基本够用，项目中使用也比较多，现在稍微记录一下用法。  

## 2.依赖
在pom.xml文件中加入以下依赖  

```
        <dependency>
            <groupId>com.github.scopt</groupId>
            <artifactId>scopt_2.10</artifactId>
            <version>3.2.0</version>
        </dependency>
```  


## 3.例子
直接上代码先  

```
object ScoptTest {
	
	case class Params(
						 input: String = "input",
						 output: String = "output",
						 index: Int = 0,
						 partitionnum: Int = 2,
						 debug: Boolean = false)
	
	
	val parser = new scopt.OptionParser[Params]("test") {
		head("this is a test for scopt params")
		
		opt[String]('i', "input").required().action {
			(x, c) => c.copy(input = x)
		}.text("default of input is input")
		
		opt[String]('o', "output").required().action {
			(x, c) => c.copy(output = x)
		}.text("default of output is output")
		
		opt[Int]("index").optional().action {
			(x, c) => c.copy(index = x)
		}.text("default of index is 0")
		
		opt[Int]("partitionnum").optional().action {
			(x, c) => c.copy(partitionnum = x)
		}.text("default of partitionnum is 2")
		
		opt[Boolean]("debug").optional().action {
			(x, c) => c.copy(debug = x)
		}.text("default of debug is false")
	}
	
	def init(args: Array[String]) = {
		val params = parser.parse(args, Params()).get
		println(params.input)
		println(params.output)
		println(params.index)
		println(params.partitionnum)
		println(params.debug)
	}
	
	def main(args: Array[String]): Unit = {
		init(args)
	}
	
}
```  

首先我们先写一个case class，里面加入各种我们需要的参数。  
然后生成一个parser对象，解析传入的参数即可。  


将上面的代码run起来，如果不传入input与output这两必须参数，会有如下提示  

```
Error: Missing option --input
Error: Missing option --output
this is a test for scopt params
Usage: test [options]

  -i <value> | --input <value>
        default of input is input
  -o <value> | --output <value>
        default of output is output
  --index <value>
        default of index is 0
  --partitionnum <value>
        default of partitionnum is 2
  --debug <value>
        default of debug is false
```  

传入如下参数

```
-i input1 -o output2
```  

代码运行的结果为  

```
input1
output2
0
2
false
```  
