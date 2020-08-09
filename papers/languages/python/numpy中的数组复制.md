## 1.np.repeat VS np.tile
repeat与tile函数都是复制相关的操作。    
tile操作，是复制的多维数组本身  
  
```
"""
Construct an array by repeating A the number of times given by reps.
“”“  
```  

repeat操作复制的则是多维数组的每个元素  

```
"""
Repeat elements of an array.
"""
```  

## 2.np.repeat  
```
>>> np.repeat(3, 4)
    array([3, 3, 3, 3])
```  

上面的操作得到一个长度为4的数组  

```
>>> x = np.array([[1,2],[3,4]])
    >>> np.repeat(x, 2)
    array([1, 1, 2, 2, 3, 3, 4, 4])
```  

上面先将高维的数组flatten至一维，然后进行复制。    

```
>>> np.repeat(x, 3, axis=1)
array([[1, 1, 1, 2, 2, 2],
       [3, 3, 3, 4, 4, 4]])

```  

axis=1是按行进行操作。  

```
>>> np.repeat(x, [1, 2], axis=0)
    array([[1, 2],
           [3, 4],
           [3, 4]])
```  

axis=0相当于按照行进行复制，并且前面的list [1,2]指定了按照不同的行复制不同的次数。  

## 3.np.tile
注意tile不需要指定axis  
```
>>> a = np.array([0, 1, 2])
    >>> np.tile(a, 2)
    array([0, 1, 2, 0, 1, 2])
```  

```
>>> np.tile(a, (2, 2))
    array([[0, 1, 2, 0, 1, 2],
           [0, 1, 2, 0, 1, 2]])
    >>> np.tile(a, (2, 1, 2))
    array([[[0, 1, 2, 0, 1, 2]],
           [[0, 1, 2, 0, 1, 2]]])

```  

```
>>> b = np.array([[1, 2], [3, 4]])
    >>> np.tile(b, 2)
    array([[1, 2, 1, 2],
           [3, 4, 3, 4]])
    >>> np.tile(b, (2, 1))
    array([[1, 2],
           [3, 4],
           [1, 2],
           [3, 4]])
```  

```
>>> c = np.array([1,2,3,4])
>>> np.tile(c,(4,1))
array([[1, 2, 3, 4],
       [1, 2, 3, 4],
       [1, 2, 3, 4],
       [1, 2, 3, 4]])
```  
