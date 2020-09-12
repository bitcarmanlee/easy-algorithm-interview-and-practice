git的远程仓库是指托管在网络上的项目仓库。对于公司来说，绝大部分公司都会自己搭建自己的git仓库。对于RD来说，自然免不了要经常跟远程仓库 remote打交道。今天我们就来对远程仓库的使用做一个总结。  


第一步自然是将代码从仓库clone过来：  

```
lei.wang ~/gitcode $ git clone git@xxx:lei.wang/user_labels_merge.git
Cloning into 'user_labels_merge'...
remote: Counting objects: 30, done.
remote: Compressing objects: 100% (25/25), done.
remote: Total 30 (delta 7), reused 0 (delta 0)
Receiving objects: 100% (30/30), 5.70 KiB | 0 bytes/s, done.
Resolving deltas: 100% (7/7), done.
Checking connectivity... done.
```  

```
lei.wang ~/gitcode/user_labels_merge $ git status
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working directory clean
```  

因为刚clone过来代码，所以此时工作区是干净的。  
然后查看一下当前配置项里有哪些远程仓库，使用`git remote`命令即可，就会列出远程库的名字。在我们clone了刚才的项目之后，默认会看到一个origin的远程仓库。  

```
lei.wang ~/gitcode/user_labels_merge $ git remote
origin
```  

与大部分命令一样，`-v`选项表示列出详细信息：  

```
lei.wang ~/gitcode/user_labels_merge $ git remote -v
origin	git@xxx:lei.wang/user_labels_merge.git (fetch)
origin	git@xxx:lei.wang/user_labels_merge.git (push)
```  

如果要给此远程仓库添加一个新名字，方便后续使用，可以用以下方式：  

```
lei.wang ~/gitcode/user_labels_merge $ git remote add test_name git@xxx:lei.wang/user_labels_merge.git
lei.wang ~/gitcode/user_labels_merge $ git remote
origin
test_name

lei.wang ~/gitcode/user_labels_merge $ git fetch test_name
From xxx:lei.wang/user_labels_merge
 * [new branch]      master     -> test_name/master

lei.wang ~/gitcode/user_labels_merge $ git remote -v
origin	git@xxx:lei.wang/user_labels_merge.git (fetch)
origin	git@xxx:lei.wang/user_labels_merge.git (push)
test_name	git@xxx:lei.wang/user_labels_merge.git (fetch)
test_name	git@xxx:lei.wang/user_labels_merge.git (push)
```  

以上操作，首先使用`git remote add new_short_name url`命令 ，相当于给url对应的git仓库起了个别名。可以看到对应的远程库多了个名称test_name，然后我们用`git fetch test_name`从 远程库拉取代码。再用`git remote -v`查看 一下，可以看到test_name相关的信息。  

如果要想删除这个test_name，也很简单：  

```
lei.wang ~/gitcode/user_labels_merge $ git remote remove test_name
lei.wang ~/gitcode/user_labels_merge $

lei.wang ~/gitcode/user_labels_merge $ git remote
origin
lei.wang ~/gitcode/user_labels_merge $ git remote -v
origin	git@xxx:lei.wang/user_labels_merge.git (fetch)
origin	git@xxx:lei.wang/user_labels_merge.git (push)
```  

使用`git remote remove remote_name`即可。  

如果要查看远程库的相关信息，使用`git remote show remote_name`：  

```
lei.wang ~/gitcode/user_labels_merge $ git remote show origin
* remote origin
  Fetch URL: git@xxx:lei.wang/user_labels_merge.git
  Push  URL: git@xxx:lei.wang/user_labels_merge.git
  HEAD branch: master
  Remote branch:
    master tracked
  Local branch configured for 'git pull':
    master merges with remote master
  Local ref configured for 'git push':
    master pushes to master (up to date)
```  

要给远程库重命名：  

```
lei.wang ~/gitcode/user_labels_merge $ git remote rename origin origin_test
lei.wang ~/gitcode/user_labels_merge $ git remote
origin_test

[xxx@xxx merge_user_labels_mr]$ git remote -v
origin	git@xxx:lei.wang/user_labels_merge.git (fetch)
origin	git@xxx:lei.wang/user_labels_merge.git (push)
```  

原来此项目是在lei.wang下面，现在我在远程库中将其移动到了名为dmo的namespace下面。此时本地对应的远程库也要进行相应修改：  

```
[xxx@xxx merge_user_labels_mr]$ git fetch
Access denied.
fatal: The remote end hung up unexpectedly
```  

可以看到，将项目移动以后，这个时候如果想拉取代码的话会报错。其实这是废话，你原来指定的远程库里代码都没有了，能不报错嘛。    
这个时候就需要修改本地仓库指向的远程库：  
 
```
[xxx@xxx merge_user_labels_mr]$ git remote set-url origin git@xxx:dmo/user_labels_merge.git
[xxx@xxx merge_user_labels_mr]$

[xxx@xxx merge_user_labels_mr]$ git remote -v
origin	git@xxx:dmo/user_labels_merge.git (fetch)
origin	git@xxx:dmo/user_labels_merge.git (push)

[xxx@xxx merge_user_labels_mr]$ git fetch
[xxx@xxx merge_user_labels_mr]$
```  

使用命令`git remote set-url remote-name new_url` 即可。至此，搞定，手工。。。  