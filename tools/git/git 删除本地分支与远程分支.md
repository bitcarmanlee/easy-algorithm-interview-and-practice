git上面的分支开发完成以后，完成了他的历史使命，就可以删除了。  
## 1.删除本地分支
查看本地分支  

```
git branch
  add_jvm_config_and_exception_log
  hdfs_config_in_zk
* master
  subBucket
```  
删除已经merge的本地分支    

```
git branch -d add_jvm_config_and_exception_log 
已删除分支 add_jvm_config_and_exception_log（曾为 4b0bd09）。
```  

如果是要删除不管有没有merge的本地分支  

```
git branch -D xxx
```  

## 2.删除远程分支

查看远程分支  

```
git branch -r
  origin/add_jvm_config_and_exception_log
  origin/hdfs_config_in_zk
  origin/master
  origin/subBucket
```  

删除远程分支  

```
git push --delete origin add_jvm_config_and_exception_log
To git@xxx
 - [deleted]         add_jvm_config_and_exception_log
```  

也可以用如下命令  

```
git push origin :xxx
```  

xxx表示分支名称  

