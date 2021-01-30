## 0.前言
自己的macos上一直没有安装上xgboost，最近因为工作需要，想在macos上安装一下xgboost。  
本来以为是个很简单的事情，没想到还是费了一些波折，特意记录一下  

## 1. 直接安装失败
最开始直接使用  

```
pin install xgboost
```  
安装，安装过程没啥问题。但是安装完毕，使用过程中出现了问题。  

```
import xgboost as xgb
```  
导入xgboost以后，直接报错  

```
xgboost.core.XGBoostError: XGBoost Library (libxgboost.dylib) could not be loaded.
Likely causes:
  * OpenMP runtime is not installed (vcomp140.dll or libgomp-1.dll for Windows, libgomp.so for UNIX-like OSes)
  * You are running 32-bit Python on a 64-bit OS
....
```  

查了一下原因，大致原因如下：  
Xgboost模型本身支持多线程运行，即用多个cpu线程进行训练；  
但是，默认的apple clang编译器不支持openmp，因此使用默认编译器将禁用多线程。  

## 2.解决方式1
又搜了下网上的解决方式，大部分的套路都是这样：  
先升级homebrew，然后通过homebrew安装更高版本的gcc，再去gitclone xgboost源码，build源码，再安装。  

结果发现不管是升级homebrew，还是安装gcc，gitclone源码，每一步都难如登天，老铁们懂的.  

所以这是种可行的方式，但是堪称地狱难度，直接放弃了。  

## 3.解决方式2
搜索的过程中发现有个老哥直接给了一行代码就可以解决问题  

```
conda install py-xgboost
```  

有几个帖子反映该方法简单粗暴好使，于是抱着试一试的想法试了下。  
结果conda掉链子了。  

```
Solving environment: failed with initial frozen solve. Retrying with flexible solve.
......
```  


## 4.接上conda的链子
conda的问题，比较明显是source的问题。不禁又是一声叹息...  
找了半天，试了N多源，发现都不奏效。  
最后认真看了下清华开源镜像站的anaconda页面，抱着试试看的心态，把官网上的配置粘到本地的.condarc文件  

```
channels:
  - defaults
show_channel_urls: true
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```  


清华开源镜像站的anaconda链接：  
[清华anaconda镜像](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)  

看到这里其实有点小小的感慨，国内IT产业如火如荼，但是这种重要而且基本的东西，居然是一个学校的学生凭自己的兴趣爱好在自发维护.....  

## 5.大功告成
将conda的配置修改完毕，再执行安装命令  

```
conda install py-xgboost
```  

发现大功告成，可以在本地正常运行xgb相关的代码。  
后面有时间再稍微查查这个py-xgboost有啥特别的地方。  