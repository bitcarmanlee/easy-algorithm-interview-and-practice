在概率论中，一组独立同分布的随机变量$x_1,x_2,\cdots,x_n$出现的频率很高。独立同分布，independent and identically distributed ,一般缩写为i.i.d。在概率论中，如果随机变量具有相同的概率分布，并且随机变量之间相互独立，那么这组随机变量就满足独立同分布。本文特意为大家整理一下与一组独立同分布的随机变量$x_1,x_2,\cdots,x_n$相关的一些有意思的小问题。  

## 1.Case1
已知随机变量$x_1,x_2,\cdots,x_n$相互独立且同分布，方差为$\sigma^2$，$y = \frac{1}{n} \sum_1^nx_i$，求$Cov(x_1,y)$。  

解答过程：  
设$E(x_1)  = E(y) = k$ ，则有
$$  
\begin{aligned}
Cov(x_1,y) & =E(x_1y) - E(x_1)E(y) \\\\
& = E(x_1y) - k^2
\end{aligned}
$$  

$$
\begin{aligned}
E(x_1y) &  = \frac{1}{n}E(x_1^2+\sum_{i=2}^nx_1x_i)  \\\\
& =  \frac{1}{n}E(x^2) +  \frac{1}{n}\sum_{i=2}^nE(x_1x_i) \\\\
& =  \frac{\sigma^2 + k^2}{n} +  \frac{n-1}{n}k^2
\end{aligned}
$$  

将下面的式子带入，很容易得到：  
$$Cov(x_1,y) = \frac{\sigma^2}{n}$$  

## 2.Case2
已知随机变量$x_1,x_2,\cdots,x_n$相互独立且同分布，求$y=x_1+x_2+\cdots+x_n$的概率密度函数，均值，方差。  
解答过程：  
先看$n=2$的情况，此时$y=x_1+x_2$  
$$p(y) = P\{Y \le y\} = p\{x_1+x_2  \le y\} = \int \_{-\infty}^{+\infty}f(x)\int_{-\infty}^{y-x}f(z)dz$$  
则概率密度$p_2(y) = \int_{-\infty}^{+\infty}f(x)f(y-x)dy$  

对于$n=3$  
$$p_3(y)=\int_{-\infty}^{+\infty}p_2(x)f(y-x)dx=\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}f(z)f(x-z)dzf(y-x)dx$$  

以此类推，且统一变量字母，可得：  
$$p_n(y)=\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}\cdots\int_{-\infty}^{+\infty}f(x_1)f(x_2-x_1)f(x_3-x_2)\cdots f(x_{n-1}-x_{n-2})f(y-x_{n-1})dx_1dx_2\cdots dx_{n-1}$$    

均值很容易看出来是为$nEx_i$，下面看看求方差。  
$$
\begin{aligned}
D(y) & =E(y^2) - E^2(y) \\\\
& = E(x_1+x_2+\cdots+x_n)^2-(nEx)^2 \\\\
& = E(x_1^2+x_2^2+ \cdots+x_n^2+2\sum_{i=1}^n\sum_{j=1,j\ne i}^n x_ix_j)-(nEx)^2 \\\\
& = n(Ex)^2+nDx_i + n(n-1)(Ex)^2-n^2(Ex)^2 \\\\
& = nDx_i
\end{aligned}
$$  

如果稍微扩展一下,$y=c_1x_1+c_2x_2+\cdots+c_nx_n$，那么期望为$E(y) = \sum c_iE(x_i)$，求方差的方法与上面类似:  
$$
\begin{aligned}
D(y) & =E(y^2) - E(y)^2 \\\\
& = E(c_1x_1+c_2x_2+\cdots+x_n)^2-E^2(c_1x_1+c_2x_2+\cdots+x_n) \\\\
& = E(c_1^2x_1^2+c_2^2x_2^2+ \cdots+c_n^2x_n^2+2\sum_{i=1}^n\sum_{j=1,j\ne i}^n x_ix_j)-E^2(c_1x_1+c_2x_2+\cdots+x_n)\\\\
& = \sum_{i=1}^n c_i^2 (Ex_i)^2 + \sum_{i=1}^nc_i^2 Dx_i + 2\sum_{i=1}^n\sum_{j=1,j\ne i}^n x_ix_j) -E^2(c_1x_1+c_2x_2+\cdots+x_n)\\\\
&=\sum_{i=1}^nc_i^2Dx_i
\end{aligned}
$$