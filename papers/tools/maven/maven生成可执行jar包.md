maven有两种生成可执行jar包的插件，能够自动加载依赖包。现在我们就针对这两种插件来分别说明。  

## 1.maven-assembly-plugin
为了简单方便，利用maven的assembly插件将依赖的jar包都打包到一个jar中。这样无论拷贝到哪里，直接运行即可，不需要修改任何配置与代码。    

看一个assembly的使用实例：  

```
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>2.6</version>
                <executions>
                    <execution>
                    <!--绑定到package的生命周期上 -->
                        <phase>package</phase>
                        <goals>
                            <goal>attached</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                    <archive>
                        <manifest>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
```  

assembly的配置项非常多，这里只用了很简单的几个，具体配置可以查阅相关文档。  

##2.appassembler-maven-plugin
appassembler-maven-plugin 的优势是能够自动生成window和linux的启动脚本，省去了自己再另写一个脚本的时间。而前面maven-assembly-plugin 生成jar包后需要执行 java -jar **.jar命令运行jar包。  
 
同样看一个实例  

```
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>appassembler-maven-plugin</artifactId>
                <version>1.1.1</version>
                <executions>
                    <execution>
                        <id>make-assembly</id>
                        <phase>package</phase>
                        <goals>
                            <goal>assemble</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
	                <!-- 配置文件的目标目录 -->
                    <configurationDirectory>conf</configurationDirectory>
                    <!-- 从哪里拷贝配置文件 (默认src/main/config) -->
                    <configurationSourceDirectory>conf</configurationSourceDirectory>
                    <!-- 拷贝配置文件到上面的目录中 -->
                    <copyConfigurationDirectory>true</copyConfigurationDirectory>
                    <includeConfigurationDirectoryInClasspath>true</includeConfigurationDirectoryInClasspath>
					<!-- lib目录中jar的存放规则，默认是${groupId}/${artifactId}的目录格式，flat表示直接把jar放到lib目录 -->
                    <repositoryLayout>flat</repositoryLayout>
                    <!-- 打包的jar，以及maven依赖的jar放到这个目录里面 -->
	                <repositoryName>lib</repositoryName>       
	                <!-- 根目录 -->
	                <assembleDirectory>${project.build.directory}/${project.artifactId}-${project.version}</assembleDirectory>

                    <binFileExtensions>
                        <unix>.sh</unix>
                    </binFileExtensions>
                    <platforms>
                    <!-- 生成linux平台的执行脚本 -->
                        <platform>unix</platform>
                    </platforms>

                    <extraJvmArguments>
                        -Xmx8000m
                        -Djava.security.krb5.conf=$BASEDIR/conf/krb5.conf
                        -Dhadoop.property.hadoop.client.keytab.file=$BASEDIR/conf/h_message_push.keytab
                        -Dhadoop.property.hadoop.client.kerberos.principal=h_message_push@XIAOMI.HADOOP
                        -Dhadoop.property.hadoop.security.authentication=kerberos
                    </extraJvmArguments>
                    <programs>
                        <program>
                            <mainClass>XXX</mainClass>
                            <name>XXXXX</name>
                        </program>
                    </programs>
                </configuration>
            </plugin>
```  

如同前面提到的，在pom里面添加appassembler-maven-plugin打包完成以后，会自动生成一个bin目录，bin里面就包含有运行XXX主类的.sh脚本。  