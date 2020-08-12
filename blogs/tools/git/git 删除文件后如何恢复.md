有时候不小心在git中rm了文件。怎么恢复呢？别急，咱们一步步来。  

首先git status一把，看看此时工作区的状态  
```
[xxx@xxx static_files]$ git status
# On branch master
nothing to commit (working directory clean)
```  

可见此时没有任何修改的内容。  
再看看具体有什么  

```
xxx@xxx static_files]$ ls
abbr_data  breakfast_data  room_type_data
```  
此时总计有三个文件。OK，让我们干掉其中一个  

```
[xxx@xxx static_files]$ git rm abbr_data
rm 'static_files/abbr_data'
[xxx@xxx static_files]$ git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#	deleted:    abbr_data
#
[xxx@xxx static_files]$ ls
breakfast_data  room_type_data
```  
此时工作区的文件就只剩两个了，abbr_data这个文件，已经被我们干掉。    

如果我们想要恢复，怎么办呢？
  
```
[xxx@xxx static_files]$ git checkout -- abbr_data
error: pathspec 'static_files/abbr_data' did not match any file(s) known to git.
```  

直接checkout，是不行的。  
那怎么办呢？其实在git status中，已经告诉我们怎么办了。  

```
[xxx@xxx static_files]$ git reset HEAD abbr_data
Unstaged changes after reset:
M	static_files/abbr_data
```  

用reset命令，先将abbr_data这个文件找回来。  

```
[xxx@xxx static_files]$ git status
# On branch master
# Changed but not updated:
#   (use "git add/rm <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#	deleted:    abbr_data
#
no changes added to commit (use "git add" and/or "git commit -a")
```  

再checkout一把  

```
[xxx@xxx static_files]$ git checkout -- abbr_data
[xxx@xxx static_files]$
```  
看到checkout以后没有任何提示，这事就成了。因为git的哲学跟unix的哲学一样，没消息就是最好的消息。。。  

再ls一下，果然，abbr_data找回来了。  
```
[xxx@xxx static_files]$ ls
abbr_data  breakfast_data  room_type_data
```  
