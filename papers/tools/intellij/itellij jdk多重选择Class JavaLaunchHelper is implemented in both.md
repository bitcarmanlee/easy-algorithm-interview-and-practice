## 1.问题描述
intellij运行java代码时，提示如下问题  

```
objc[xxx]: Class JavaLaunchHelper is implemented in both xxx and xxx. One of the two will be used. Which one is undefined.
```  

## 2.问题解决
问题描述得比较清楚了，是系统中现在有两个JDK，intellij不知道选择哪个。所以重新配置一下就好  

### 2.1 打开idea.properties文件
点击help -> edit custom properties。如果系统中没有该文件，IDE会提示你是否创建该文件。  

### 2.2 修改文件
在文件后面添加一行  

```
idea.no.launcher=true
```  

## 2.3 重启IDE
重启IDE即可。  
