## 1.anaconda默认源太慢
anaconda的默认源在下载安装相应包的时候，速度很慢，碰到包稍微大一点，基本就慢得让人无法接受。因此可以更改一下源的配置，提高效率。  

## 2.查看conda版本
执行下面的命令  

```
conda --version
conda 4.8.2
```  

可以查看到本地的conda版本，表明此时conda安装成功。  
如果没有成功显示，重新配置一下环境变量即可。  
修改.bash_profile配置文件  
```
export PATH="anaconda的路径"
```  

## 3.修改.condarc的配置
用vim打开~/.condarc文件。如果没有，生成对应的文件即可。  
编辑上述文件，加入对应的源  

```
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
show_channel_urls: true
```  

~/.condarc文件里只需上述三行即可。  

修改完上述配置以后，此时重新安装新的包速度很快，亲测有效！  

## 4.验证修改是否成功

```
conda info

     active environment : base
    active env location : /Users/wanglei/anaconda3/anaconda3
            shell level : 1
       user config file : /Users/wanglei/.condarc
 populated config files : /Users/wanglei/.condarc
          conda version : 4.8.2
    conda-build version : 3.18.11
         python version : 3.7.6.final.0
       virtual packages : __osx=10.15.3
       base environment : /Users/wanglei/anaconda3/anaconda3  (writable)
           channel URLs : https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/osx-64
                          https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/noarch
          package cache : /Users/wanglei/anaconda3/anaconda3/pkgs
                          /Users/wanglei/.conda/pkgs
       envs directories : /Users/wanglei/anaconda3/anaconda3/envs
                          /Users/wanglei/.conda/envs
               platform : osx-64
             user-agent : conda/4.8.2 requests/2.22.0 CPython/3.7.6 Darwin/19.3.0 OSX/10.15.3
                UID:GID : 501:20
             netrc file : None
           offline mode : False
```  

关注一下channel URLs字段，可以发现已经变成我们添加的源，说明已经生效。