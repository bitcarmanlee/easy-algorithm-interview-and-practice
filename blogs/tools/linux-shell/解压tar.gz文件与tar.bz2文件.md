解压tar.gz文件与tar.bz2文件的命令是不一样的。  
其中  
解压tar.gz的命令为  
`tar -zxvf ×××.tar.gz`  
解压tar.bz2的命令为  
`tar -jxvf ×××.tar.bz2`  
主要区别在于，一个参数为-z，一个参数为-j。  
-z即询问是否有gzip属性，-j询问是否有bzip2属性  