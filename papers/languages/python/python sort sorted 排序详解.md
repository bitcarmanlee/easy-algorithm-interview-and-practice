python中，list类型内置了sort()方法用于排序。当然，python还有内置的全局sorted()方法，用于可迭代序列的排序。这两个方法大部分的用法是相同的，最大的不同在于，sort()方法不会生成一个新的list，而是在原有的list上进行修改；sorted()方法则是生成一个新的可迭代序列。  

## 1.最简单的排序
首先help一把list.sort()方法  

```
In [1]: help(list.sort)

Help on method_descriptor:

sort(...)
    L.sort(cmp=None, key=None, reverse=False) -- stable sort *IN PLACE*;
    cmp(x, y) -> -1, 0, 1
(END)
```  
注：在python 3.x系列中，cmp参数已经被废弃，由key参数指定即可。  

list.sort()方法就可以对list进行排序。不过需要注意的是，此时原来的list将被修改。  

```
In [2]: array=[5,3,1,7,9]

In [3]: array.sort()

In [4]: array
Out[4]: [1, 3, 5, 7, 9]
```  

## 2.复杂对象排序
使用的更广泛的情况是用复杂对象的某些值来实现复杂对象的排序。  
例如：  
```
In [5]: persons=[['lindan','A',20],['chenlong','A',18],['tiantian','B',18]]

In [6]: list.sort(persons,key=lambda person:person[2])

In [7]: persons
Out[7]: [['chenlong', 'A', 18], ['tiantian', 'B', 18], ['lindan', 'A', 20]]
```  

使用operator模块  
```
In [8]: persons=[['lindan','A',20],['chenlong','A',18],['tiantian','B',18]]

In [9]: from operator import itemgetter,attrgetter

In [10]: list.sort(persons,key=itemgetter(2))

In [11]: persons
Out[11]: [['chenlong', 'A', 18], ['tiantian', 'B', 18], ['lindan', 'A', 20]]
```  

## 3.对拥有命名属性的复杂对象排序
也可以对某个拥有命名属性的复杂对象进行排序(为了方便，使用sorted()方法，与list.sort()方法本质是一样的)  

```
class Person:
    def __init__(self,name,hierarchy,age):
        self.name = name
        self.hierarchy = hierarchy
        self.age = age
        
    def __repr__(self):
        return repr((self.name,self.hierarchy,self.age))
  
#按年龄排序  
def sort_age():
    Persons = [Person('kobe','A',20),Person('janes','A',18),Person('Tracy','B',18)]
    p_age = sorted(Persons,key = attrgetter('age'),reverse = True)
    print p_age
  
#先按年龄，再按名字排序  
def sort_age_hierarchy():
    Persons = [Person('kobe','A',20),Person('janes','A',18),Person('Tracy','B',18)]
    p_sorted = sorted(Persons,key = attrgetter('age','name'),reverse = True)
    print p_sorted
    
if __name__ == '__main__':
    sort_age()
    sort_age_hierarchy()
```  

结果如下：  
```
[('kobe', 'A', 20), ('janes', 'A', 18), ('Tracy', 'B', 18)]
[('kobe', 'A', 20), ('janes', 'A', 18), ('Tracy', 'B', 18)]
```  