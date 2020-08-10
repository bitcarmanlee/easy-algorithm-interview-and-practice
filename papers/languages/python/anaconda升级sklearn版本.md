调用sklearn的model_selection时，发现sklearn中没有model_selection的模块。经过检查，发现anaconda中的sklearn版本太低，为0.17版本。于是，开始了sklearn的升级之旅。  

## 1.查看原有版本
首先使用`conda list`命令，查看一下现有的版本：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/updatesklearn/1.png)    

果不其然，版本是0.17.1，版本太低，果断开始升级。  

## 2.升级到最新版本
使用`conda update scikit-learn`命令，更新sklearn的版本。更新之前，会提示将更新到什么版本。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/updatesklearn/2.png)    

可以看出最新的版本为0.19.0  

然后确认，开始更新。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/updatesklearn/3.png)  

由于此次更新需要更新的包很多，并且很大，所以需要等相当长的时间。。。  

等更新完毕以后，再使用model_selection包，就OK了.  