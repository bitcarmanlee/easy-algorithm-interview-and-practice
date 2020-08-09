## 1. 嵌套list
python中嵌套的list还算比较常见的一种结构。比如我们经常用嵌套两层的list来模拟矩阵:  

```
>>> matrix = [[1,2,3],[4,5,6],[7,8,9]]
>>> matrix
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```  

很多时候我们想将这一个嵌套两层的list变成一个list，该怎么办呢？对于上面的例子，我们很容易找到如下的方式就可以满足需求：  

```
def flatmatrix(matrix):
    result = []
    for i in range(len(matrix)):
        result.extend(matrix[i])
    print result


matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flatmatrix(matrix)
```  

如果嵌套的list不是两层结构，而是任意的形式，上面的方式就不适用了。  

## 2.递归打平嵌套list
比较容易想到的是递归的方式处理任意形式的嵌套list。我们取遍历原始的list，如果里面的元素是list则递归，如果不是加入结果中，直到原始list的所有元素遍历结束。具体代码如下:  

```
def flat1(inputlist, result = None):
    if result is None:
        result = []
    for item in inputlist:
        if isinstance(item, list):
            flat1(item, result)
        else:
            result.append(item)
    return result
    
inputlist = ['it', 'is', ['a', ['test', 'of', ['circle', 'lists'], ','], 'please', 'like', ['it', 'and'], 'hello'], 'world']
print flat1(inputlist)
```  

## 3.通过循环打平嵌套list
一般来说，递归的优势是简洁明了，容易理解。缺点则是需要递归栈，效率比较低。我们尝试用非递归的方式来实现。  

```
def flat2(inputlist):
    result = []
    while inputlist:
        head = inputlist.pop(0)
        if isinstance(head, list):
            inputlist = head + inputlist
        else:
            result.append(head)
    return result


inputlist = ['it', 'is', ['a', ['test', 'of', ['circle', 'lists'], ','], 'please', 'like', ['it', 'and'], 'hello'], 'world']
print flat2(inputlist)
```  

循环的过程中，每次将输入list的首位元素取出来然后放到原来的位置，这样就起到了解开一层嵌套的作用，直到最后将所有的嵌套解开为止！  