## 1.json是什么
JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式。它基于JavaScript Programming Language, Standard ECMA-262 3rd Edition - December 1999的一个子集。json最大的优势就是独立于编程语言， 易于人阅读和编写，同时也易于机器解析和生成。所以，如果我们需要在不同的编程语言之间传递对象，或者需要在网络世界中传输数据，我们都可以将数据序列化为json格式。当将其序列化为json格式以后，可以方便地被所有编程语言读取与解析，也可以方便地被存储在磁盘中或者用于网络传输。正因为有这些优点，json在实际中使用非常广泛。  

JSON构建于两种结构：  
1.“名称/值”对的集合（A collection of name/value pairs）。不同的语言中，它被理解为对象（object），纪录（record），结构（struct），字典（dictionary），哈希表（hash table），有键列表（keyed list），或者关联数组 （associative array）。  
2.值的有序列表（An ordered list of values）。在大部分语言中，它被理解为数组（array）。  

## 2.python数据类型与json数据类型的映射关系
Python类型 JSON类型  
dict $\hspace{1.3cm}$ {}  
list  $\hspace{1.5cm}$ []  
str(unicode) $\hspace{0.5cm}$ string  
int(float,long) $\hspace{0.3cm}$number  
True(False) $\hspace{0.7cm}$ true(false)  
None $\hspace{1.7cm}$ null  

## 3.python中json模块的简单用法
python中内置的json模块就可以完成从python对象到json格式数据的转换。  
先来看看怎么把一个python对象变为一个json串：  

```
>>> import json
>>> dic = dict(name='James',age=18)
>>> dic_to_str = json.dumps(dic)
>>> dic_to_str
'{"age": 18, "name": "James"}'
>>> type(dic_to_str)
<type 'str'>
```  

通过dumps方法，就把一个dict变为了一个json串，返回的是一个str对象。dumps方法相当于一个encoding过程，是对简单数据类型的编码。也可以理解是对python对象的一个序列化的过程。  

接下来看看如何把一个json串变为一个python对象：  

```
>>> str_to_dic = json.loads(dic_to_str)
>>> str_to_dic
{u'age': 18, u'name': u'James'}
>>> type(str_to_dic)
<type 'dict'>
```  

同理通过loads方法，将一个json串，变为了一个dict对象，返回的是一个dict。loads方法相当于是一个decoding过程，是对字符串的一个解码。当然也可以理解为是对python对象的反序列化！  

## 4.将自己的类转成json串
前面我们看了怎样将python中的内置dict对象转化为json串的过程。在很多时候，我们希望将自己定义的类也转化为json串。比如我们自己定义了person类，并且希望将其序列化为json串：  

```
#!/usr/bin/env python
#coding:utf-8

import json

class Person(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

person = Person("James",18)
print (json.dumps(person))
```  

将上面的代码run起来以后，会有以下错误：  

```
Traceback (most recent call last):
  File "./person.py", line 13, in <module>
    print (json.dumps(person))
  File "/Users/lei.wang/anaconda/lib/python2.7/json/__init__.py", line 244, in dumps
    return _default_encoder.encode(obj)
  File "/Users/lei.wang/anaconda/lib/python2.7/json/encoder.py", line 207, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/Users/lei.wang/anaconda/lib/python2.7/json/encoder.py", line 270, in iterencode
    return _iterencode(o, 0)
  File "/Users/lei.wang/anaconda/lib/python2.7/json/encoder.py", line 184, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: <__main__.Person object at 0x101a00090> is not JSON serializable
```  

很明显可以看出，是我们无法将person对象序列化！  
我们再仔细观察一下dumps()方法：  

```
json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)

Serialize obj to a JSON formatted str using this conversion table. If ensure_ascii is false, the result may contain non-ASCII characters and the return value may be a unicode instance.
```  

参数default选项就是将一个对象变为一个可序列化的Json对象。前面的Person类就是因为没有指定default选项，所以无法序列化。现在我们为Person类写一个专门的序列化方法：  

```
!/usr/bin/env python
#coding:utf-8

import json

class Person(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

def person_to_dict(person):
    return {
        'name': person.name,
        'age':  person.age
            }

person = Person("James",18)
print json.dumps(person,default = person_to_dict)
```  

将代码运行起来：  

```
{"age": 18, "name": "James"}
```  

上面这么做的目的，就是通过person_to_dict方法，将person对象转化为dict对象，然后通过将default选项设置为person_to_dict，就可以使用dumps方法将person对象序列化为json对象了！  

当然，如果我们想偷点懒，也是可以的。可以不写person_to_dict方法，直接调用person类的__dict__方法：  

```
!/usr/bin/env python
#coding:utf-8

import json

class Person(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

def person_to_dict(person):
    return {
        'name': person.name,
        'age':  person.age
            }

person = Person("James",18)
print json.dumps(person,default = lambda obj:obj.__dict__)
print json.dumps(person,default = person_to_dict)
```  

让代码run起来：  

```
{"age": 18, "name": "James"}
{"age": 18, "name": "James"}
```  

由此可见，print两行代码的效果是一致的！  

同样的道理，既然能将自己定义的类转化为json串，同理也能将json串变为类。我们先看看loads方法：  

```
json.loads(s[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])
Deserialize s (a str or unicode instance containing a JSON document) to a Python object using this conversion table.

object_hook is an optional function that will be called with the result of any object literal decoded (a dict). The return value of object_hook will be used instead of the dict. This feature can be used to implement custom decoders (e.g. JSON-RPC class hinting).
```  

仿照上面的思路：  

```
#!/usr/bin/env python
#coding:utf-8

import json

class Person(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

def dic_to_person(dic):
    return Person(dic['name'],dic['age'])

json_person = '{"name":"James","age":18}'
print json.loads(json_person,object_hook = dic_to_person)
```  

让代码run起来：  

```
<__main__.Person object at 0x1022071d0>
```  

由此可见，我们通过loads方法，达到了将json字符串反序列化为Person对象的目的！  