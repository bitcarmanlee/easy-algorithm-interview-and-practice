本地已经有了现成的项目，需要将此项目push到远端gitlab的服务器上。具体操作步骤如下：  

## 1.在gitlab上创建好对应的project
首先，我们现在gitlab服务器上创建git@xxx.xxx.xxx:xxx/xxx.git项目，xxx.git是具体的项目名称。  

## 2.初始化本地项目
cd到本地项目目录，然后执行  

```
git init
```  
这样就初始化了本地git仓库  

## 3.关联远程仓库

```
git remote add origin git@xxx.xxx.xxx:xxx/xxx.git
```  

## 4.提交代码

```
git add .
git commit -m "init project"
git push -u origin master
```  

## 5.注意事项
使用`git add .`的时候，经常会将一些不必要的内容带进去。这个时候需要将不必要的内容撤销。由于此时还没有提交所以不存在HEAD版本，不能使用 git reset HEAD命令。  

此时，可以使用`git rm -r --cached .`撤销之前的add内容。  