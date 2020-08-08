公司配的机器操作系统是ubuntu，自己在ubuntu上面用VirtualBox装了个windows的虚拟机。有时候需要从windows传一些文件到ubuntu上面。最开始使用的是虚拟机的share功能。后来使用一段时间以后发现，share功能很多时候并不是很好用。所以干脆在windows上装一个ssh工具用来传输文件。  

## 1.确认ubuntu的ssh-server开启
ssh是分客户端与服务端的。为了实现从windows传文件到ubuntu的功能，需要确保ubuntu的ssh-server是开启可用的，要不别的机器怎么连你的机器。。。    
如果ubuntu上面没有安装ssh-server，则先安装    

```
sudo apt install openssh-server
```  

安装完毕以后，手动启动server  

```
/etc/init.d/ssh start
```  

如果要停止，则可按如下操作  

```
/etc/init.d/ssh stop
```  

在我本机上查看ssh相关的进程：  

```
ps -ef | grep ssh
...
root     25483     1  0 17:25 ?        00:00:00 /usr/sbin/sshd -D
```  

再查看一下ssh占用的端口  

```
sudo netstat -anp | grep 25483
...
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      25483/sshd 
```  

可以看出ssh占用了22端口  

## 2.windows上下载ssh客户端
随便找一个windows上的ssh客户端下载，安装即可。  

## 3.连接ubuntu
打开ssh客户端，连上ubuntu的机器。  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/tools/shell/1.png)    

填入host的ip，用户名，然后点connect，输入密码即可。  