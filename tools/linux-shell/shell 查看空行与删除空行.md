文件中经常会出现一些空行，很多场合下我们需要对这些空行进行处理，下面稍微总结一下处理空行的一些办法。  

## 1.查看空行行号
使用linux文本三剑客来处理。  
### 1.1 grep

```
grep -n '^\s*$' xxx
```  
其中，-n表示line-number，会输出行号  

### 1.2 awk

```
awk '/^\s*$/{print NR}' xxx
```  

### 1.3 sed

```
sed -n '/^\s*$/=' xxx
```  

其中，-n表示    

```
-n, --quiet, --silent

              suppress automatic printing of pattern space
```  

## 2.去除空行  
更多时候，我们需要做的是去除空行，下面看看去除空行的方法  

### 2.1 grep

```
grep -v '^\s*$' xxx >newfile
```  

其中，-v表示与匹配结果反转。  

```
-v, --invert-match
             Selected lines are those not matching any of the specified patterns.
```  

### 2.2  sed

```
sed '/^\s*$/d' xxx >newfile
```  

当然，我们还可以使用-i参数对文件原地进行修改。  

```
-i[SUFFIX], --in-place[=SUFFIX]

              edit files in place (makes backup if SUFFIX supplied)
```  

### 2.3 awk

```
awk '$0!~/^\s*$/{print $0} ' xxx >newfile
```
