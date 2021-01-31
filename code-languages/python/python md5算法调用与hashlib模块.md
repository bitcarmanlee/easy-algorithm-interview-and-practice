## 1.python中的md5
将一个字符串md5匿名化是数据处理中的一种常见手段，python3.X中也内置实现了md5算法，下面我们看下md5的用法。  

```
import hashlib

def test():
    s = "123"
    m = hashlib.md5()
    for i in range(5):
        m.update(s.encode("utf8"))
        result = m.hexdigest()
        print(result)
```  

上面代码的输出为：  

```
202cb962ac59075b964b07152d234b70
4297f44b13955235245b2497399d7a93
f5bb0c8de146c67b44babbf4e6584cc0
101193d7181cc88340ae5b2b17bba8a1
e277dd1e05688a22e377e25a3dae5de1
```  

我们想对123这个字符串做5次md5，理论上5次md5的结果应该一样，但是最后输出的结果却不相同。  

原因就在于update方法：  
当同一个hashlib对象调用update方法时，假设第一次输入字符串a,第二次输入字符串b，那么第二次md5的结果其实是a+b的md5结果。  

看个简单的例子来证实一下我们的结论：  

```
def test():
    s = "123123"
    m = hashlib.md5()
    m.update(s.encode("utf8"))
    result = m.hexdigest()
    print(result)
```  

上面的输出结果为  

```
4297f44b13955235245b2497399d7a93
```  

与之前for循环遍历的第二次输出结果一直，即"123123"进行md5以后得到的结果。  

## 2.hashlib模块
hashlib模块中包含常用的hash算法，源码中列出来的有如下：  

```
# This tuple and __get_builtin_constructor() must be modified if a new
# always available algorithm is added.
__always_supported = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                      'blake2b', 'blake2s',
                      'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
                      'shake_128', 'shake_256')
```  

下面我们选择几个常见的做一下测试  

```
from hashlib import md5
from hashlib import sha256
from hashlib import sha512

hash_functions = [md5, sha256, sha512]

def get_hash_code(s):
    result = []
    for function in hash_functions:
        hash_obj = function(s)
        hash_hex = hash_obj.hexdigest()
        result.append((hash_obj.name, hash_hex, len(hash_hex)))
    return result


if __name__ == '__main__':
    s = "123"
    result = get_hash_code(s.encode("utf-8"))
    for each in result:
        print(each)
```  

最终输出结果为：  

```
('md5', '202cb962ac59075b964b07152d234b70', 32)
('sha256', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 64)
('sha512', '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2', 128)
```  
