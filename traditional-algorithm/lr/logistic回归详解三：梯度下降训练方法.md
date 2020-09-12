在前文中，  
http://blog.csdn.net/bitcarmanlee/article/details/51165444，  
我们已经对logistic回归的cost function做了完整的推导。如果是单个样本，其损失函数为：  
$$cost(h_{\theta}(x),y) = -y_ilog(h_{\theta}(x)) - (1-y_i)log(1-h_{\theta}(x))$$  

## 1.梯度下降的原理
现在问题就转化为一个无约束优化问题，即我们找出最小的$\theta$，使得cost function达到最小。而在无约束优化问题中，最重要最基本的方法莫过于梯度下降（Gradient Descent)了。  
描述梯度下降的资料很多，这里我选取wiki百科上的一部分内容：  

梯度下降法，基于这样的观察：如果实值函数$F(\mathbf{x})$在点$\mathbf{a}$处可微且有定义，那么函数$F(\mathbf{x})$在$\mathbf{a}$点沿着梯度相反的方向$ -\nabla F(\mathbf{a})$ 下降最快。  
因而，如果  
$\mathbf{b}=\mathbf{a}-\gamma\nabla F(\mathbf{a})$  
对于$\gamma>0$为一个够小数值时成立，那么$F(\mathbf{a})\geq F(\mathbf{b})$。  
考虑到这一点，我们可以从函数F的局部极小值的初始估计$\mathbf{x}_0$出发，并考虑如下序列$ \mathbf{x}_0$, $\mathbf{x}_1$, $\mathbf{x}_2$, $\dots$使得  

$\mathbf{x}_{n+1}=\mathbf{x}_n-\gamma_n \nabla F(\mathbf{x}_n),\ n \ge 0$。  
因此可得到  

$F(\mathbf{x}_0)\ge F(\mathbf{x}_1)\ge F(\mathbf{x}_2)\ge \cdots$,  
如果顺利的话序列$(\mathbf{x}_n)$收敛到期望的极值。注意每次迭代步长$\gamma$可以改变。  

同样是来自wiki的一张示意图，清楚地描述了梯度下降的过程：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/lr/4.png)  

## 2.对损失函数求导并得出迭代公式  
令单个样本的损失函数为：$$J(\theta)=cost(h_{\theta}(x),y) = -y_ilog(h_{\theta}(x)) - (1-y_i)log(1-h_{\theta}(x))$$，则：  
$$\begin{aligned}  
\frac{\partial}{\partial\theta}J(\theta_j) & = -\left( y{\frac{1}{g(\theta^Tx)} - (1-y)\frac{1}{1-g(\theta^Tx)}} \right) \frac{\partial}{\partial\theta_j} g(\theta^Tx) \\\\
& =  -\left( y{\frac{1}{g(\theta^Tx)} - (1-y)\frac{1}{1-g(\theta^Tx)}} \right) g(\theta^Tx) (1 - g(\theta^Tx)) \frac{\partial}{\partial\theta_j} \theta^Tx) \\\\
& = - \left( y(1-g(\theta^Tx)) - (1-y)g(\theta^Tx) \right) x_j \\\\
& = (h_\theta (x) - y)x_j
\end{aligned}$$  

注意从第一步到第二步，用到了 http://blog.csdn.net/bitcarmanlee/article/details/51165444  里对logistic函数求导的结论。  
  

如果对单个样本迭代，则表达式如下：  
$$\theta_j:=\theta_j - \alpha(h_\theta(x^i) - y^i)x_j ^i$$  
扩展到全体样本，表达式如下：  
$$\theta_j:=\theta_j - \sum_i ^m \alpha(h_\theta(x^i) - y^i)x_j ^i$$  

## 3.迭代公式向量化（vectorization)
根据第二部分我们得到的最终$\theta$相关的迭代公式为 ：  
$$\theta_j:=\theta_j - \sum_i ^m \alpha(h_\theta(x^i) - y^i)x_j ^i$$ 如果按照此公式操作的话，每计算一个$\theta$需要 循环m次。为此，我们需要将迭代公式进行向量化。  

首先我们将样本矩阵表示如下：  
$$ \mathbf{X} = 
\left [
\begin{matrix}
x^{(1)} \\\\
x^{(2)} \\\\
\cdots \\\\
x^{(m)}
\end{matrix} 
\right ] =
\left [
\begin{matrix}
x_0^{(1)} & x_1^{(1)} & \cdots & x_n^{(1)} \\\\
x_0^{(2)} & x_1^{(2)} & \cdots & x_n^{(2)} \\\\
\cdots & \cdots & \cdots &  \cdots  \\\\
x_0^{(m)} & x_1^{(m)} & \cdots & x_n^{(m)} 
\end{matrix} 
\right ] 
$$  

$$
\mathbf{y} = 
\left [
\begin{matrix}
y^{(1)} \\\\
y^{(2)} \\\\
\cdots \\\\
y^{(m)}
\end{matrix}
\right ]
$$  

将要求的$\theta$也表示成 矩阵的形式：  
$$
\mathbf{\theta} = 
\left [
\begin{matrix}
\theta_0 \\\\
\theta_1 \\\\
\cdots \\\\
\theta_n
\end{matrix}
\right ]
$$  

将$x\cdot\theta$的乘积记为A，有：  
$$
A = x\cdot\theta =
\left [
\begin{matrix}
x_0^{(1)} & x_1^{(1)} & \cdots & x_n^{(1)} \\\\
x_0^{(2)} & x_1^{(2)} & \cdots & x_n^{(2)} \\\\
\cdots & \cdots & \cdots &  \cdots  \\\\
x_0^{(m)} & x_1^{(m)} & \cdots & x_n^{(m)} 
\end{matrix} 
\right ] \cdot 
\left [
\begin{matrix}
\theta_0 \\\\
\theta_1 \\\\
\cdots \\\\
\theta_m
\end{matrix}
\right ] = 
\left [
\begin{matrix}
\theta_0x_0^{(1)} & \theta_1x_1^{(1)} & \cdots & \theta_nx_n^{(1)} \\\\
\theta_0x_0^{(2)} & \theta_1x_1^{(2)} & \cdots & \theta_nx_n^{(2)} \\\\
\cdots & \cdots & \cdots &  \cdots  \\\\
\theta_0x_0^{(m)} & \theta_1x_1^{(m)} & \cdots & \theta_nx_n^{(m)} 
\end{matrix} 
\right ] 
 $$  

将$h_{\theta}(x)-y$记为E:  
$$E=h_{\theta}(x)-y=
\left [
\begin{matrix}
g(A^1) - y^1 \\\\
g(A^2)  - y^2\\\\
\cdots \\\\
g(A^m) -y^m
\end{matrix}
\right ] = 
\left [
\begin{matrix}
e^1 \\\\
e^2 \\\\
\cdots \\\\
e^m
\end{matrix}
\right ] = 
g(A) - y
$$  

由上面的式子可以看出，$g(A)$的参数是一个 m*1的矩阵，或者说是一个列向量。如果我们设计函数$g$的时候，支持传入一个列向量，并返回一个列向量，则$h_{\theta}(x)-y$可以一次计算得到结果。  

回到我们的迭代公式，令j=0  
$$ \begin{aligned}
\theta_0: &=\theta_0 - \sum_i ^m \alpha(h_\theta(x^i) - y^i)x_0 ^i  \\\\
& = \theta_0 - \alpha  \sum_i ^m e^{(i)} x_0^{(i)} \\\\
& = \theta_0 - \alpha \cdot(x_0^{(1)},x_0^{(2)},\cdots,x_0^{(n)})\cdot E
\end{aligned}$$  

对于$\theta_j$，同理：  
$$\theta_j := \theta_j -\alpha \cdot(x_j^{(1)},x_j^{(2)},\cdots,x_j^{(n)})\cdot E$$  

将其写成矩阵的表达式：  
$$
\left [
\begin{matrix}
\theta_0 \\\\
\theta_1 \\\\
\cdots \\\\
\theta_m
\end{matrix}
\right ] :=
\left [
\begin{matrix}
\theta_0 \\\\
\theta_1 \\\\
\cdots \\\\
\theta_m
\end{matrix}
\right ] - \alpha \cdot 
\left [
\begin{matrix}
x_0^{(1)} & x_0^{(2)} & \cdots & x_0^{(m)} \\\\
x_1^{(1)} & x_1^{(2)} & \cdots & x_1^{(m)} \\\\
\cdots & \cdots & \cdots &  \cdots  \\\\
x_n^{(1)} & x_n^{(2)} & \cdots & x_n^{(m)} 
\end{matrix} 
\right ] \cdot E = 
\theta-\alpha \cdot x^T \cdot E
$$  

所以最后的迭代公式为：$$\theta = \theta-\alpha \cdot x^T \cdot E$$  

## 4.几点需要注意的事项
1.x的矩阵表示方式里，上边的范围是m,表示样本的数量，下边的范围是n，表示每个样本变量的维度。整个样本矩阵的大小是m\*n。  
2.如何快速理解$\theta$的迭代公式？我自己总结的一个小技巧：  
$\theta$表示每一维特征的权重，所以它是n\*1的矩阵。$x^T$是n\*m，E是m\*1,这两个矩阵相乘，刚好得到一个n*1的矩阵，跟$\theta$的大小是相吻合的！  

## 5.批量梯度下降（Batch Gradient Descent）与随机梯度下降(Stochastic Gradient Descent SGD)
对于迭代公式$$\theta = \theta-\alpha \cdot x^T \cdot E$$ 最大的好处就是形式简单明了，直接将样本矩阵与残差矩阵带入迭代即可。而且这种方式是将所有的训练样本代入，最终所求得的解也是全局最优解，求解出来的参数将使损失函数最小。如果将所有样本矩阵带入进行计算，这就是所谓的批量梯度下降(BGD)。但在实际应用场景中，最大的问题就是样本矩阵可能非常大。比如大到放不进内存，比如大到进行一轮迭代需要的运算时间非常长，这个时候，批量梯度下降就不是那么好用了。这个时候，我们可以采用考虑随机梯度下降 (SGD)。  
BGD是一次训练带入所有样本，SGD则是每来一次样本进行一次计算：  
$$\theta_j:=\theta_j + \alpha(y^i - h_\theta(x^i))x_j ^i$$  
i表示是第i个样本，j表示样本第j个维度。  
SGD是通过每个样本来迭代更新。如果样本的数量很多，有可能才迭代了一小部分样本，就已经得到了$\theta$的解。所以SGD的收敛速度可能比BGD要快，而且运算量小。但是SGD的问题是每次迭代并不是全局最优解的方向，尤其是遇到噪声数据，影响会比较大。有的时候SGD在最优解附近会存在比较明显的锯齿震荡现象，即损失函数的值会在最优解附近上下震荡一段时间才最终收敛。  