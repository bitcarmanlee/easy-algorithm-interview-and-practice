在python中，数组可以用list来表示。如果有两个数组，分别要求交集，并集与差集，怎么实现比较方便呢？  
当然最容易想到的是对两个数组做循环，即写两个for循环来实现。这种写法大部分同学应该都会，而且也没有太多的技术含量，本博主就不解释了。这里给大家使用更为装bility的一些方法。  

老规矩，talk is cheap,show me the code  

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年6月9日

@author: lei.wang
'''

def diff(listA,listB):
    #求交集的两种方式
    retA = [i for i in listA if i in listB]
    retB = list(set(listA).intersection(set(listB)))
    
    print "retA is: ",retA
    print "retB is: ",retB
    
    #求并集
    retC = list(set(listA).union(set(listB)))
    print "retC1 is: ",retC
    
    #求差集，在B中但不在A中
    retD = list(set(listB).difference(set(listA)))
    print "retD is: ",retD
    
    retE = [i for i in listB if i not in listA]
    print "retE is: ",retE
    
def main():
    listA = [1,2,3,4,5]
    listB = [3,4,5,6,7]
    diff(listA,listB)
    
if __name__ == '__main__':
    main()
```  

让code run起来  

```
retA is:  [3, 4, 5]
retB is:  [3, 4, 5]
retC1 is:  [1, 2, 3, 4, 5, 6, 7]
retD is:  [6, 7]
retE is:  [6, 7]
```  

结合代码来看，大体上是两种思路：  
1.使用列表解析式。列表解析式一般来说比循环更快，而且更pythonic显得更牛逼。  
2.将list转成set以后，使用set的各种方法去处理。  