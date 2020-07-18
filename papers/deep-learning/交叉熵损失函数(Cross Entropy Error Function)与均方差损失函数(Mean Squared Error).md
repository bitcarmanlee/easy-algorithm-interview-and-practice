## 1.均方差损失函数(Mean Squared Error)
均方差损失函数是预测数据和原始数据对应点误差的平方和的均值。计算方式也比较简单  
$$MSE = \frac{1}{N}(\hat y - y) ^ 2$$  

其中，N为样本个数。  

## 2.交叉熵损失函数(Cross Entropy Error Function)  

在分类问题中，尤其是在神经网络中，交叉熵函数非常常见。因为经常涉及到分类问题，需要计算各类别的概率，所以交叉熵损失函数又都是与sigmoid函数或者softmax函数成对出现。  

比如用神经网络最后一层作为概率输出，一般最后一层神经网络的计算方式如下：  
1.网络的最后一层得到每个类别的scores。  
2.score与sigmoid函数或者softmax函数进行计算得到概率输出。  
3.第二步得到的类别概率与真实类别的one-hot形式进行交叉熵计算。  

二分类的交叉熵损失函数形式  
$$\sum -y_ilog(\hat y_i) - (1-y_i)log(1-\hat y_i)$$  
上面的$y_i$表示类别为1,$\hat y_i$表示预测类别为1的概率。  

而多分类的交叉熵损失函数形式为  
$$-\sum_{i=1} ^n y_i log(\hat y_i)$$  

上面的式子表示类别有n个。单分类问题的时候，n个类别是one-hot的形式，只有一个类别$y_i=1$，其他n-1个类别为0。  

## 3.MSE与sigmoid函数不适合配合使用  
MSE的loss为  
$$MSE =- \frac{1}{N}(\hat y - y) ^ 2$$  
如果其与sigmoid函数配合使用，偏导数为  
$$\frac{\partial  Loss_i}{\partial w} = (y - \hat y) \sigma '(wx _i+ b)x_i  $$  
其中  
$$\sigma '(wx _i+ b) = \sigma (wx _i+ b) (1 - \sigma (wx _i+ b)) $$  

于是，在$\sigma (wx _i+ b)$的值接近0或者1的时候，其导数都接近0。这样会导致模型一开始的学习速度非常慢，所以MSE一般不会与sigmoid函数配合使用。  

## 4.交叉熵损失函数与sigmoid函数配合使用  

交叉熵损失函数与sigmoid函数配合使用，最终损失函数求导的结果为  
$$\frac{\partial  Loss_i}{\partial w} = (\hat y_i - y_i)x_i$$  

由此可见，求导的结果与$\hat y_i - y_i$与$x_i$的值有关，不会出现模型开始训练速度很慢的现象。  

具体的推导过程见参考文献1  
[交叉熵损失函数求导](https://blog.csdn.net/bitcarmanlee/article/details/51473567)  


## 5.交叉熵损失函数与softmax函数配合使用  
前面提到，在神经网络中，交叉熵损失函数经常与softmax配合使用。  
$$Loss = - \sum_i t_i lny_i$$  
softmax函数  
$$y_i = \frac{e^i}{\sum_j e^j} = 1 - \frac{\sum_{j \neq i} e^j}{\sum_j e^j}$$  

接下来求导  

$$
{\begin{aligned}
\frac{\partial  Loss_i}{\partial_i} & = - \frac{\partial  ln y_i}{\partial_i} \\\\
& = -\frac{\sum_j e^j}{e^i} \cdot \frac {\partial (\frac{e_i}{\sum_j e^j})}{\partial_i} \\\\
& = -\frac{\sum_j e^j}{e^i} \cdot (- \sum _ {j \neq i}e^j ) \cdot \frac{\partial( \frac {1} {\sum_j e^j} ) } { \partial_i} \\\\ 
& = \frac { \sum_j e^j \cdot \sum_{j \neq i} e^j}  {e^i } \cdot \frac { - e^i} { (\sum_j e^j) ^ 2} \\\\
& = -\frac { \sum_{j \neq i} e^j } { \sum_j e^j }  \\\\
& = -(1 - \frac{ e ^ i } { \sum_j e^j } ) \\\\
& = y_i - 1
\end{aligned}}
$$  

由此可见，交叉熵函数与softmax函数配合，损失函数求导非常简单！  


## 参考文献
1.https://blog.csdn.net/bitcarmanlee/article/details/51473567