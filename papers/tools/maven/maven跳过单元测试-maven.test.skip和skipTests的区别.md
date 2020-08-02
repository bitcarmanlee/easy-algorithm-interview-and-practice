-DskipTests，不执行测试用例，但编译测试用例类生成相应的class文件至target/test-classes下。  

-Dmaven.test.skip=true，不执行测试用例，也不编译测试用例类。  

不执行测试用例，但编译测试用例类生成相应的class文件至target/test-classes下。  

## 1.maven.test.skip
使用maven.test.skip，不但跳过单元测试的运行，也跳过测试代码的编译。  
```
mvn package -Dmaven.test.skip=true  
```  

也可以在pom.xml文件中修改  

```
<plugin>  
    <groupId>org.apache.maven.plugin</groupId>  
    <artifactId>maven-compiler-plugin</artifactId>  
    <version>2.1</version>  
    <configuration>  
        <skip>true</skip>  
    </configuration>  
</plugin>  
<plugin>  
    <groupId>org.apache.maven.plugins</groupId>  
    <artifactId>maven-surefire-plugin</artifactId>  
    <version>2.5</version>  
    <configuration>  
        <skip>true</skip>  
    </configuration>  
 </plugin> 
```  

## 2.DskipTests
使用 mvn package -DskipTests 跳过单元测试，但是会继续编译；如果没时间修改单元测试的bug，或者单元测试编译错误。使用上面的，不要用这个  

```
<plugin>  
    <groupId>org.apache.maven.plugins</groupId>  
    <artifactId>maven-surefire-plugin</artifactId>  
    <version>2.5</version>  
    <configuration>  
        <skipTests>true</skipTests>  
    </configuration>  
</plugin> 
```
