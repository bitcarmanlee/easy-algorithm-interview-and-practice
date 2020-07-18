机器中的tensorflow版本有点老旧，想升级一下，发现用  

```
pip install --upgrade --ignore-installed tensorflow
```  
升级并没有奏效  

于是使用  

```
pip uninstall tensorflow
```  
先将老版本卸载，然后再重新安装：  

```
pip install tensorflow
```  
不过发现装上去的还是原来的旧版本。  
找了一下解决方案：  

```
pip install tensorflow=1.6
```  
后面接上要安装的版本号即可。  