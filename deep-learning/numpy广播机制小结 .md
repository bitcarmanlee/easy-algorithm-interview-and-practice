## 1.Broadcast(广播)机制
numpy中的广播很常见，其用法是针对不同的shape的ndarray进行对应的数值计算的时候，将较小的ndarray广播变成更大的ndarray进行对应的shape匹配，从而使两个看起来shape不匹配的数组能进行相应的数值运算。

## 2.广播的规则
1.All input arrays with ndim smaller than the input array of largest ndim, have 1’s prepended to their shapes.    

2.The size in each dimension of the output shape is the maximum of all the input sizes in that dimension.  

3.An input can be used in the calculation if its size in a particular dimension either matches the output size in that dimension, or has value exactly 1.  

4.If an input has a dimension size of 1 in its shape, the first data entry in that dimension will be used for all calculations along that dimension. In other words, the stepping machinery of the ufunc will simply not step along that dimension (the stride will be 0 for that dimension).  

翻译过来就是  
1.让所有输入数组都向其中shape最长的数组看齐，shape中不足的部分都通过在前面加1补齐    
2.输出数组的shape是输入数组shape的各个轴上的最大值  
3.如果输入数组的某个轴和输出数组的对应轴的长度相同或者其长度为1时，这个数组能够用来计算，否则出错  
4.当输入数组的某个轴的长度为1时，沿着此轴运算时都用此轴上的第一组值  

上面的解释其实还是比较抽象，下面我们通过一些例子来理解。  

## 3.实例分析  
首先我们看最简单的一种广播方式，向量对标量的运算。  

```
import numpy as np


def t1():
    array = np.arange(5)
    print("array is: ", array)
    array = array * 4
    print("after broadcast, array is: ", array)
```  

运行的结果为  

```
array is:  [0 1 2 3 4]
after broadcast, array is:  [ 0  4  8 12 16]
```  

这个没啥好讲的，比较典型的element-wise运算方式，本质上是array每个位置都乘4，运算过程可以理解为将4这个标量广播成了5*1的维度。  

```
def t2():
    array = np.arange(12).reshape(4, 3)
    print("array is: ", array)

    print(array.mean(0))
    print(array.mean(0).shape)
    print(array.mean(1))
    print(array.mean(1).shape)
    array = array - array.mean(0)
    print("after broadcast, array is: ", array)
    array = array - array.mean(1)
    print("after broadcast, array is: ", array)
```  

输出的结果为  

```
array is:  [[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
[4.5 5.5 6.5]
(3,)
[ 1.  4.  7. 10.]
(4,)
after broadcast, array is:  [[-4.5 -4.5 -4.5]
 [-1.5 -1.5 -1.5]
 [ 1.5  1.5  1.5]
 [ 4.5  4.5  4.5]]
Traceback (most recent call last):
  File "/Users/wanglei/wanglei/code/python/tfpractice/basic/Broadcast.py", line 81, in <module>
    t2()
  File "/Users/wanglei/wanglei/code/python/tfpractice/basic/Broadcast.py", line 29, in t2
    array = array - array.mean(1)
ValueError: operands could not be broadcast together with shapes (4,3) (4,) 
```  

上面的代码中，mean(0)的维度为(3,)，与(4, 3)维度的array运算时，mean(0)最后一维为3，与(4,3)的最后一维相等，所以能被顺利广播。但是mean(1)的维度为(4, )，与(4,3)的最后一维不相等，所以无法被广播。  

```
def t3():
    array = np.arange(12).reshape(4, 3)
    print("array is: ", array)
    print(array.mean(0))
    print(array.mean(0).shape)
    print(array.mean(1))
    print(array.mean(1).shape)
    array = array - array.mean(0).reshape(1, 3)
    print("after broadcast, array is: ", array)
```  

运行结果如下  

```
array is:  [[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
[4.5 5.5 6.5]
(3,)
[ 1.  4.  7. 10.]
(4,)
after broadcast, array is:  [[-4.5 -4.5 -4.5]
 [-1.5 -1.5 -1.5]
 [ 1.5  1.5  1.5]
 [ 4.5  4.5  4.5]]
```  

```
def t4():
    array = np.arange(12).reshape(4, 3)
    print("array is: ", array)
    print(array.mean(1).reshape(4, 1))
    array = array - array.mean(1).reshape(4, 1)
    print("after broadcast, array is: ", array)
```  

运行结果如下  

```
array is:  [[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
[[ 1.]
 [ 4.]
 [ 7.]
 [10.]]
after broadcast, array is:  [[-1.  0.  1.]
 [-1.  0.  1.]
 [-1.  0.  1.]
 [-1.  0.  1.]]
```  

当mean(1)被reshape成(4,1)以后，与array的维度(4, 3)相比，第一维相同，第二维是1，所以能顺利广播。  


```
def t5():
    array = np.arange(24).reshape(2, 3, 4)
    print("in the beginning, array is: ", array)
    arrayb = np.arange(12).reshape(3, 4)
    print("arrayb is: ", arrayb)
    array = array - arrayb
    print("after broadcast, array is: ", array)
```  

运行结果  

```
in the beginning, array is:  [[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
arrayb is:  [[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
after broadcast, array is:  [[[ 0  0  0  0]
  [ 0  0  0  0]
  [ 0  0  0  0]]

 [[12 12 12 12]
  [12 12 12 12]
  [12 12 12 12]]]
```  


上述array的维度是(2, 3, 4)，arrayb的维度是(3,4)，因此广播的时候，是相当于是在shape[0]的维度上进行复制。  

```
def t6():
    array = np.arange(24).reshape(2, 3, 4)
    print("in the beginning, array is: ", array)
    arrayb = np.arange(8).reshape(2, 1, 4)
    print("arrayb is: ", arrayb)
    array = array - arrayb
    print("after broadcast, array is: ", array)


def t7():
    array = np.arange(24).reshape(2, 3, 4)
    print("in the beginning, array is: ", array)
    arrayb = np.arange(6).reshape(2, 3, 1)
    print("arrayb is: ", arrayb)
    array = array - arrayb
    print("after broadcast, array is: ", array)
```  

运行结果为  

```
in the beginning, array is:  [[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
arrayb is:  [[[0 1 2 3]]

 [[4 5 6 7]]]
after broadcast, array is:  [[[ 0  0  0  0]
  [ 4  4  4  4]
  [ 8  8  8  8]]

 [[ 8  8  8  8]
  [12 12 12 12]
  [16 16 16 16]]]
in the beginning, array is:  [[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
arrayb is:  [[[0]
  [1]
  [2]]

 [[3]
  [4]
  [5]]]
after broadcast, array is:  [[[ 0  1  2  3]
  [ 3  4  5  6]
  [ 6  7  8  9]]

 [[ 9 10 11 12]
  [12 13 14 15]
  [15 16 17 18]]]
```  

上面的两个方法，则分别是在shape[1]与shape[2]的维度上进行广播  


## 4.总结
结合上面的实例，我们总结一下广播的基本原则：  
1.两个数组从末尾开始进行维度的比较。  
2.如果维度相等或者其中有一个值为1，则认为可以广播。  
3.维度如果缺失，可以忽略。  
4.广播是在缺失的维度或者为1的维度上进行的。  

