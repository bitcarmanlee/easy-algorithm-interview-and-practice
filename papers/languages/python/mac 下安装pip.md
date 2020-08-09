pip是常用的python包管理工具，类似于java的maven。用python的同学，都离不开pip。  
在新mac中想用home-brew安装pip时，遇到了一些小问题：  

```
bogon:~ wanglei$ brew install pip
Error: No available formula with the name "pip"
Homebrew provides pip via: `brew install python`. However you will then
have two Pythons installed on your Mac, so alternatively you can install
pip via the instructions at:

  https://pip.readthedocs.org/en/stable/installing/#install-pip
```  

由此可见，在home-brew中，pip的安装是跟python一起的。  

换种方式：  

```
bogon:~ wanglei$ sudo easy_install pip
Password:
Searching for pip
Reading https://pypi.python.org/simple/pip/
...
```  

稍等片刻，pip就安装完毕。。。  