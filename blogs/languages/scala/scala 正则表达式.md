正则表达式是所有攻城狮尤其是算法，数据相关攻城狮必备的技能。日常工作中免不了处理各种字符串与字符串操作，写好正则表达式能大幅度提高工作效率，提升工作愉悦度。现在就简单总结一下scala中常见的正则表达式用法。  

如果有对正则表达式不熟悉的同志们，可以查看[正则表达式30分钟入门教程](https://deerchao.net/tutorials/regex/regex.htm)。  

## 1.匹配电话号码
匹配电话号码是我们常见的需求之一。代码如下：  

```
    def reg() = {
        val PHONE_PATTERN = """1(([3,5,8]\d{9})|(4[5,7]\d{8})|(7[0,6-8]\d{8}))""".r
        val num = "13566513245"
        val res = PHONE_PATTERN.findFirstIn(num).get
        println(res)
    }
```  

在这里，"""表示raw string，三引号括起来的字符串表示不需要转义。因为正则表达式本身比较长，可读性也比较差，所以用三引号可以降低阅读难度，并且缩短字符串长度。  

## 2.匹配小写字母  

```
    def reg2() = {
        val str = "abc"
        val pattern = new Regex("[a-z]+")
        println(pattern.findFirstIn(str).get)
    }
```  

## 3.匹配所有英文字母

```
    def reg3() = {
        val str = "abcDEFg"
        //val pattern = new Regex("(?i)[a-z]+")
        val pattern = new Regex("[a-zA-Z]")
        println(pattern.findAllIn(str).mkString(""))
    }
```  

注意pattern的两种写法都可以。  

## 4.匹配email

```
    def reg4() = {
        val str = "email:leilei@mi.com.cn"
        val pattern = new Regex("""(?i)[a-z0-9._-]+@[a-z0-9._-]+(\.[a-z0-9._-]+)+""")
        println(pattern.findAllIn(str).mkString(""))
    }
```  

## 5.匹配日期，并提取年月日

```
    def reg5() = {
        val str = "2017-01-01"
        val datePattern = new Regex("""(\d{4})-(\d{2})-(\d{2})""")
        val datePattern(year, month, day) = str
        println(year, month, day)

        str match {
            case datePattern(year, month, day) => println(s"year is $year.\n" +
                f"month is $month.\n" + raw"day is $day")
        }
    }
```  

正则表达式中，小括号表示分组的概念。从上面的例子可以看出，scala正则中提取分组可以采用两种方式，都很方便。模式匹配的方式可能更直观，更符合scala的习惯。  

## 6.非铆定

```
    def reg7() = {
        val datePattern = new Regex("""(\d{4})-(\d{2})-(\d{2})""")
        val pattern = datePattern.unanchored
        val str = "Date: 2017-05-21 19:25:18"
        
        str match {
            case pattern(year, month, day) => println(s"year is $year.\n" +
                f"month is $month.\n" + raw"day is $day")
        }
    }
```  

如果要非铆定，可以使用上面的用法。  
