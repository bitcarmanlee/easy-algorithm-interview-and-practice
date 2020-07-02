## 1.从N个数中等概率抽取M个数
从N个样本中等概率抽取M个样本(M<N)是常见的需求。现在我们以一个数组来模拟样本，看看怎么实现这个算法。  
最容易想到的方法，肯定就是直接等概率抽取。具体做法如下：每次都随机在\[0, N-1](假设第一个样本d的标号为0)之间抽取一个数，并且与之前的数相比较。如果与前面生成的随机数相同，则继续随机生成，直到生成一个与之前所有生成数不同的数。如果不相同，则将该随机数添加到结果集中，并继续随机抽取，直至结果集中的数为M个。  

```
    public static Set<Integer> sampletest() {
        Set<Integer> set = new HashSet<>();
        int first = RandomUtils.nextInt(0, 24);
        int second = RandomUtils.nextInt(0, 24);
        int third = RandomUtils.nextInt(0, 24);
        set.add(first);
        while(set.contains(second)) {
            second = RandomUtils.nextInt(0, 24);
        }
        set.add(second);
        while(set.contains(third)) {
            third = RandomUtils.nextInt(0, 24);
        }
        set.add(third);
        return set;
    }
    public static void samplemassive() {
        Map<Integer, Integer> map = new HashMap();
        for(int i=0; i<10000; i++) {
            Set<Integer> res = sampletest();
            for(int each: res) {
                map.put(each, map.getOrDefault(each, 0) + 1);
            }
        }
        for(Map.Entry<Integer, Integer> entry: map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
```  
上面的代码是在24个数中随机抽取3个数，然后将该抽样重复一万次，输出最后的结果。  
将samplemassive方法run起来以后，输出结果如下：  

```
0: 1218
1: 1239
2: 1195
3: 1200
4: 1213
5: 1282
6: 1297
7: 1241
8: 1200
9: 1270
10: 1272
11: 1277
12: 1250
13: 1270
14: 1233
15: 1212
16: 1298
17: 1228
18: 1238
19: 1212
20: 1209
21: 1308
22: 1308
23: 1256
```  

一共需要抽样出来10000*3=30000个数，每个数出现的次数平均为30000/24=1250次。上面的结果大致满足等概率均匀分布。  

上面算法的问题在于，当m比较大的时候，每次调用random方法生成的数与之前重合的概率也会越来越大，则while循环里random的调用次数会越来越多，这样时间复杂度就会升高。  
那么具体的时间复杂度是多少呢？可以定量分析一下。  
假设之前已经生成了x个数，接下来生成第x-1个数。  
第一次调用random就成功生成第x-1个数的概率为$1 - \frac{x}{n}$  
第二次调用random就成功生成第x-1个数的概率为$(1 - \frac{x}{n})\frac{x}{n}$  
第k次调用random就成功生成第x-1个数的概率为$(1 - \frac{x}{n}){(\frac{x}{n})}^{k-1}$  

那么生成第x+1个数需要调用random方法的次数为:  
$$E(x+1) = (1 - \frac{x}{n}) * 1 + (1 - \frac{x}{n})\frac{x}{n} * 2 + \cdots + (1 - \frac{x}{n}){(\frac{x}{n})}^{k-1} * k + \cdots = \frac{n}{n-x}$$  
上述等差-等比数列求和的方法，见参考文献1，只需要中学数学知识即可理解。  

则调用random方法的总次数期望为:  
$$E(random) = \frac{n}{n} + \frac{n}{n-1} + \cdots + \frac{n}{n-m-1} \approx O(n(lg(n) - lg(n-m)))$$  
当m接近n时，此时时间复杂度接近$O(nlogn)$，算法的复杂度比较高。  

上面的sample算法比较笨，实现一个通用的从N个数抽取M个的算法。  

```
    public static Set<Integer> sampletest(int n, int m) {
        Set<Integer> set = new HashSet<>();
        int first = RandomUtils.nextInt(0, n);
        set.add(first);
        while(set.size() < m) {
            int tmp = RandomUtils.nextInt(0, n);
            while(set.contains(tmp)) {
                tmp = RandomUtils.nextInt(0, n);
            }
            set.add(tmp);
        }
        return set;
    }
```  
其中，n是原始样本长度，m为待抽取样本个数。  

## 2.时间复杂度为O(n)的从N个数中抽取M个的算法
上面的算法，时间复杂度为$O(nlgn)$。那么有没有时间复杂度更低的算法呢？  
答案是有的，用蓄水池算法就可以实现。  
关于蓄水池算法的具体原理，可查阅参考文献2。  
直接上一个例子。  

```
       public static int[] reservoir(int[] array, int m) {
        int[] result = new int[m];
        int n = array.length;
        for(int i=0; i<n; i++) {
            int current_num = array[i];
            if(i < m) {
                result[i] = current_num;
            } else {
                int tmp = RandomUtils.nextInt(0, i+1);
                if(tmp < m) {
                    result[tmp] = current_num;
                }
            }
        }
        return result;
    }

    public static void massive_reservoir() {
        int[] array = {0, 1, 2, 3, 4};
        int m = 2;
        Map<Integer, Integer> map = new HashMap();
        for(int i=0; i<10000; i++) {
            int[] result = reservoir(array, m);
            for(int each: result) {
                map.put(each, map.getOrDefault(each, 0) + 1);
            }
        }
        for(Map.Entry<Integer, Integer> entry: map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
```  

上面代码模拟的是从{0, 1, 2, 3, 4}中随机抽取两个数，重复10000次。  
最后运行的结果如下：  

```
0: 4056
1: 4001
2: 3903
3: 4102
4: 3938
```  

## 3.随机抽取有序列表
上面抽样的结果都是无序的，只需要满足最后出现的概率相等即可。例如从{0, 1, 2, 3, 4}中抽取两个数，有可能先抽到0，也有可能先抽到4。如果我们要求抽样结果是有序的，那该怎么办？  
这种情况在实际中很常见。比如在流量分配系统中，流量都是流式过来的，或者说是有序的。假设有十个流量依次过来，需要在这十个流量随机选择三个投放三个广告，并且每个流量投放广告的概率都相等。这种场景就跟抽取有序列表类似。  
在Knuth的《计算机程序设计艺术 第2卷 半数值算法》一书中，给出了一个算法。  

```
void GenerateKnuth(int n,int m)
{
	int t=m;
	for(int i=0;i<n;i++)
		if(Rand(0,n-1-i)<t)//即以t/(n-i)的概率执行下面的语句
		{
			printf("%d\n",i);
			t--;
		}
}
```  
上面的n是指待抽取的列表总长度，m为想要抽取的结果个数。  

```
    public static List<Integer> randomtest() {
        int m = 3;
        int tmp = m;
        int[] array = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        int len = array.length;
        List<Integer> list = new ArrayList<>();
        for(int i=0; i<len; i++) {
            if(RandomUtils.nextInt(0, len - i) < tmp) {
                list.add(array[i]);
                tmp--;
            }
        }
        return list;
    }

    public static void massive_randomtest() {
        Map<Integer, Integer> map = new HashMap();
        for(int i=0; i<10000; i++) {
            List<Integer> list = randomtest();
            for(int each: list) {
                map.put(each, map.getOrDefault(each, 0) + 1);
            }
        }
        for(Map.Entry<Integer, Integer> entry: map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
```  
上面代码的写法是按照算法的思路来的。我在项目实现过程中，想了另外一种更容易理解，也更只管的实现方式。可以进行简单的证明如下:  
1.需要保证每个样本被抽到的概率是$\frac{m}{n}$  
2.第一个样本按$\frac{m}{n}$的概率进行抽样即可。  
3.对于第二个样本，如果第一个样本被抽中，其被抽中的概率为$\frac{m-1}{n-1}$。如果第一个样本没有被抽中，其被抽中的概率为$\frac{m}{n-1}$。第二个样本被抽中的概率为$\frac{m-1}{n-1} * \frac{m}{n} + \frac{m}{n-1} * (1 - \frac{m}{n}) =  \frac{m}{n}$。  
4.对于第i个样本，被抽中的概率为$\frac{m - k}{n - i + 1}$，其中k为前面已经抽中的个数，k<=m。即抽取第i个样本时候，如果前面已经抽中了k个，那么需要在剩下的n-i+1个样本中抽取m-k个。  

按照我自己理解的思路再实现一下，代码更简单，思路也更清晰一些：  

```
    public static List<Integer> randomtest() {
        int m = 3;
        double costednum = 0.0;
        int[] array = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        int len = array.length;
        List<Integer> list = new ArrayList<>();
        for(int i=0; i<len; i++) {
            double probability = (m - costednum) / (len - i);
            double value = Math.random();
            if(probability > value) {
                list.add(array[i]);
                costednum += 1;
            }
        }
        return list;
    }

    public static void massive_randomtest() {
        Map<Integer, Integer> map = new HashMap();
        for(int i=0; i<10000; i++) {
            List<Integer> list = randomtest();
            for(int each: list) {
                map.put(each, map.getOrDefault(each, 0) + 1);
            }
        }
        for(Map.Entry<Integer, Integer> entry: map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
```  

最后的输出结果为：  

```
0: 3013
1: 2941
2: 2929
3: 3060
4: 3020
5: 3047
6: 3058
7: 3067
8: 2917
9: 2948
```  

## 参考文献：
1.https://zh.wikipedia.org/wiki/%E7%AD%89%E5%B7%AE-%E7%AD%89%E6%AF%94%E6%95%B0%E5%88%97  
2.https://blog.csdn.net/bitcarmanlee/article/details/52719202  
