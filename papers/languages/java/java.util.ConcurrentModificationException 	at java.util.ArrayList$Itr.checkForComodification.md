## 1.ConcurrentModificationException
有如下代码处理ArrayList  

```
    @Test
    public void test1() {
        List<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.add(3);
        list.add(4);
        for(int num: list) {
            if (num == 2) {
                list.remove(num);
            }
        }
        System.out.println(StringUtils.join(list, ","));
    }
```  

代码运行起来会报如下错误：  

```
java.util.ConcurrentModificationException
	at java.util.ArrayList$Itr.checkForComodification(ArrayList.java:909)
	at java.util.ArrayList$Itr.next(ArrayList.java:859)
	...
```  

## 2.分析
https://juejin.im/post/5a992a0d6fb9a028e46e17ef  
上面的文章分析得挺详细的，就不复制粘贴了。简单总结一下就是：  
ArrayList抛异常的位置源码如下  

```
        final void checkForComodification() {
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
        }
```  

modCount是ArrayList本身的属性，expectedModCount是ArrayList内部类Iterator的属性。  

理论上他们是同步的，但是我们在某些操作的过程中导致会导致他们不一致，比如说在这个例子中，我们调用的是ArrayList.remove()方法，修改了size和modCount属性，但是Itr中的这cursor、expectedModCount却没有发生变化，当增强for循环再次执行的时候，调用的却是Itr中的方法，最终发现了数据不一致。这就是本例ConcurrentModificationException产生的根本原因。    

## 3.解决方案
最保险的方案就是在遍历的时候不remove，最后再remove...  

```
    @Test
    public void test2() {
        List<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.add(3);
        list.add(4);
        List<Integer> tmp = new ArrayList<>();
        for(int num: list) {
            if (num == 2) {
                tmp.add(num);
            }
        }
        list.removeAll(tmp);
        System.out.println(StringUtils.join(list, ","));
    }
```  
