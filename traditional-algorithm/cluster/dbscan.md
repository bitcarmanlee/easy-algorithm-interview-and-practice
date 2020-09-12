## 1.简介
DBSCAN(Density-Based Spatial Clustering of Application with Noise)是一种基于密度的经典聚类算法，出现的时间大概是1996年前后。  

## 2.DBSCAN的一些基本概念
DBSCAN算法基于一组“邻域”参数(经常用$\epsilon$，MinPts)来描述样本分布的紧凑程度。若给定样本集$D= x_1, x_2, \cdots,x_m$，我们可以定义一下几个概念：  

1. $\epsilon$邻域：对$x_j \in  D$，其$\epsilon$邻域包含样本集 D中与$x_j$的距离不大于$\epsilon$的样本，  

$$N_{\epsilon}(\boldsymbol{x_j}) = \{ \boldsymbol{x_i} \in D \mid \text{dist}(\boldsymbol{x_i}, \boldsymbol{x_j}) \le \epsilon \}$$  

其中dist为距离的计算方法。  
2. 核心对象（core object) 若$x_j$的$\epsilon$邻域至少包含MinPts个样本，即$N_{\epsilon}(\boldsymbol{x_j}) = \{ \boldsymbol{x_i} \in D \mid \text{dist}(\boldsymbol{x_i}, \boldsymbol{x_j}) \le \epsilon \}  \geq MinPts$， 则$x_j$为一个核心对象。  
3. 密度直达（directly density-reachable）如果$x_j$位于$x_i$的某一$\epsilon$邻域中，且$x_i$是核心对象，则$x_j$可以由$x_i$密度直达。但是反过来不一定城里。  
4. 密度可达（density-reachable）对样本$x_i, x_j$，如果有样本序列$p_1, p_2, \cdots, p_n$，其中$p_1 = x_i， p_n = x_j$，且$p_{i+1}$由$p_i$密度直达，则称$x_j$由$x_i$密度可达。密度可达关系满足传递性，但不满足对称性。  
5. 密度相连（density-connected）对样本$x_i, x_j$，若存在$x_k$使得$x_i, x_j$均由$x_k$密度可达，则称$x_i, x_j$密度相连。显然密度相连是对称的。  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/dbscan/1.jpg)  

DBSCAN定义的基本概念(MinPts=3)。其中虚线部分为$\epsilon$邻域，$x_1$为核心对象，$x_2$由$x_1$密度直达，$x_3$由$x_1$密度可达，$x_3, x_4$密度相连。  

根据上面的定义，DBSCAN将“簇”定义为： 由密度可达关系导出的最大密度相连的样本集合。  

## 3.算法的过程
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/dbscan/2.jpg)  

在第1-7行中，算法先根据给定的邻域参数($\epsilon$, MinPts)找出所有核心对象；然后在第10-24行中，以任一核心对象为出发点，找出由其密度可达的样本生成聚类簇，直到所有核心对象均被访问过为止。  

## 4.算法的优缺点
优点：  
1.相比 K-平均算法，DBSCAN 不需要预先声明聚类数量。  
2.DBSCAN 可以找出任何形状的聚类，甚至能找出一个聚类，它包围但不连接另一个聚类，另外，由于 MinPts 参数，single-link effect （不同聚类以一点或极幼的线相连而被当成一个聚类）能有效地被避免。  
3.DBSCAN 能分辨噪音（局外点）。  
4.DBSCAN 只需两个参数，且对数据库内的点的次序几乎不敏感（两个聚类之间边缘的点有机会受次序的影响被分到不同的聚类，另外聚类的次序会受点的次序的影响）。  
5.DBSCAN 被设计成能配合可加速范围访问的数据库结构，例如 R*树。  
6.如果对资料有足够的了解，可以选择适当的参数以获得最佳的分类。  

缺点：  
1.DBSCAN 不是完全决定性的：在两个聚类交界边缘的点会视乎它在数据库的次序决定加入哪个聚类，幸运地，这种情况并不常见，而且对整体的聚类结果影响不大——DBSCAN 对核心点和噪音都是决定性的。DBSCAN* 是一种变化了的算法，把交界点视为噪音，达到完全决定性的结果。  
2.DBSCAN 聚类分析的质素受函数 regionQuery(P,ε) 里所使用的度量影响，最常用的度量是欧几里得距离，尤其在高维度资料中，由于受所谓“维数灾难”影响，很难找出一个合适的 ε ，但事实上所有使用欧几里得距离的算法都受维数灾难影响。  
3.如果数据库里的点有不同的密度，而该差异很大，DBSCAN 将不能提供一个好的聚类结果，因为不能选择一个适用于所有聚类的 minPts-ε 参数组合。  
4.如果没有对资料和比例的足够理解，将很难选择适合的 ε 参数。  

## 5.例子

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author: WangLei
#date: 2020/3/28


import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler


# #############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# #############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

```  

最后输出结果  

```
Estimated number of clusters: 3
Estimated number of noise points: 18
Homogeneity: 0.953
Completeness: 0.883
V-measure: 0.917
Adjusted Rand Index: 0.952
Adjusted Mutual Information: 0.916
Silhouette Coefficient: 0.626
```  

![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/cluster/dbscan/3.png)  

## 参考文献
1.https://zh.wikipedia.org/wiki/DBSCAN  
2.http://aandds.com/blog/dbscan.html  