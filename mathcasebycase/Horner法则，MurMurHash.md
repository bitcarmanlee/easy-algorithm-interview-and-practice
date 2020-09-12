## 1.Horner法则  
假设有一个n次多项式需要计算。  
$$f(x) = a_nx^n + a_{n-1}x^{n-1} + \cdots + a_1x + a_0$$  
如果直接进行计算，需要$\frac{n(n+1)}{2}$次乘法与$n$次加法。而乘法的代价是比较大的，所以效率会比较低。  

将上面的多项式改写一下  

$$
\begin{aligned}
f(x) & = a_nx^n + a_{n-1}x^{n-1} + \cdots + a_1x + a_0  \\\\
& = (a_nx^{n-1} + a_{n-1}x^{n-2} + \cdots + a_2x + a_1)x + a_0 \\\\
& =  (((a_nx + a_{n-1})x + a_{n-2})x + \cdots + a_1)x + a_0\\\\
\end{aligned}
$$  

求上面的值的时候，很明显可以从括号里由内到位一次计算，最后的计算复杂度为n次乘法与n次加法。  

## 2.java String中的HashCode
看看String类里hashCode的源码。  

```
    public int hashCode() {
        int h = hash;
        if (h == 0 && value.length > 0) {
            char val[] = value;

            for (int i = 0; i < value.length; i++) {
                h = 31 * h + val[i];
            }
            hash = h;
        }
        return h;
    }
```  

根据源码不难看出，其计算方式就是  
$$s[0]*31^{(n-1)} + s[1]*31^{(n-2)} + ... + s[n-2] * 31 + s[n-1]$$


## 3.MurMurHash
上面的hashCode方法有个不好的地方就是变化不够激烈。比如我们看一下的例子  

```
    @Test
    public void test2() {
        String s1 = "abcdefg";
        String s2 = "abcdeff";
        System.out.println(s1.hashCode());
        System.out.println(s2.hashCode());
    }
```  

上面代码运行的结果为  

```
-1206291356
-1206291357
```  

两个相似的字符串，得到的hash值也很相似。  

MurmurHash 是一种非加密型哈希函数，适用于一般的哈希检索操作。由Austin Appleby 在2008年发明，并出现了多个变种，都已经发布到了公有领域。与其它流行的哈希函数相比，对于规律性较强的key，MurmurHash的随机分布特征表现更良好，现在在libstdc++，hadoop和nginx等很多著名开源项目中使用。    


