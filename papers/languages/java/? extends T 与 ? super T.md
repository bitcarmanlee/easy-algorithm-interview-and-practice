java的一个设计理念是，与泛型相关的异常最好是在编译期间就被发现，因此设计了extends与super这两种方式。  
具体来说，List<? extends T>表示该集合中存在的都是类型T的子类，包括T自己。  
而List<? super T>表示该集合中存的都是类型T的父类，包括T自己。  

List<? extends T>如果去添加元素的时候，因为list中存放的其实是T的一种子类，如果我们去添加元素，其实不知道到底应该添加T的哪个子类，这个时候桥接方法在进行强转的时候会出错。但是如果是从集合中将元素取出来，我们可以知道取出来的元素肯定是T类型。所以? extends T这种方式可以取元素而不能添加，这个叫get原则。  

List<? super T>因为存的都是类型T的父类，所以如果去添加T类或者T类子类的元素，肯定是可以的。但是如果将元素取出来，则不知道到底是什么类型，所以? super T可以添加元素但是没法取出来，这个叫put原则。  

```
    public static void test() {
        List<? extends Number> l1 = new ArrayList<>();
        // l1.add(1); 会报错

        List<? super Number> l2 = new ArrayList<>();
        // Number n = l2.get(1); 会报错
        l2.add(1);
        l2.add(2);
        l2.add(0.11);
        for(Object n: l2) {
            System.out.println(n.toString());
        }
    }
```  
