## 1.简介
层次聚类(Hierarchical Clustering)通过计算各类别中数据之间的相似度，最终创建一棵有层次的嵌套聚类树。起核心思想是基于各"簇"之间的相似度，在不同层次上分析数据，得到最终的树形聚类结构。  

## 2.agglomerative与divisive
自底向上聚合（agglomerative）策略和自顶向下分拆（divisive）策略是层次聚类中常见的两种划分策略。  

算法的基本步骤为  
1.计算数据集的相似矩阵。  
2.先假设每个样本点为一个簇类。  
3.迭代：合并相似度最高的两个簇类，并且更新相似矩阵。  
4.当簇类或者迭代次数满足终止条件时，算法结束。  


我们选择一个以自底向上聚合的例子，来说明层次聚类的具体过程。  
假定数据点之前的相似度以距离来计算，现在有如下点  

```
A 16.9
B 38.5
C 39.5
D 80.8
E 82
F 34.6
G 116.1
```  

然后计算如下相似矩阵(用欧式距离表示两点的相似度)  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/hierarchy/1.png)  

由上表可以看出，BC两点之间的距离是最近的，所以认为BC最相似，将其归为一类，并重新计算各数据点的相似矩阵。数据点间的距离计算方式与之前的方法一样。这里需要说明的是组合数据点(B,C)与其他数据点间的计算方法。当我们计算(B,C)到A的距离时，需要分别计算B到A和C到A的距离均值，这种计算方式叫做Average Linkage。  
接下来我们再观察，发现DE之间的距离最小，因此将DE化为一类，并再次计算各数据点之间的距离。  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/hierarchy/2.png)  
如此不停迭代，直到算法满足终止条件退出为止。  
(本例中的数据来自参考文献1)  

## 3.如何计算两个簇(组合数据点)之间的距离

1.单链接法(single linkage algorithm)，即计算两个簇之间最近样本之间的距离。用数学式子表达就是  
$$dist(C1, C2) = \min \limits_{p_i \in C1, p_j \in C2} dist(p_i, p_j)$$  

如果用图表示更为形象  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/hierarchy/3.png)  

2.全链接算法(complete linkage algorithm)，即计算两个簇之间最远样本之间的距离。用数学式子表达就是  
$$dist(C1, C2) = \max \limits_{p_i \in C1, p_j \in C2} dist(p_i, p_j)$$  
如果用图表示更为形象  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/hierarchy/4.png)  

3.均链接算法（average-linkage algorithm）即计算簇类C1和C2的距离等于两个簇类所有样本对的距离平均，数学表达式为  
$$dist(C1, C2) =\frac{1}{|C1|  |C2|} \sum \limits_{p_i \in C1, p_j \in C2} dist(p_i, p_j)$$  
其中|C1|，|C2|分别表示簇类的样本个数  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/hierarchy/5.png)  

## 4.算法优缺点
优点：  
1.可以发现类的层次关系，可解释性较强。  
2.可以聚类各种形状。  
3.距离与相似的定义比较灵活，可以比较自由进行选择。  
缺点  
1.计算复杂度较高，不太适合大样本数据集。  
2.算法很可能聚类成链状  

## 5.实例

```
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

np.random.seed(0)

# Generate waveform data
n_features = 2000
t = np.pi * np.linspace(0, 1, n_features)


def sqr(x):
    return np.sign(np.cos(x))

X = list()
y = list()
for i, (phi, a) in enumerate([(.5, .15), (.5, .6), (.3, .2)]):
    for _ in range(30):
        phase_noise = .01 * np.random.normal()
        amplitude_noise = .04 * np.random.normal()
        additional_noise = 1 - 2 * np.random.rand(n_features)
        # Make the noise sparse
        additional_noise[np.abs(additional_noise) < .997] = 0

        X.append(12 * ((a + amplitude_noise)
                 * (sqr(6 * (t + phi + phase_noise)))
                 + additional_noise))
        y.append(i)

X = np.array(X)
y = np.array(y)

n_clusters = 3

labels = ('Waveform 1', 'Waveform 2', 'Waveform 3')

# Plot the ground-truth labelling
plt.figure()
plt.axes([0, 0, 1, 1])
for l, c, n in zip(range(n_clusters), 'rgb',
                   labels):
    lines = plt.plot(X[y == l].T, c=c, alpha=.5)
    lines[0].set_label(n)

plt.legend(loc='best')

plt.axis('tight')
plt.axis('off')
plt.suptitle("Ground truth", size=20)


# Plot the distances
for index, metric in enumerate(["cosine", "euclidean", "cityblock"]):
    avg_dist = np.zeros((n_clusters, n_clusters))
    plt.figure(figsize=(5, 4.5))
    for i in range(n_clusters):
        for j in range(n_clusters):
            avg_dist[i, j] = pairwise_distances(X[y == i], X[y == j],
                                                metric=metric).mean()
    avg_dist /= avg_dist.max()
    for i in range(n_clusters):
        for j in range(n_clusters):
            plt.text(i, j, '%5.3f' % avg_dist[i, j],
                     verticalalignment='center',
                     horizontalalignment='center')

    plt.imshow(avg_dist, interpolation='nearest', cmap=plt.cm.gnuplot2,
               vmin=0)
    plt.xticks(range(n_clusters), labels, rotation=45)
    plt.yticks(range(n_clusters), labels)
    plt.colorbar()
    plt.suptitle("Interclass %s distances" % metric, size=18)
    plt.tight_layout()


# Plot clustering results
for index, metric in enumerate(["cosine", "euclidean", "cityblock"]):
    model = AgglomerativeClustering(n_clusters=n_clusters,
                                    linkage="average", affinity=metric)
    model.fit(X)
    plt.figure()
    plt.axes([0, 0, 1, 1])
    for l, c in zip(np.arange(model.n_clusters), 'rgbk'):
        plt.plot(X[model.labels_ == l].T, c=c, alpha=.5)
    plt.axis('tight')
    plt.axis('off')
    plt.suptitle("AgglomerativeClustering(affinity=%s)" % metric, size=20)


plt.show()

```  

其中的一个结果为  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/hierarchy/6.png)  



## 参考文献
1.https://www.cnblogs.com/zongfa/p/9344769.html
