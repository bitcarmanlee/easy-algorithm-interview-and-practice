## 1.CART树回顾
在正式讲Xgboost之前，我们先回顾一下CART树。
CART树的生成过程，就是递归构建二叉树的过程，本质上是在某个特征维度对样本空间进行划分。这种空间划分是一种NP Hard问题，因此一般都是用启发式的方式去求解，即求某个特征j的且分点s，使得
$$\min_ { j , s } \left[ \min _ { c _ { 1 } } \sum _ { x _ { i } \in R _ { 1 } ( j , s ) } \left( y _ { i } - c _ { 1 } \right) ^ { 2 } + \min _ { c _ { 2 } } \sum _ { x _ { i } \in R _ { 2 } ( j , s ) } \left( y _ { i } - c _ { 2 } \right) ^ { 2 } \right]$$

## 2.XGBoost叶子节点取值推导
XGBoost的大体思路跟GBDT一样，也是通过不断进行特征分裂添加树，来学习一个新的弱学习器，来拟合上次预测结果的残差。

首先来看一下XGBoost的损失函数
$$L ( \phi ) = \sum _ { i } l \left( y _ { i } , \hat { y } _ { i } \right) + \sum _ { k } \Omega \left( f _ { k } \right) ,\quad 其中 \quad \Omega \left( f _ { k } \right) = \gamma T + \frac { 1 } { 2 } \lambda | | w | | ^ { 2 }$$

很容易可以看出来
$\sum\limits_i l \left( y _ { i } , \hat { y } _ { i } \right)$是代表预测值与真实值的偏差，而$\sum\limits_k \Omega \left( f _ { k } \right)$为正则项。

其中，$y_i$为样本的真实值，$\hat y_ i$为预测值。$f_k$表示第k棵树，$\gamma$为叶子树的正则项，起到剪枝的作用，T为树的叶子节点个数，$w$为叶子节点的分数，$\lambda$为叶子节点分数的正则项，起到防止过拟合的作用。

前面树系列的文章提到过很多次，boost系列算法的核心思想是用新生成的树拟合上次预测的残差(对于GBDT来说是上次预测的负梯度方向)。生成第t棵树后，预测值可以写为
$$\hat y_i = \hat y_i ^{t-1} + f_t(x)$$

此时，损失函数可以表示为

$$L^t = \sum _{i=1} l ( y _i^t , \hat y_i ^{t-1}) + f_t(x_i) + \Omega (f _t)$$

于是我们要找一个$f_t$让损失函数最小。对上面的式子进行泰勒展开
$$\mathcal { L } ^ { ( t ) } \simeq \sum _ { i = 1 } ^ { n } \left[ l \left( y _ { i } , \hat { y } ^ { ( t - 1 ) } \right) + g _ { i } f _ { t } \left( \mathbf { x } _ { i } \right) + \frac { 1 } { 2 } h _ { i } f _ { t } ^ { 2 } \left( \mathbf { x } _ { i } \right) \right] + \Omega \left( f _ { t } \right)$$

其中，
$$g_i = \frac{\partial l(y_i, \hat y_i ^{t-1})} {\partial \hat y_i ^{t-1}}$$
$$h_i = \frac{\partial ^ 2 l(y_i, \hat y_i ^{t-1})} {\partial (\hat y_i ^{t-1})^2}$$

其中$g_i, h_i$的含义可以按如下方式理解
假设目前已经有t-1棵数，这t-1棵树组成的模型对第i个训练样本有一个预测值$\hat y_i$，$\hat y_i$与真实值$y_i$肯定有差距，这个差距可以用$l(y_i, \hat y_i)$这个损失函数来衡量，所以此处的$g_i$与$h_i$就是对于该损失函数的一阶导和二阶导。(参考文献1)


搞定了前面的损失函数部分，接下来再观察一下正则项
$$ \Omega (f_t) = \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$$

对于上面的正则项，我们最简单的理解方式为：要使模型尽可能简单，那就是叶子节点的个数T要小，同时叶子节点上的值也尽可能小。

因为前t-1棵树的预测分数与y的残差对目标函数优化不影响, 可以直接去掉，所以损失函数可以写成

$$\mathcal { L } ^ { ( t ) } \simeq \sum _ { i = 1 } ^ { n } \left[ g _ { i } f _ { t } \left( \mathbf { x } _ { i } \right) + \frac {1} {2} h_i f _ { t } ^ { 2 } \left( \mathbf { x } _ { i } \right) \right] + \Omega \left( f _ { t } \right)$$

上面式子的含义是将每个样本的损失函数相加，而每个样本最终都会落到一个叶子节点上，所以我们可以将所有同一个叶子结点的样本重组起来
$$
\begin{align}
\hat{ \mathcal { L }}^{(t)} & =\sum_{i=1}^n [g_if_t(x_i) + \frac12h_tf_t^2(x_i)] + \Omega(f_t) \\
 & =\sum_{i=1}^n [g_if_t(x_i) + \frac12h_tf_t^2(x_i)] + \gamma T+\frac{1}{2}\lambda\sum\limits_{j=1}^{T}w_j^2 \\ 
 & = \sum\limits_{j=1}^{T} [(\sum\limits_{i\in I_j}g_i)w_j+\frac{1}{2}(\sum\limits_{i\in I_j}h_i+\lambda) w_j^2]+\gamma T \\ 
 & = \frac{1}{2}\sum\limits_{j=1}^{T} (H_j+\lambda)(w_j + \frac{G_j}{H_j+\lambda})^2+\gamma T -\frac{1}{2}\sum\limits_{j=1}^{T}\frac{G_j^2}{H_j+\lambda} 
\end{align}
$$

其中，$G_j = \sum _{i \in I_j} g_i$是落入叶子节点i所有样本一阶梯度的总和，而$H_j = \sum _{i \in I_j} h_i$是落入叶子节点i所有样本二阶梯度的总和。

基于中学数学的原理，我们可以得知：
当
$$w_j^* = -\frac{G_j}{H_j+\lambda}$$
时，损失函数最小。此时最终的损失函数大小为
$$\hat{\mathcal { L }}^{*} =-\frac{1}{2}\sum\limits_{j=1}^{T}\frac{G_j^2}{H_j+\lambda}+\gamma T$$


## 3.与牛顿法的关系
上面我们推导过程中，用到了二阶导数。而常见的基于二阶导数的优化方法就是牛顿法，下面我们看看与牛顿法的关系。
假设有一个函数$f(x)$二阶可微，我们对其进行泰勒展开到二阶，有
$$f(x) = f(x_k) + f'(x_k)(x-x_k) + f''(x_k)(x-x_k)^2$$
上面的式子对x求导，并令导数等于0
$$f'(x_k) +  f''(x_k)(x-x_k) = 0$$

可以得到x的迭代公式为
$$x = x_k - \frac{f'(x_k)}{f''(x_k)}$$
这就是牛顿法的迭代公式。

对比一下叶子节点的取值方式
$$w_j^* = -\frac{G_j}{H_j+\lambda}$$
与牛顿法唯一的区别在于，分母上二阶导多了一个正则项$\lambda$，形式上完全一致，就是一阶导除以二阶导，与牛顿法的形式完全一致。

## 4.XGBoost的树分裂方式
上面推导了这么一大串，都是在分析叶子节点怎么取值。提升树系列的算法，还有很重要的一点是树的分裂方式。
首先我们回顾一下其他算法比如GBDT是怎么进行分裂的。标准的做法是选择MSE作为损失函数，采用启发式的方式来选择某个特征j的切分点s进行分裂。这个分裂的过程，并不一定总与损失函数相关。比如在分类树中，我们一般都会用对数损失函数(交叉熵)来评估模型的最终效果，这个时候树分裂的结果与损失函数就没有直接的关系。

XGBoost的树分裂是直接与损失函数相关的。在分裂的时候，会计算损失函数的增益Gain
$$ Gain = \frac{1}{2} \left[\frac{G_L^2}{H_L+\lambda}  + \frac{G_R^2}{H_R+\lambda} - \frac{(G_L + G_R)^2}{H_L + H_R+\lambda} \right] - \gamma$$

上面这个式子其实很容易理解
$$\frac{(G_L + G_R)^2}{H_L + H_R+\lambda}$$是分裂前最终的损失函数值，而
$$\frac{G_L^2}{H_L+\lambda}, \frac{G_R^2}{H_R+\lambda} $$
分别为分裂后的左右子树的损失函数值

那树进行分裂的时候，自然希望损失函数减少得越多越好。
前面我们推导出了损失函数最终的表达式

$$\hat{\mathcal { L }}^{*} =-\frac{1}{2}\sum\limits_{j=1}^{T}\frac{G_j^2}{H_j+\lambda}+\gamma T$$


那我们想要的结果就是分列前的损失函数减去分裂后的损失函数，差值最大，注意前面的负号，最后的分裂准则为
$$max\left(\frac{G_L^2}{H_L+\lambda} + \frac{G_R^2}{H_R+\lambda} - \frac{(G_L + G_R)^2}{H_L + H_R+\lambda}\right)$$

## 5.XGBoost的各种Tricks总结
防止过拟合方法：
1.加入了正则项，对叶子节点数量，叶子节点分数加入了正则惩罚项。
2.加入了学习率，减少了单棵树影响，给后面树的优化留了更多空间。
3.列采样(特征采样)，与随机森林类似，不仅来带来更好的效果，还可以提高运行速度。

缺失值的处理
在别的算法中，一般会使用中位数，均值或者两者进行融合计算的方式去处理缺失值。但是xgboost能处理缺失值，模型允许缺失值存在。
在寻找分裂点的时候，不对该特征缺失的样本进行遍历，只遍历该特征有的样。具体实现时，将该特征值缺失的样本分别分配到左叶子节点与右叶子节点，分别计算增益，然后选择增益较大的方向进行分裂即可。如果训练样本中没有缺失值，而预测时有缺失，默认将缺失值划分到右子节点。

分裂点的选择
并不把所有特征值间的间隔点作为候选分裂点，而是用分位数的方法将其作为分裂的候选集。

并行处理
XGBoost中虽然树之间是串行关系，但是同层级的节点可以并行。对于某个节点，节点内选择最佳分裂点与计算分裂点的增益是可以并行的。

基学习器(弱学习器)
传统的GBDT与CART树作为基分类器，XGBoost不仅支持CART树，还支持线性分类器，这个时候xgboost就相当于带L1与L2正则项的逻辑斯蒂回归（分类问题）或者线性回归（回归问题）。

## 6.XGBoost 与GBDT的对比
主要的区别其实就是上面的Tricks。


## 参考文献
1.https://www.jianshu.com/p/ac1c12f3fba1