## 1.bloom filter
布隆过滤器（英语：Bloom Filter）是1970年由布隆提出的。它实际上是一个很长的二进制向量和一系列随机映射函数。布隆过滤器可以用于检索一个元素是否在一个集合中。它的优点是空间效率和查询时间都远远超过一般的算法，缺点是有一定的误识别率和删除困难。  

## 2.两种错误率FP/FN

```
FP = A false positive error, or in short a false positive, commonly called a “false alarm”, is a result that indicates a given condition exists, when it does not.

FN = A false negative error, or in short a false negative, is a test result that indicates that a condition does not hold, while in fact it does.
```  

在bloom filter中，FP是集合里没有某元素，查找结果是有该元素。FN是集合中有某元素，查找结果是没有该元素。  

在bloom filter中，FP 会随着 BF 中插入元素的数量而增加——极限情况就是所有 bit 都为 1，这时任何元素都会被认为在集合里。而FN则为0，如果某元素在集合中，则一定能找到该元素。  

## 3.FP的推导
假设哈希函数以相等的概率选择位数组中的位置。如果 m 是位数组中的比特数，则在插入元素期间某一特定比特位不被某个哈希函数设置为 1 的概率是：  

$$1- \frac{1}{m}$$  
假设有k个哈希函数，则通过 k 个哈希函数都未将该位设置为 1 的概率是  
$$(1- \frac{1}{m}) ^ k$$  

那么，如果我们插入了 n 个元素，某个位仍然为 0 的概率就是：  

$$(1- \frac{1}{m}) ^ {nk}$$  

因此这一位的值为 1 的概率就是：  

$$1 - (1- \frac{1}{m}) ^ {nk}$$  

那么，BF 的误判率是怎么得出的？前面提到，我们主要关注 FP，即集合里没有某元素，查找结果是有该元素。  

现在我们要判断一个元素是否在集合中，假设这个元素本不在集合中，理论上来讲，经过 k 个哈希函数计算后得到的位数组的 k 个位置的值都应该是 0，如果发生了误判，即这 k 个位置的值都为 1，这个概率如下：  

$$(1 - (1- \frac{1}{m}) ^ {kn}) ^ k = (1- e^{-\frac{kn}{m}})^k$$  

## 4.stream lib中的bloom filter

```
    public void test2() {
        Filter filter = new BloomFilter(1000, 0.01);
        filter.add("abc");
        filter.add("def");
        filter.add("g");
        boolean result = filter.isPresent("123");
        System.out.println("result is: " + result);
    }
```  

`Filter filter = new BloomFilter(1000, 0.01);` 1000是在构建BitSet时跟bit数组位数有关的参数，0.01是错误率。  

## 5.Count-Min Sketch算法
CountMinSketch 是一种“速写”算法，能够使用较小的空间勾勒出数据集内各类事件的频次。比如，我们可以统计出当前最热门的推特内容，或是计算网站访问量最大的页面。当然，这一算法同样会牺牲一定的准确性。  


CountMinSketch算法的流程：  
1.选定d个hash函数，开一个 dxm 的二维整数数组作为哈希表  
2.于每个元素，分别使用d个hash函数计算相应的哈希值，并对m取余，然后在对应的位置上增1，二维数组中的每个整数称为sketch  
3.要查询某个元素的频率时，只需要取出d个sketch, 返回最小的那一个（其实d个sketch都是该元素的近似频率，返回任意一个都可以，该算法选择最小的那个）  


## 6.Count-Mean-Min Sketch
Count-Min Sketch算法对于低频的元素，结果不太准确，主要是因为hash冲突比较严重，产生了噪音，例如当m=20时，有1000个数hash到这个20桶，平均每个桶会收到50个数，这50个数的频率重叠在一块了。Count-Mean-Min Sketch 算法做了如下改进：  

1.来了一个查询，按照 Count-Min Sketch的正常流程，取出它的d个sketch  
2.对于每个hash函数，估算出一个噪音，噪音等于该行所有整数(除了被查询的这个元素)的平均值  
3.用该行的sketch 减去该行的噪音，作为真正的sketch  
4.返回d个sketch的中位数  

```
class CountMeanMinSketch {
    // initialization and addition procedures as in CountMinSketch
    // n is total number of added elements
    long estimateFrequency(value) {
        long e[] = new long[d]
        for(i = 0; i < d; i++) {
            sketchCounter = estimators[i][ hash(value, i) ]
            noiseEstimation = (n - sketchCounter) / (m - 1)
            e[i] = sketchCounter – noiseEstimator
        }
        return median(e)
    }
}
```  

Count-Mean-Min Sketch算法能够显著的改善在长尾数据上的精确度。  

## 参考文献
1.https://zh.wikipedia.org/wiki/%E5%B8%83%E9%9A%86%E8%BF%87%E6%BB%A4%E5%99%A8  
2.http://shzhangji.com/cnblogs/2017/08/27/an-introduction-to-stream-lib-the-stream-processing-utilities/  
3.https://soulmachine.gitbooks.io/system-design/content/cn/bigdata/frequency-estimation.html  