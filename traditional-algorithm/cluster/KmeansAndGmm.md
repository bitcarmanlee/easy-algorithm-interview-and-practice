## 1.标准Kmeans
经典的标准kmeans算法无需多言，每个无监督学习的开场白一般都是标准kmeans算法。具体的原理不再多言，可以参考之前的文章：  
https://blog.csdn.net/bitcarmanlee/article/details/52092288  

标准的kmeans的优缺点，上面的文章也有详细介绍，再详细说一说kmeans++对于初始中心点的优化  

kmeans++中心点初始化步骤  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/kmeans/1.png)  
下面举个例子来说明怎么优化初始点。  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/kmeans/2.png)  
数据集中共有8个样本，分布以及对应序号如图所示。  
假设经过图2的步骤一后6号点被选择为第一个初始聚类中心，那在进行步骤二时每个样本的D(x)和被选择为第二个聚类中心的概率如下表所示：  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/kmeans/3.png)  
其中的P(x)就是每个样本被选为下一个聚类中心的概率。最后一行的Sum是概率P(x)的累加和，用于轮盘法选择出第二个聚类中心。方法是随机产生出一个0~1之间的随机数，判断它属于哪个区间，那么该区间对应的序号就是被选择出来的第二个聚类中心了。例如1号点的区间为[0,0.2)，2号点的区间为[0.2, 0.525)。  

 从上表可以直观的看到第二个初始聚类中心是1号，2号，3号，4号中的一个的概率为0.9。而这4个点正好是离第一个初始聚类中心6号点较远的四个点。这也验证了K-means的改进思想：即离当前已有聚类中心较远的点有更大的概率被选为下一个聚类中心。可以看到，该例的K值取2是比较合适的。当K值大于2时，每个样本会有多个距离，需要取最小的那个距离作为D(x)。  
(kmeans++优化中心点的例子来自参考文献1)  


## 2.kmeans python实现
用python实现一个kmeans的例子。  

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author: WangLei
#date: 2020/3/19

import numpy as np

class KMeansClassifier():

    def __init__(self, k=3, init_cent='random', max_iter=500):
        self._k = k
        self._init_cent = init_cent
        self._max_iter = max_iter
        self._clusterAssment = None
        self._labels = None
        self._sse = None

    def _cal_edist(self, arrA, arrB):
        return np.math.sqrt(sum(np.power(arrA - arrB, 2)))

    def _cal_mdist(self, arrA, arrB):
        return sum(np.abs(arrA, arrB))


    def _rand_cent(self, data_X, k):
        n = data_X.shape[1] # 特征维度
        centroids = np.empty((k, n)) #使用numpy生成一个k*n的矩阵，用于存储质心
        for j in range(n):
            minJ = min(data_X[:, j])
            rangeJ = float(max(data_X[:, j]) - minJ)
            centroids[:, j] = (minJ + rangeJ * np.random.rand(k, 1)).flatten()

        return centroids

    def fit(self, data_X):
        if not isinstance(data_X, np.ndarray) or isinstance(data_X, np.matrixlib.defmatrix.matrix):
            try:
                data_X = np.asarray(data_X)
            except:
                raise TypeError("numpy.ndarray resuired for data_X")

        m = data_X.shape[0] #获取样本的个数
        self._clusterAssment = np.zeros((m, 2))

        if self._init_cent == 'random':
            self._centroids = self._rand_cent(data_X, self._k)

        clusterChanged = True

        for _ in range(self._max_iter):
            clusterChanged = False
            for i in range(m): #将每个样本点分配到离它最近的质心所属的族
                minDist = np.inf
                minIndex = -1
                for j in range(self._k):
                    arrA = self._centroids[j,:]
                    arrB = data_X[i,:]
                    distJI = self._cal_edist(arrA, arrB)
                    if distJI < minDist:
                        minDist = distJI
                        minIndex = j
                if self._clusterAssment[i, 0] != minIndex or self._clusterAssment[i, 1] > minDist ** 2:
                    clusterChanged = True
                    self._clusterAssment[i, :] = minIndex, minDist ** 2

            if not clusterChanged:#若所有样本点所属的族都不改变,则已收敛,结束迭代
                break

            for i in range(self._k):  # 更新质心，将每个族中的点的均值作为质心
                index_all = self._clusterAssment[:, 0]  # 取出样本所属簇的索引值
                value = np.nonzero(index_all == i)  # 取出所有属于第i个簇的索引值
                ptsInClust = data_X[value[0]]  # 取出属于第i个簇的所有样本点
                self._centroids[i, :] = np.mean(ptsInClust, axis=0)  # 计算均值

        self._labels = self._clusterAssment[:, 0]
        self._sse = sum(self._clusterAssment[:, 1])

    def predict(self, X):  # 根据聚类结果，预测新输入数据所属的族
        # 类型检查
        if not isinstance(X, np.ndarray):
            try:
                X = np.asarray(X)
            except:
                raise TypeError("numpy.ndarray required for X")

        m = X.shape[0]  # m代表样本数量
        preds = np.empty((m,))
        for i in range(m):  # 将每个样本点分配到离它最近的质心所属的族
            minDist = np.inf
            for j in range(self._k):
                distJI = self._calEDist(self._centroids[j, :], X[i, :])
                if distJI < minDist:
                    minDist = distJI
                    preds[i] = j
        return preds

```

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author: WangLei
#date: 2020/3/19

from cluster.kmeans import KMeansClassifier

import numpy as np
import pandas as pd


def loadDataSet(infile):
    df = pd.read_csv(infile, sep='\t', header=None, dtype=str, na_filter=False)
    return np.array(df).astype(np.float)

def main():
    data_X = loadDataSet("data/testSet.txt")
    print(data_X.shape)
    k = 3
    clf = KMeansClassifier(k)
    clf.fit(data_X)
    cents = clf._centroids
    labels = clf._labels
    sse = clf._sse

    print(cents)
    print(labels)
    print(len(labels))
    print(sse)

main()
```  

数据如下  

```
1.658985	4.285136
-3.453687	3.424321
4.838138	-1.151539
-5.379713	-3.362104
0.972564	2.924086
-3.567919	1.531611
0.450614	-3.302219
-3.487105	-1.724432
2.668759	1.594842
-3.156485	3.191137
3.165506	-3.999838
-2.786837	-3.099354
4.208187	2.984927
-2.123337	2.943366
0.704199	-0.479481
-0.392370	-3.963704
2.831667	1.574018
-0.790153	3.343144
2.943496	-3.357075
-3.195883	-2.283926
2.336445	2.875106
-1.786345	2.554248
2.190101	-1.906020
-3.403367	-2.778288
1.778124	3.880832
-1.688346	2.230267
2.592976	-2.054368
-4.007257	-3.207066
2.257734	3.387564
-2.679011	0.785119
0.939512	-4.023563
-3.674424	-2.261084
2.046259	2.735279
-3.189470	1.780269
4.372646	-0.822248
-2.579316	-3.497576
1.889034	5.190400
-0.798747	2.185588
2.836520	-2.658556
-3.837877	-3.253815
2.096701	3.886007
-2.709034	2.923887
3.367037	-3.184789
-2.121479	-4.232586
2.329546	3.179764
-3.284816	3.273099
3.091414	-3.815232
-3.762093	-2.432191
3.542056	2.778832
-1.736822	4.241041
2.127073	-2.983680
-4.323818	-3.938116
3.792121	5.135768
-4.786473	3.358547
2.624081	-3.260715
-4.009299	-2.978115
2.493525	1.963710
-2.513661	2.642162
1.864375	-3.176309
-3.171184	-3.572452
2.894220	2.489128
-2.562539	2.884438
3.491078	-3.947487
-2.565729	-2.012114
3.332948	3.983102
-1.616805	3.573188
2.280615	-2.559444
-2.651229	-3.103198
2.321395	3.154987
-1.685703	2.939697
3.031012	-3.620252
-4.599622	-2.185829
4.196223	1.126677
-2.133863	3.093686
4.668892	-2.562705
-2.793241	-2.149706
2.884105	3.043438
-2.967647	2.848696
4.479332	-1.764772
-4.905566	-2.911070
```  

最后代码运行的结果为  

```
(80, 2)
[[ 2.99405094 -0.1605263 ]
 [-1.6334182   3.03655888]
 [-3.01169468 -3.01238673]]
[1. 1. 0. 2. 1. 1. 2. 2. 0. 1. 0. 2. 0. 1. 0. 2. 0. 1. 0. 2. 0. 1. 0. 2.
 1. 1. 0. 2. 0. 1. 2. 2. 0. 1. 0. 2. 1. 1. 0. 2. 1. 1. 0. 2. 0. 1. 0. 2.
 0. 1. 0. 2. 0. 1. 0. 2. 0. 1. 0. 2. 0. 1. 0. 2. 0. 1. 0. 2. 0. 1. 0. 2.
 0. 1. 0. 2. 0. 1. 0. 2.]
80
136.84604817873276
```

## 3.kmeans算法复杂度分析
假设有k个聚类中心，总共有n个点，迭代t轮，那么每一轮迭代都需要算n个点到k个中心点的距离，算法的总复杂度为$O(tnk)$  

## 4.GMM(Gaussian Mixed Model)
GMM混合高斯分布是多个高斯分布函数的线性组合，假设有随机变量$X$，GMM模型可以用如下公式表示  
$$p(\boldsymbol{x}) = \sum_{k=1}^K\pi_k \mathcal{N}(\boldsymbol{x}|\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$$  

其中，$\mathcal{N}(\boldsymbol{x}|\boldsymbol{\mu}\_k, \boldsymbol{\Sigma}\_k)$  
是模型中的第k个分量(component)。$p(\boldsymbol{x})$是混合系数（mixture coefficient)，而且有  
$$\sum_{k=1}^K\pi_k = 1$$  
$$0 \leq \pi_k \leq 1$$  

如果样本$X$是一维数据(Univariate)，高斯分布的概率密度函数PDF(Probability Density Function)为：  
$$P(x|\theta) = \frac{1}{\sqrt{2\pi\sigma^{2}}} exp(-\frac{(x-\mu)^2}{2\sigma^{2}})$$
  
当$X$为多维数据(Multivariate)时，其PDF如下：  

$$P(x|\theta) = \frac{1}{(2\pi)^{\frac{D}{2}}\left| \Sigma \right|^{\frac{1}{2}}}exp(-\frac{(x-\mu)^{T}\Sigma^{-1}(x-\mu)}{2})$$  

其中，$\mu$为期望，$\Sigma$为协方差矩阵，是一个对称矩阵。D为数据的维度。    

协方差：  
如果用$x_{ki}$表示随机变量$x_k$的第i个样本，n表示样本总数，则$x$第m维与第k维的协方差为  

$$\sigma\left(x_m,x_k\right)=\frac{1}{n-1}\sum_{i=1}^n\left(x_{mi}-\bar{x}\_m\right)\left(x_{ki}-\bar{x}_k\right)$$  

$$\Sigma=\left [
\begin{matrix}
\sigma(x_1, x_1) & \cdots & \sigma(x_1, x_d) \\\\
\cdots & \cdots & \cdots \\\\
\sigma(x_d, x_1) & \cdots  & \sigma(x_d, x_d) \\
\end{matrix} 
\right ]$$  

其中，对角线上的元素尾各随机变量的方差，而非对角线上的元素为两两随机变量之间的协方差。由协方差矩阵的定义易知，协方差矩阵为方针，大小为d*d，且为对称矩阵(symmetric matrix)。  

## 5.GMM聚类
GMM聚类的核心思想是假设所有的数据点来自多个参数不同的高斯分布，来自同一分布的数据点被划分为同一类。算法结果返回的是数据点属于不同类别的概率。  

提GMM，必然绕不过EM算法。反过来，提EM算法，一般也会提GMM，这两跟孪生兄弟一样经常成对出现，下面我们试着用简单的方式来描述一下EM算法。  

假设我们得到一组样本$x_t$，而且$x_t$服从高斯分布，但是高斯分布的参数未知，就是第四小节里提到的$x \sim N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$。我们的目标是找一个合适的高斯分布，确定分布参数，使得这个高斯分布能产生这组样本的可能性尽可能大。  

学过概率统计的同学应该有感觉，产生这组样本的可能性尽可能大，这个时候就轮到极大似然估计(Maximum Likehood Estimate, MLE)大显身手的时候了。  

假设样本集$X = x_1, x_2, \cdots, x_n$，而$p(x_n | \boldsymbol{\mu}, \boldsymbol{\Sigma})$是高斯分布的概率分布函数。如果假设样本抽样独立，样本集$X$的联合概率就是似然函数：  
$$L(\boldsymbol{\mu}, \boldsymbol{\Sigma}) = L(x_1, x_2, \cdots, x_n; \boldsymbol{\mu}, \boldsymbol{\Sigma}) = \prod_{i=0}^n p(x_n; \boldsymbol{\mu}, \boldsymbol{\Sigma})$$  

接下来的求解过程就是求极值了，学过高数的同学都知道，对上式求导，并令导数为0，就可以求得高斯分布的参数。  

所以最大化似然函数的意义在于：通过使得样本集的联合概率最大来对参数进行估计，从而选择最佳的分布模型。  

回到GMM。上面是只有一个高斯分布的情况，在GMM中，有多个高斯分布，我们并不知道样本来自哪个高斯分布。换句话说，  
$$p(\boldsymbol{x}) = \sum_{k=1}^K\pi_k \mathcal{N}(\boldsymbol{x}|\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$$  

中，$p(x)$的值我们并不知道，我们不光需要求解不同高斯分布的参数，还需要求解不同高斯分布的概率。  

我们引入一个隐变量$\gamma$，它是一个K维二值随机变量，在它的K维取值中只有某个特定的元素$\gamma_k$的取值为1，其它元素的取值为0。实际上，隐变量描述的就是：每一次采样，选择第k个高斯模型的概率，故有：  
$$p({\gamma _k} = 1) = {\pi _k}$$
  
当给定了$\gamma$的一个特定的值之后（也就是知道了这个样本从哪一个高斯模型进行采样），可以得到样本x的条件分布是一个高斯分布，满足：
  
$$p(x|{\gamma _k} = 1) = N(x|{\mu _k},{\Sigma _k})$$  

而实际上，每个样本到底是从这K个高斯模型中哪个模型进行采样的，是都有可能的。故样本y的概率为：  
$$p(x) = \sum\nolimits_\gamma  {p(\gamma )} p(y|\gamma ){\rm{ = }}\sum\limits_{{\rm{k}} = 1}^K {{\pi _k}N(x|{\mu _k},{\Sigma _k})}$$  


样本集X(n个样本点)的联合概率为：  
$$L(\mu ,\Sigma ,\pi ) = L({x_1},{x_2}...{x_N};\mu ,\Sigma ,\pi ) = \prod\limits_{n = 1}^N {p({x_n};\mu ,\Sigma ,\pi )}  = \prod\limits_{n = 1}^N {\sum\limits_{{\rm{k}} = 1}^K {{\pi \_k}N({x_n}|{\mu \_k},{\Sigma \_k})} }$$  
　　
对数似然函数表示为：  
$$\ln L(\mu ,\Sigma ,\pi ) = \sum\limits_{n = 1}^N {\ln \sum\limits_{{\rm{k}} = 1}^K {{\pi _k}N({x_n}|{\mu _k},{\Sigma _k})} }$$  

接下来再求导，令导数为0，可以得到模型参数$(\mu ,\Sigma ,\pi)$。  
到此为止，貌似问题已经解决了。但是在对数似然函数里面，里面还有求和。实际上没有办法通过求导的方法来求这个对数似然函数的最大值。  

具体的EM算法步骤参见参考文献2，公式比较多，就不复制粘贴了。  

## 6.GMM代码示例

```
import numpy as np
import itertools

from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn import mixture

# Number of samples per component
n_samples = 500

# Generate random sample, two components
np.random.seed(0)
C = np.array([[0., -0.1], [1.7, .4]])
X = np.r_[np.dot(np.random.randn(n_samples, 2), C),
          .7 * np.random.randn(n_samples, 2) + np.array([-6, 3])]

lowest_bic = np.infty
bic = []
n_components_range = range(1, 7)
cv_types = ['spherical', 'tied', 'diag', 'full']
for cv_type in cv_types:
    for n_components in n_components_range:
        # Fit a Gaussian mixture with EM
        gmm = mixture.GaussianMixture(n_components=n_components,
                                      covariance_type=cv_type)
        gmm.fit(X)
        bic.append(gmm.bic(X))
        if bic[-1] < lowest_bic:
            lowest_bic = bic[-1]
            best_gmm = gmm

bic = np.array(bic)
color_iter = itertools.cycle(['navy', 'turquoise', 'cornflowerblue',
                              'darkorange'])
clf = best_gmm
bars = []

# Plot the BIC scores
plt.figure(figsize=(8, 6))
spl = plt.subplot(2, 1, 1)
for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
    xpos = np.array(n_components_range) + .2 * (i - 2)
    bars.append(plt.bar(xpos, bic[i * len(n_components_range):
                                  (i + 1) * len(n_components_range)],
                        width=.2, color=color))
plt.xticks(n_components_range)
plt.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
plt.title('BIC score per model')
xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
    .2 * np.floor(bic.argmin() / len(n_components_range))
plt.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
spl.set_xlabel('Number of components')
spl.legend([b[0] for b in bars], cv_types)

# Plot the winner
splot = plt.subplot(2, 1, 2)
Y_ = clf.predict(X)
for i, (mean, cov, color) in enumerate(zip(clf.means_, clf.covariances_,
                                           color_iter)):
    v, w = linalg.eigh(cov)
    if not np.any(Y_ == i):
        continue
    plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

    # Plot an ellipse to show the Gaussian component
    angle = np.arctan2(w[0][1], w[0][0])
    angle = 180. * angle / np.pi  # convert to degrees
    v = 2. * np.sqrt(2.) * np.sqrt(v)
    ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
    ell.set_clip_box(splot.bbox)
    ell.set_alpha(.5)
    splot.add_artist(ell)

plt.xticks(())
plt.yticks(())
plt.title('Selected GMM: full model, 2 components')
plt.subplots_adjust(hspace=.35, bottom=.02)
plt.show()
```



关键步骤有注释，参考注释就好。  
最后出来的效果  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/kmeans/4.png)  

## 7.高斯分布于混合高斯分布流程小结
对于一个高斯分布，参数估计的流程一般如下：  
1.首先得到一些符合高斯分布的采样数据。  
2.假设有一个高斯分布最有可能得到这些采样数据，接下来求解该高斯分布的参数。  
3.求采样数据产生的联合概率P  
4.使用极大似然估计最大化P获得高斯分布的参数。  

如果是一个混合高斯分布，一般的求解流程如下  
1.首先得到一些符合混合高斯分布的采样数据。  
2.假设有一组高斯分布最有可能得到这些采样数据，接下来求解该高斯分布的参数。  
3.1 各个采样数据最有可能是从哪一个高斯分布产生的，相当于对采样数据做分类划分。  
3.2 各个类对划分到的样本，求样本产生的概率$P(x_t, \gamma_t| \boldsymbol{\mu}, \boldsymbol{\Sigma}, \pi)$  
3.3 求采样数据产生的概率(Q函数)  
3.4 最大化Q函数来优化混合高斯分布参数。
  
## 8 Kmeans与GMM的区别与联系
相同点  
两者都是迭代算法，并且迭代策略大致相同：算法开始对需要计算的参数赋初值，然后交替执行两个步骤。第一个步骤是对数据的估计，k-means是估计每个点所属簇，GMM是计算隐含变量的期望。第二个步骤是用第一步的估计值重新计算参数值，更新目标参数。其中k-means是计算簇心位置；GMM是计算各个高斯分布的中心位置和协方差矩阵。  
不同点  
1.k-means是计算簇心位置，GMM是计算各个高斯分布的参数。  
2.k-means是计算当前簇中所有元素的位置的均值，GMM是通过计算似然函数的最大值实现分布参数的求解的。  


## 参考文献
1.https://www.cnblogs.com/yixuan-xu/p/6272208.html  
2.https://blog.csdn.net/lin_limin/article/details/81048411  