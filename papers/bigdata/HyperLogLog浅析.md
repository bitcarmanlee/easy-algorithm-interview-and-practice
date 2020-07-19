## 1.伯努利实验
如果我们不断投掷一个硬币，而且该硬币是均匀的，每次投掷出现正反面的概率相等都为0.5，知道我们得到第一个正面，假设这个过程为一次伯努利过程。那么，投掷一次硬币就得到正面的概率为1/2，投掷两次硬币得到正面的概率为1/4。  

现在有如下两个问题：  
1.如果进行上述n次伯努利过程，所有投掷次数均不大于k(每次都小于k)的概率是多少？  
2.如果进行上述n次伯努利过程，至少有一次不小于k(至少有一次大于等于k)的概率是多少？  

对于第一个问题，要求每次都小于k，如果是第k+1次才出现正面，则前k次均为反面的概率为$\frac{1}{2^k}$，$P_n(X \leq k) = (1 - \frac{1}{2^k})^n$。$P_n(X \leq k)$表示所有投掷次数均不大于k的概率。  


显然第二个问题的答案为$P_n(X > k) = 1 - (1 - \frac{1}{2^k})^n$  

当$n << 2 ^ k$时， $P_n(X \leq k) =1$。而当$n >>2 ^ k$时， $P_n(X > k) = 1$。如果翻译一下就是：当伯努利过程的次数n远小于$2^k$时，所有投掷次数均不大于k的概率是1，或者说至少有一次大于等于k的概率是0。反过来当伯努利过程的次数n远大于$2^k$时，所有投掷次数均不大于k的概率是0，而至少有一次大于等于k的概率是1。    

将上面的情况做一个对应：一过伯努利过程对应一个元素的比特串，正面对应1，反面对应0。投掷次数k为对应第一个"1"出现的位置。  

假设有一个集合的技术为n, k为所有元素中首个'1'出现的位置最大的那个元素的'1'的位置。如果n<<$2^k$，则得到k为当前值的概率几乎为0。同理，如果n>>$2^k$，则得到k为当前值的概率也几乎为0。因此$2^k$可以作为基数n的一个粗糙估计。  

上面可以总结为：进行n次抛硬币实验，每次分别记录下第一次抛到正面的投掷次数k，那么可以用n次实验中最大的抛掷次数$k_{max}$作为实验组数量n的估计：$\hat n = 2 ^ k$。  

再通俗点说明： 假设我们为一个数据集合生成一个8位的哈希串，那么我们得到00000111的概率是很低的，也就是说，我们生成大量连续的0的概率是很低的。生成连续5个0的概率是1/32，那么我们得到这个串时，可以估算，这个数据集的基数是32。  

## 2.分桶

上面的算法是比较粗糙的，我们可以接下来进一步优化得到比较准确的解。  

最简单的一种优化方法显然就是把数据分成m个均等的部分，分别估计其总数求平均后再乘以m，称之为分桶。对应到前面抛硬币的例子，其实就是把硬币序列分成m个均等的部分，分别用之前提到的那个方法估计总数求平均后再乘以m，这样就能一定程度上避免单一突发事件造成的误差。  

具体要怎么分桶呢？我们可以将每个元素的hash值的二进制表示的前几位用来指示数据属于哪个桶，然后把剩下的部分再按照之前最简单的想法处理。  

假设我要分2个桶，那么我只要去ele1的hash值的第一位来确定其分桶即可，之后用剩下的部分进行前导零的计算。  

假设有两个元素{ele1, ele2}，其二进制表示如下：  
```
hash(ele1) = 00110111
hash(ele2) = 10010001
```  

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200308172520798.png)  


## 3.调和平均数
LogLog算法完整的基数计算公式如下：  
$$DV_{LL} = constant * m * 2^{\bar R}$$  

其中m代表分桶数，R头上一道横杠的记号就代表每个桶的结果（其实就是桶中数据的最长前导零+1）的均值，相比我之前举的简单的例子，LogLog算法还乘了一个常数constant进行修正。（参考文献1）  


影响LogLog算法精度的一个重要因素就是，hash值的前导零的数量显然是有很大的偶然性的，经常会出现一两数据前导零的数目比较多的情况，所以HyperLogLog算法相比LogLog算法一个重要的改进就是使用调和平均数而不是平均数来聚合每个桶中的结果，HyperLogLog算法的公式如下：  

$$DV_{LL} = constant * m ^ 2 * (\sum_j ^m 2 ^ {-R_j}) ^ {-1}$$  

其中constant常数和m的含义和之前的LogLog算法公式中的含义一致，Rj代表(第j个桶中的数据的最大前导零数目+1)，为了方便理解，我将公式再拆解一下：  


![在这里插入图片描述](https://img-blog.csdnimg.cn/20200308173005251.png)  
其实从算术平均数改成调和平均数这个优化是很容易想到的，但是为什么LogLog算法没有直接使用调和平均数吗？网上看到一篇英文文章里说大概是因为使用算术平均数的话证明比较容易一些，毕竟科学家们出论文每一步都是要证明的，不像我们这里简单理解一下，猜一猜就可以了。  

## 4.细节微调
关于HyperLogLog算法的大体思想到这里你就已经全部理解了。  
不过算法中还有一些细微的校正，在数据总量比较小的时候，很容易就预测偏大，所以我们做如下校正：  
（DV代表估计的基数值，m代表桶的数量，V代表结果为0的桶的数目，log表示自然对数）  

```
if DV < (5 / 2) * m:
    DV = m * log(m/V)
```  

我再详细解释一下V的含义，假设我分配了64个桶（即m=64），当数据量很小时（比方说只有两三个），那肯定有大量桶中没有数据，也就说他们的估计值是0，V就代表这样的桶的数目。  

事实证明，这个校正的效果是非常好，在数据量小的时，估计得非常准确，有兴趣可以去玩一下外国大佬制作的一个HyperLogLog算法的仿真：  
http://content.research.neustar.biz/blog/hll.html  

## 5.constant选择  
constant常数的选择与分桶的数目有关，具体的数学证明请看论文，这里就直接给出结论：  
假设：m为分桶数，p是m的以2为底的对数  
$$p = log_2m$$  

则按如下的规则计算constant  

```
switch (p) {
   case 4:
       constant = 0.673 * m * m;
   case 5:
       constant = 0.697 * m * m;
   case 6:
       constant = 0.709 * m * m;
   default:
       constant = (0.7213 / (1 + 1.079 / m)) * m * m;
}
```  

## 6.stream lib中hyperloglog用法

stream-lib是github上的一个开源项目，里面包含有hyperloglog等许多算法。  
关于stream-lib的说明(github上的readme文件一部分)  
```
A Java library for summarizing data in streams for which it is infeasible to store all events. More specifically, there are classes for estimating: cardinality (i.e. counting things); set membership; top-k elements and frequency. One particularly useful feature is that cardinality estimators with compatible configurations may be safely merged.

These classes may be used directly in a JVM project or with the provided shell scripts and good old Unix IO redirection.

The ideas here are not original to us. We have endeavored to create useful implementations from iterating over the existing academic literature. As such this library relies heavily on the work of others. Please read the Sources and Reference sections.
```  


HyperLogLog 会计算每一个成员二进制值首位有多少个零，如果零的最大个数是n，则唯一值数量就是$2^n$。  
算法中有两个关键点，首先，成员的值必须是服从正态分布的，这一点可以通过哈希函数实现。stream-lib 使用的是 MurmurHash，它简单、快速、且符合分布要求，应用于多种基于哈希查询的算法。其次，为了降低计算结果的方差，集合成员会先被拆分成多个子集合，最后的唯一值数量是各个子集合结果的调和平均数。上文代码中，我们传递给 HyperLogLog 构造函数的整型参数就表示会采用多少个二进制位来进行分桶。最后，准确性可以通过这个公式计算：1.04/sqrt(2^log2m)。  

```
import com.clearspring.analytics.stream.cardinality.HyperLogLog;
import com.clearspring.analytics.stream.cardinality.ICardinality;
import org.junit.Test;

/**
 * Created by wanglei on 2020/3/8.
 */
public class Stream1 {

    @Test
    public void test() {
        ICardinality card = new HyperLogLog(16);
        for(int i=0; i<1000000; i++) {
            card.offer(i);
        }
        System.out.println(card.cardinality());
    }
}
```  

某次运行的结果为  

```
998908
```  

## 参考文献  
https://www.jianshu.com/p/55defda6dcd2  

