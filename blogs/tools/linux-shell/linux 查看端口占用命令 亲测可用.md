端口是系统非常重要的一个东东，我们经常需要查看哪个进程占用了哪个端口，或者哪个端口被哪个进程占用。废话不多说，直接上干货，教大家怎样查看系统端口占用情况。  

方法一：  
1.先用`ps -ef | grep xxx(某个进程)`，可以查看某个进程的pid。  
2.再用`netstat -anp | grep pid号`，可以查看到该进程占用的端口号！  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/shell/2.png)    

方法二：  
直接用`lsof`命令可以查看端口使用情况！  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/shell/3.png)    