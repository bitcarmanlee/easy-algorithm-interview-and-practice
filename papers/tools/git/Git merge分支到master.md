在本地开发好了一个分支，想要merge到master上，怎么操作呢？手把手教你操作。

## 1.本地拉一个分支出来

```
git checkout -b xxx
```

## 2.开发完以后提交到远程分支

```
git add .
git commit -m "commit xxx"
git push -u origin xxx
```

## 3.返回master

```
git checkout master
```

## 4.把本地的分支合并到master

```
git mrege xxx
```

## 5.把本地的master同步到远程

```
git push origin master
```

## 6.如果不需要本地或者远程的xxx分支了，你可以选择删除。
