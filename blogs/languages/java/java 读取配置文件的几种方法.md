比如我们有以下目录  

```
|--project
    |--src
        |--javaapplication
            |--Test.java
            |--file1.txt
        |--file2.txt
    |--build 
        |--javaapplication
            |--Test.class
            |--file3.txt
        |--file4.txt
```  

 
在上面的目录中，有一个src目录，这是JAVA源文件的目录，有一个build目录，这是JAVA编译后文件(.class文件等）的存放目录  
那么，我们在Test类中应该如何分别获得  
file1.txt  file2.txt  file3.txt  file4.txt这四个文件呢？  
 
首先讲file3.txt与file4.txt  
file3.txt:  
方法一：  
``` 
File file3 = new File(Test.class.getResource("file3.txt").getFile());
```  

方法二：  

```
File file3 = new File(Test.class.getResource("/javaapplication/file3.txt").getFile());
```  

方法三：  

```
File file3 = new File(Test.class.getClassLoader().getResource("javaapplication/file3.txt").getFile());
```  

 
file4.txt:  
方法一：  

```
File file4 = new File(Test.class.getResource("/file4.txt").getFile());
```  

方法二：  

```
File file4 = new File(Test.class.getClassLoader().getResource("file4.txt").getFile());
```  

 
很好，我们可以有多种方法选择，但是file1与file2文件呢？如何获得？  
答案是，你只能写上它们的绝对路径，不能像file3与file4一样用class.getResource()这种方法获得，它们的获取方法如下  
假如整个project目录放在c:/下，那么file1与file2的获取方法分别为  
file1.txt  
方法一：  

```
File file1 = new File("c:/project/src/javaapplication/file1.txt");
```  

方法二：。。。没有  
 
file2.txt  
方法一：  

```
File file2 = new File("c:/project/src/file2.txt");
```  

方法二：。。。也没有  
 
重点注意地方：  
总结一下，就是你想获得文件，你得从最终生成的.class文件为着手点，不要以.java文件的路径为出发点，因为真正使用的就是.class，不会拿个.java文件就使用，因为java是编译型语言嘛  

至于getResouce()方法的参数，你以class为出发点，再结合相对路径的概念，就可以准确地定位资源文件了，至于它的根目录嘛，你用不同的IDE build出来是不同的位置下的，不过都是以顶层package作为根目录，比如在Web应用中，有一个WEB-INF的目录，WEB-INF目录里面除了web.xml文件外，还有一个classes目录，没错了，它就是你这个WEB应用的package的顶层目录，也是所有.class的根目录“/”，假如clasaes目录下面有一个file.txt文件，它的相对路径就是"/file.txt"，如果相对路径不是以"/"开头，那么它就是相对于.class的路径。。  
 
还有一个getResourceAsStream()方法，参数是与getResouce()方法是一样的，它相当于你用getResource()取得File文件后，再new InputStream(file)一样的结果。getResource().getFile()得到的是文件的string，例如可以这么写：  

```
File file = new File(Demo01.class.getResource("/a.properties").getFile());
```  

而getResourceAsStream()方法返回的是一个inputStream,例如可以这么写:  

```
InputStream in = Demo01.class.getResourceAsStream("/a.properties");
```  
