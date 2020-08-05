## 1.Override is not allowed when implementing interface method 
这是由于module的language level是6以下，我们需要修改module的language的level为6或6以上：  
 
File->Project Structure->Project Settings -> Modules -> 选择所在的module -> 修改Language level为6或6以上 。修改设置完成以后，最好重启项目。   

## 2.Error:java: Compilation failed: internal java compiler error 
很明显这个问题是由jdk的版本不一致引起的。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/intellij/1.png)    

按图所示的位置设置Project bytecode version即可。