项开发过程中，有时会需要将代码回滚至上一次提交或回滚到某一次提交。项目新版本上经后，如果不能正常运行，或遇到其它极端问题时，我们需要将代码回滚至上一个版本。通过git revert命令，可以实现代码的提交回滚。  

## 1.git revert命令介绍
git revert作用是回滚已经存在提交。  

git revert回滚本质是用某次commit时的代码再做一次commit提交，所以git revert不会对已经提交的代码产生影响。 下面是三种常用的回滚方式：  

```
git revert commit-id    // 回滚至某个commit版本
git revert HEAD              // 回滚至上一次的 commit
git revert HEAD^             // 回滚至上上次的commit
```

## 2.使用git revert回滚代码至上一个版本
使用git revert回滚代码，关键点在于到找到要回滚版本commit时的提交标识。  

如果使用Git标签进行版本管理，可以使用git show 标签名命令来查找指定版本最后一次commit提交信息。例如，在发布v1.0版时，添加了一个名为v1.0的标签，现在想回滚至v1.0，可以使用以下命令查看提交标识：  

```
git show tag v1.0
```  

如果没有使用git 标签进行版本管理，或者要回滚的目标代码不是某个发布版本，那么就需要通过git log查看提交日志，并通提交时的描述信息确认提交标识。  

```
git log
```  

通上面介绍的方法，现在找了v1.0版本的提交标识为afc4408db31cd537cef669f0f8e40acf079ea8a0，回滚至v1.0代码如下：  

```
git revert afc4408db31cd537cef669f0f8e40acf079ea8a0
```  