##1.one hot编码的由来
在实际的应用场景中，有非常多的特征不是连续的数值变量，而是某一些离散的类别。比如在广告系统中，用户的性别，用户的地址，用户的兴趣爱好等等一系列特征，都是一些分类值。这些特征一般都无法直接应用在需要进行数值型计算的算法里，比如CTR预估中最常用的LR。那针对这种情况最简单的处理方式是将不同的类别映射为一个整数，比如男性是0号特征，女性为1号特征。这种方式最大的优点就是简单粗暴，实现简单。那最大的问题就是在这种处理方式中，各种类别的特征都被看成是有序的，这显然是非常不符合实际场景的。

为了解决上述问题，其中一种可能的解决方法是采用独热编码（One-Hot Encoding）。  
独热编码即 One-Hot 编码，又称一位有效编码，其方法是使用N位状态寄存器来对N个状态进行编码，每个状态都由他独立的寄存器位，并且在任意时候，其中只有一位有效。可以这样理解，对于每一个特征，如果它有m个可能值，那么经过独热编码后，就变成了m个二元特征。并且，这些特征互斥，每次只有一个激活。因此，数据会变成稀疏的。（本段内容来自网络）

##2.one hot 编码的优点
由第一部分的分析，很容易看出one hot编码的优点：  
1.能够处理非连续型数值特征。  
2.在一定程度上也扩充了特征。比如性别本身是一个特征，经过one hot编码以后，就变成了男或女两个特征。  

##3.为什么能使用one hot
1.使用one-hot编码，将离散特征的取值扩展到了欧式空间，离散特征的某个取值就对应欧式空间的某个点。  
2.将离散特征通过one-hot编码映射到欧式空间，是因为，在回归，分类，聚类等机器学习算法中，特征之间距离的计算或相似度的计算是非常重要的，而我们常用的距离或相似度的计算都是在欧式空间的相似度计算，计算余弦相似性，基于的就是欧式空间。  
3.将离散型特征使用one-hot编码，可以会让特征之间的距离计算更加合理。比如，有一个离散型特征，代表工作类型，该离散型特征，共有三个取值，不使用one-hot编码，其表示分别是x_1 = (1), x_2 = (2), x_3 = (3)。两个工作之间的距离是，(x_1, x_2) = 1, d(x_2, x_3) = 1, d(x_1, x_3) = 2。那么x_1和x_3工作之间就越不相似吗？显然这样的表示，计算出来的特征的距离是不合理。那如果使用one-hot编码，则得到x_1 = (1, 0, 0), x_2 = (0, 1, 0), x_3 = (0, 0, 1)，那么两个工作之间的距离就都是sqrt(2).即每两个工作之间的距离是一样的，显得更合理。  


##4.sklearn里的one hot
sklearn作为广泛使用深受推崇的机器学习库，自然少不了one hot编码。  
首先上一段sklearn的自带例子：

```
import numpy as np
from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()
enc.fit([[0, 0, 3], [1, 1, 0], [0, 2, 1],[1, 0, 2]])
print "enc.n_values_ is:",enc.n_values_
print "enc.feature_indices_ is:",enc.feature_indices_
print enc.transform([[0, 1, 1]]).toarray()
```
  

代码运行结果  

```
enc.n_values_ is: [2 3 4]
enc.feature_indices_ is: [0 2 5 9]
[[ 1.  0.  0.  1.  0.  0.  1.  0.  0.]]
```
  
要想明白上面代码的意思，我们看看源码中的说明就明白了

```
   """Encode categorical integer features using a one-hot aka one-of-K scheme.

    The input to this transformer should be a matrix of integers, denoting
    the values taken on by categorical (discrete) features. The output will be
    a sparse matrix where each column corresponds to one possible value of one
    feature. It is assumed that input features take on values in the range
    [0, n_values).

    This encoding is needed for feeding categorical data to many scikit-learn
    estimators, notably linear models and SVMs with the standard kernels.

    Read more in the :ref:`User Guide <preprocessing_categorical_features>`.

Attributes
    ----------
    active_features_ : array
        Indices for active features, meaning values that actually occur
        in the training set. Only available when n_values is ``'auto'``.

    feature_indices_ : array of shape (n_features,)
        Indices to feature ranges.
        Feature ``i`` in the original data is mapped to features
        from ``feature_indices_[i]`` to ``feature_indices_[i+1]``
        (and then potentially masked by `active_features_` afterwards)

    n_values_ : array of shape (n_features,)
        Maximum number of values per feature.

```  

前面一部分是对one-hot的原理解释。Attributes部分是对属性的一些解释：  
n_values：是一个数组，长度为每个特征的所有出现类别的总和。具体到代码里，[[0, 0, 3], [1, 1, 0], [0, 2, 1],[1, 0, 2]]是我们的样本矩阵，[0, 0, 3]是一个样本，每个样本有三维，即三类特征。对于第一维或者说第一类特征，有0，1两种取值；第二类特征，有0，1，2两类特征；第三类特征，有0，1，2，3三类特征，所以  

```
enc.n_values_ is: [2 3 4]
```  
feature_indices_：根据说明，明显可以看出其是对n_values的一个累加。  
最后`enc.transform([[0, 1, 1]]).toarray()`，就是将[0,1,1]这个输入样本，用one-hot编码出来的结果咯。  

##5.不需要对特征进行归一化的情况
基于树的方法不需要进行特征的归一化。例如随机森林，bagging与boosting等方法。如果是基于参数的模型或者基于距离的模型，因为需要对参数或者距离进行计算，都需要进行归一化。

