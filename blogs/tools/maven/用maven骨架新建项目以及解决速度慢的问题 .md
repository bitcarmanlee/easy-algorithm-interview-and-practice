用maven中的命令行方式可以新建一个maven项目。命令行如下：  

```
mvn archetype:generate \
-DgroupId=edu.bit.auto \
-DartifactId=test \
-DarchetypeArtifactId=maven-archetype-quickstart \
-DinteractiveMode=false
```  

当然，执行上面命令的时候需要将mvn加入到PATH中。  
将命令行执行后，一直卡在如下界面中：  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/maven/1.png)  

显示出来一直在`Generating project in Batch mode`  

为了看清楚到底是发生了什么，加上-X选项看看log，最靠谱的还是log大法：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/maven/2.png)  

原来一直是在maven的中央仓库里找archetype-catalog.xml。你懂的。  
那怎么绕过去这个坑呢？  
解决方案也比较容易。先看自己的maven本地仓库里有没有archetype-catalog.xml。默认的位置为`~/.m2/repository/org/apache/maven/archetype/archetype-catalog`。可能下面还有一层版本信息的路径，然后cd进去，看看有没有`archetype-catalog-2.4.pom` 文件(我的版本是2.4)。如果没有，下载对应的archetype-catalog.xml让如相应的位置。然后在命令行后面加上一个选项`-DarchetypeCatalog=local`。最后执行相应的命令行即可。  

命令执行完毕以后，用tree命令看看生成的内容：  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/maven/3.png)  

可以看到，跟我们在IDE里生成的项目结构是一样的，都会自动生成一个App.java与AppTest.java的类！  

再进去看看pom的内容：  

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"                                                                                                     
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.bit.auto</groupId>
  <artifactId>test</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>test</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>

```  

这样一来，通过命令行的方式，自动生成maven项目，减少了pom.xml以及项目本身结构出错的可能！  
