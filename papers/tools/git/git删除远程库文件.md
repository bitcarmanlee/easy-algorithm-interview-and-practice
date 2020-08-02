项目开发初期由于.gitignore 文件配置不正确很有可能导致某些不需要的目录上传到 git 远程仓库上了，这样会导致每个开发者提交的时候这些文件每次都会不同。当然最稳妥的方案是一开始就配置好.gitignore，但是如果这种情况发生了该怎么办呢？  

## 1.删除远程库文件,但本地保留该文件

```
git rm --cached xxx
git commit -m "remove file from remote"
git push -u origin master
```  

## 2.删除远程库文件夹,但本地保留该文件夹


```
git rm --cached -r xxx
git commit -m "remove file from remote"
git push -u origin master
```  

加上参数-r，递归删除该文件夹。  

## 3.git rm与git rm --cached 的区别
git rm 是删除暂存区或分支上的文件, 同时也删除工作区中这个文件。  
git rm --cached是删除暂存区或分支上的文件,但本地还保留这个文件， 是不希望这个文件被版本控制。

