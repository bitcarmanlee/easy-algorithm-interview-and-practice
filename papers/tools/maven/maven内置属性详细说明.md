Maven共有6类属性：  

## 1.内置属性(Maven预定义,用户可以直接使用)

`${basedir}`表示项目根目录,即包含pom.xml文件的目录;  
`${version}`表示项目版本;  
`${project.basedir}`同`${basedir}`;  
`${project.baseUri}`表示项目文件地址;  
`${maven.build.timestamp}`表示项目构件开始时间;  
`${maven.build.timestamp.format}`表示属性 `${maven.build.timestamp}`的展示格式,默认值为yyyyMMdd-HHmm,可自定义其格式,其类型可参考Java.text.SimpleDateFormat。用法如下：  

```
<properties>
<maven.build.timestamp.format>yyyy-MM-dd HH:mm:ss</maven.build.timestamp.format>
</properties>
```  

## 2.POM属性(使用pom属性可以引用到pom.xml文件对应元素的值)
`${project.build.directory}`表示主源码路径，缺省为target;  
`${project.build.outputDirectory}` 构建过程输出目录，缺省为target/classes  
`${project.build.sourceEncoding}`表示主源码的编码格式;  
`${project.build.sourceDirectory}`表示主源码路径;  
`${project.build.finalName}`表示输出文件名称，缺省为`${project.artifactId}-\${project.version}`;  
`${project.packaging}` 打包类型，缺省为jar;  
`${project.version}`表示项目版本,与`${version}`相同;  

## 3.自定义属性
在pom.xml文件的`$<properties>$`标签下定义的Maven属性  

```
<project>
  <properties>
    <my.pro>abc</my.pro>
  </properties>
</project>
```  

在其他地方使用`${my.pro}`使用该属性值。  

## 4.settings.xml文件属性
与pom属性同理,用户使用以settings.开头的属性引用settings.xml文件中的XML元素值  
`${settings.localRepository}`表示本地仓库的地址;  

## 5.Java系统属性
所有的Java系统属性都可以使用Maven属性引用  
使用mvn help:system命令可查看所有的Java系统属性;  
System.getProperties()可得到所有的Java属性;  
`${user.home}`表示用户目录;  

## 6.环境变量属性
所有的环境变量都可以用以env.开头的Maven属性引用  
使用mvn help:system命令可查看所有环境变量;  
`${env.JAVA_HOME}`表示JAVA_HOME环境变量的值;  