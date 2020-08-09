## 1.遍历嵌套list
将嵌套的list遍历并输出是很常见的需求。以下通过两种方法达到目的    

```
def nested_list(list_raw,result):
    for item in list_raw:
        if isinstance(item, list):
            nested_list(item,result)
        else:
            result.append(item)
            
    return  result   
            
def flatten_list(nested):
    if isinstance(nested, list):
        for sublist in nested:
            for item in flatten_list(sublist):
                yield item
    else:
        yield nested
    
def main():   
    list_raw = ["a",["b","c",["d"]]]
    result = []
    print "nested_list is:  ",nested_list(list_raw,result)
    print "flatten_list is: ",list(flatten_list(list_raw))
    
main()
```  

让代码run起来，输出为：    

```
nested_list is:   ['a', 'b', 'c', 'd']
flatten_list is:  ['a', 'b', 'c', 'd']

```  

nested_list方法采用递归的方式，如果item是list类型，继续递归调用自身。如果不是，将item加入结果列表中即可。  
flatten_list方法则是采用生成器的方式，本质上也是递归的思路。  

## 2.两层嵌套list去重
list里面套了一层list，需要去重，并在生成一个去重的list。请看代码：  

```
def dup_remove_set(list_raw):
    result = set()
    for sublist in list_raw:
        item = set(sublist)
        result = result.union(item)
    return list(result)

def main():  
    list_dup = [[1,2,3],[1,2,4,5],[5,6,7]]
    print dup_remove_set(list_dup)
```  

让代码run起来：  

```
[1, 2, 3, 4, 5, 6, 7]
```  

基本思路：将每一个子list转为set，然后求并集，即可。  

## 3.多重嵌套去重

```
def dup_remove(list_raw,result):
    for item in list_raw:
        if isinstance(item, list):
            dup_remove(item,result)
        else:
            result.add(item)
            
    return  list(result)

def main():   
    list_raw = ["a",["b","c",["d","a","b"]]]
    result = set()
    print "dup_remove is:  ",dup_remove(list_raw,result)
```  

让代码run起来：  

```
dup_remove is:   ['a', 'c', 'b', 'd']
```  

基本思路与之前遍历嵌套list的思路差不多，唯一的区别就是之前result是一个list，而要去重的话用result是一个set，保证最后的结果为去重的结果。  