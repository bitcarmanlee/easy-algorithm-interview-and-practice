## 1.java中传递变长参数
在java中传递变长参数的方式为`...`，看个简单的实例  

```
    public static void argsTest(String... args) {
        for(String each: args) {
            System.out.println(each);
        }
    }

    public static void main(String[] args) {
        String s1 = "a", s2 = "b", s3 = "c";
        argsTest(s1, s2, s3);
    }
```  

## 2.scala中传递变长参数  
scala中也支持传递变长参数，而且比java中更简单，只需要在参数类型后面使用特殊符号"*"即可。同样看一个简单的例子  

```
    def findMax(values: Int*) = {
        values.foldLeft(values(0)) {
            (x, y) => Math.max(x, y)
        }
    }

    def main(args: Array[String]): Unit = {
        println(findMax(1, 3, 5, 2, 4, 6))
    }
```  
