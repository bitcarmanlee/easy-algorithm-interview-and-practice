在python中想用graphviz画图的时候，发现报了如下异常：  

```
RuntimeError: failed to execute ['dot', '-Tpdf', '-O', 'test'], make sure the Graphviz executables are on your systems' path
```  

很奇怪啊。python里面明明已经安装好了graphviz。。。  
经过google搜索，发现是系统也需要安装graphviz。。。  

```
sudo apt-get install graphviz
```  

系统安装graphviz完毕以后，代码就可以正常运行。  
