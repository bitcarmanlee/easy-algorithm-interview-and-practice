## 1.计算均值

```
import numpy as np

a = [5, 6, 16, 9]
print(np.mean(a))
```  

最后结果  

```
9.0
```  

np.mean方法即可求均值  

## 2.计算方差

```
var = np.var(a)
print(var)
```  

输出结果  

```
18.5
```  

如果我们模拟一下计算方差的过程  
```
var2 = [math.pow(x-np.mean(a), 2) for x in a]
print(np.mean(var2))
```  

输出结果  

```
18.5
```  

np.var计算的是整体方差，如果想要计算样本方差，即除数的分母为N-1，可以指定ddof参数  

```
sample_var = np.var(a, ddof=1)
print(sample_var)
```  

输出结果为  

```
24.666666666666668
```  

## 3.计算标准差

```
std = np.std(a)
std2 = np.std(a, ddof=1)
print(std)
print(std2)
```  

std函数计算的是整体标准差。跟var函数一样，如果指定ddof=1，计算的是样本标准差。  