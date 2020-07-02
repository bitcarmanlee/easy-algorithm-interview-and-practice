## 1.Gamma函数
首先我们可以看一下Gamma函数的定义：  
$$\Gamma(x) = \int _{0}^{\infty}t^{x-1} e^{-t}dt$$  

Gamma的重要性质包括下面几条：  
1.递推公式：$\Gamma(x+1)=x\Gamma(x)$  
2.对于正整数n, 有$\Gamma(n+1) = n!$  
因此可以说Gamma函数是阶乘的推广。  
3.$\Gamma(1) = 1$  
4.$\Gamma(\frac{1}{2}) = \sqrt{\pi}$  

关于递推公式，可以用分部积分完成证明：  
$$\begin{aligned}
\Gamma(n+1) &= \int _{0}^{\infty}t^{n} e^{-t}dt \\\\
& = -\int _{0}^{\infty}t^{n}d(e^{-t}) \\\\
& = -(t^{n}e^{-t} - n\int _{0}^{\infty} e^{-t} \cdot t ^ {n-1}dt) 
\end{aligned}$$


由洛必达法则，易知括号内第一项为0, 则可以得出$\Gamma(n+1)=n\Gamma(n)$  


## 2.Beta函数
B函数，又称为Beta函数或者第一类欧拉积分，是一个特殊的函数，定义如下：  
$$B(x, y) = {\int _{0}^{1}t^{\alpha -1}(1-t)^{\beta -1}\,dt}$$  

B函数具有如下性质：  
1.$B(x,y) = B(y, x)$  
2.$B(x,y) = \frac{(x - 1)!(y - 1)!}{(x + y -1)!}$  
3.$B(x, y) = \frac{\Gamma(x) \Gamma(y)}{\Gamma(x+y)}$  

## 3.Beta分布
在介绍贝塔分布(Beta distribution)之前，需要先明确一下先验概率、后验概率、似然函数以及共轭分布的概念。  

1.通俗的讲，先验概率就是事情尚未发生前，我们对该事发生概率的估计。利用过去历史资料计算得到的先验概率，称为客观先验概率； 当历史资料无从取得或资料不完全时，凭人们的主观经验来判断而得到的先验概率，称为主观先验概率。例如抛一枚硬币头向上的概率为0.5，这就是主观先验概率。  
2.后验概率是指通过调查或其它方式获取新的附加信息，利用贝叶斯公式对先验概率进行修正，而后得到的概率。  
3.先验概率和后验概率的区别：先验概率不是根据有关自然状态的全部资料测定的，而只是利用现有的材料(主要是历史资料)计算的；后验概率使用了有关自然状态更加全面的资料，既有先验概率资料，也有补充资料。另外一种表述：先验概率是在缺乏某个事实的情况下描述一个变量；而后验概率（Probability of outcomes of an experiment after it has been performed and a certain event has occured.）是在考虑了一个事实之后的条件概率。  
4.共轭分布(conjugacy)：后验概率分布函数与先验概率分布函数具有相同形式  

先验概率和后验概率的关系为：  
$$posterior = likelihood * prior$$  

Beta分布的概率密度函数为：  
$${\begin{aligned}
f(x;\alpha ,\beta )&={\frac {x^{\alpha -1}(1-x)^{\beta -1}}{\int _{0}^{1}u^{\alpha -1}(1-u)^{\beta -1}\,du}}\\\\
&={\frac {\Gamma (\alpha +\beta )}{\Gamma (\alpha )\Gamma (\beta )}}\,x^{\alpha -1}(1-x)^{\beta -1}\\\\
&={\frac {1}{\mathrm {B} (\alpha ,\beta )}}\,x^{\alpha -1}(1-x)^{\beta -1}
\end{aligned}}$$  

随机变量X服从参数为 $\alpha$ ,$\beta$ 的Β分布通常写作  
$$X\sim {\textrm {Be}}(\alpha ,\beta )$$  

Beta分布与Gamma分布的关系为：  
$$B(x, y)=\frac{\Gamma(x)\Gamma(y)}{\Gamma(x+y)}$$  

用一句话来说，beta分布可以看作一个概率的概率分布，当你不知道一个东西的具体概率是多少时，它可以给出了所有概率出现的可能性大小。  

Beta分布的期望与方差分别为：  
$$\mu = E(X) = \frac {\alpha} {\alpha + \beta}$$  
$$Var(X) = E(X-\mu) ^ 2 = \frac{\alpha \beta}{(\alpha + \beta) ^ 2(\alpha + \beta + 1)}$$  

## 4.Beta分布是二项分布的共轭先验
这个结论很重要，在实际中应用也相当广泛。  
在这之前，我们先简单回顾一下伯努利分布与二项分布。  
伯努利分布(Bernoulli distribution)有称为0-1分布，伯努利分布式基于伯努利实验(Bernoulli trial)而来。  

伯努利试验是只有两种可能结果的单次随机试验,即对于一个随机变量X来说:  
$P_r[X=1] = p$  
$P_r[X=0] = 1-p$  
伯努利实验本质上即为"YES OR NO"的问题。最常见的一个例子就是抛硬币。  
如果进行一次伯努利实验，假设成功(X=1)的概率为$p(0<=p<=1)$，失败(X=0)的概率为$1-p$，称随机变量X服从伯努利分布。  

二项分布(Binomial distribution)是n重伯努利试验成功次数的离散概率分布。  
如果试验E是一个n重伯努利试验，每次伯努利试验的成功概率为p，X代表成功的次数，则X的概率分布是二项分布，记为X~B(n,p)，其概率质量函数为  
$$P\{X=k\} = C_n^k p^k (1-p)^{n-k}, k = 0, 1, 2, \cdots, n$$  
从上面的定义很明显可以看出，伯努利分布是二项分布在n=1时的特例。  
二项分布使用最广泛的例子就是抛硬币了，假设硬币正面朝上的概率为p，重复扔n次硬币，k次为正面的概率即为一个二项分布概率。  

在实验数据较少的情况下，如果我们直接用极大似然估计，二项分布的参数可能会出现过拟合的现象。比如，扔硬币三次都是正面，那么最大似然法预测以后的所有抛硬币结果都是正面。为了避免这种情况的发生，可以考虑引入先验概率分布$p(\mu)$来控制参数$\mu$，防止过拟合现象的发生。那么我们应该如何选择$p(\mu)$？  

前面我们提到，先验概率和后验概率的关系为：  
$$posterior = likelihood * prior$$  

二项分布的似然函数为:$\mu^m (1-\mu)^n$  
如果选择的先验概率$p(\mu)$也是$\mu$与$(1-\mu)$次方乘积的关系，那么后验概率的分布形式与先验将一样，这样先验概率与后验概率就是共轭分布了。  

由第三部分，我们知道Beta分布的概率密度函数为：  
$$Beta(\mu|, \alpha, \beta) = \frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}x^{\alpha -1}(1-x)^{\beta -1}$$  
正好满足我们上面的要求！所以说，Beta分布式二项式分布的共轭先验！  

## 5.多项式分布
将二项式分布推广到多项式分布(Multinomial Distribution)，二项式分布式n次伯努利实验，规定了每次的实验结果只有两个。现在还是做n次实验，只不过每次实验的结果变成了m个，且m个结果发生的概率互斥且和为1，则发生其中一个结果X次的概率就是多项式分布。    
扔骰子是典型的多项式分布。骰子有6个面对应6个不同的点数，这样单次每个点数朝上的概率都是1/6（对应p1~p6，它们的值不一定都是1/6，只要和为1且互斥即可，比如一个形状不规则的骰子）,重复扔n次，如果问有k次都是点数6朝上的概率就是    
$$P\{X = k\} = C_n ^ k p_6 ^ k(1 - p_6) ^ {n-k}, k = 0, 1, 2, \cdots, n$$  

而多项式分布的一般概率质量函数为：  
$$P\{x_1, x_2, \cdots,x_k\} = \frac{n!}{m_1!m_2!\cdots m_k!}\prod_{i=1}^n p_i ^{m_i}, \sum_{i=0} ^n p_i = 1$$  
将试验进行N次，记第i种可能发生的次数为$m_i$，$\sum_i ^ k m_i = n$  

简单推导一下概率质量函数的推导：  
k种独立的取值可能，n次实验，每种可能的概率为$p_1, p_2, \cdots, p_k$。  
则第一种被选中$m_1$次，第二种被选中$m_2$次，第k种被选中$m_k$次的概率为：  

$$C_n^{m_1}p_1^{m_1}C_{n-m_1}^{m_2}p_2^{m_2}\cdots C_{n-m_1-m_2-\cdots-m_{k-1}}^{m_k}p_k^{m_k}$$  
展开既可以得到上面的结果。  

## 6.Dirichlet狄利克雷分布
前面我们讲到Beta分布式二项式分布的共轭先验，Dirichlet分布则是多项式分布的共轭先验。  
Dirichlet（狄利克雷）同时可以看做是将Beta分布推广到多变量的情形。概率密度函数定义如下  
$$Dir(\vec p|\vec \alpha) = \frac{1}{B(\vec \alpha)} \prod_{k=1}^{K}p_{k}^{\alpha_{k}-1}$$  
其中，$\vec \alpha = (\alpha_{1},\alpha_{2},\ldots,\alpha_{K})$为Dirichlet分布的参数。且有：  
$$\alpha_{1},\alpha_{2},\dots,\alpha_{K} > 0$$  

$B(\vec \alpha)$表示 Dirichlet分布的归一化常数  
$$B(\vec \alpha)=\int \prod_{k=1}^{K}p_{k}^{\alpha_{k}-1} \ d\vec p$$  

类似于Beta函数有以下等式成立：   
$$B(\vec\alpha) = \frac{\Gamma(\sum_{k=1}^{K}\alpha_{k})}{\prod_{k=1}^{K}\Gamma(\alpha_{k})}$$  

Dirichlet分布的期望为：   
$$E(\vec p) = (\frac{\alpha_{1}}{\sum_{k=1}^{K}\alpha_{k}},\frac{\alpha_{2}}{\sum_{k=1}^{K}\alpha_{k}},\ldots,\frac{\alpha_{K}}{\sum_{k=1}^{K}\alpha_{k}})$$  



## 参考文献：
1.https://blog.csdn.net/a358463121/article/details/52562940  带你理解beta分布  
2.https://zh.wikipedia.org/wiki/Β分布  
3.https://zh.wikipedia.org/wiki/%E4%BC%BD%E7%8E%9B%E5%88%86%E5%B8%83  
4.https://zh.wikipedia.org/wiki/Β函数  
5.https://blog.csdn.net/Michael_R_Chang/article/details/39188321  
6.https://cosx.org/2013/01/lda-math-beta-dirichlet/  LDA-math - 认识 Beta/Dirichlet 分布  
7.https://zhuanlan.zhihu.com/p/31470216 一文详解LDA主题模型  