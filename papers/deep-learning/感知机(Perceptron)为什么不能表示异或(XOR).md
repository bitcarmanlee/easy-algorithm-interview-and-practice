## 1.感知机不能表示异或
在很早之前学Pattern Recognition相关课程的时候，老师在课堂上就说过感知机遇到的一个大问题就是无法表示异或问题(XOR）。后来接触深度学习相关的内容，开头部分肯定会提到感知机，提到感知机也必会提到不能表示异或的问题。正好抽出点时间，稍微搞明白一下为什么感知机不能表示异或。  

## 2.感知机的数学定义
感知机到底是什么呢？首先来看一下他的数学定义：  
假设输入空间(即样本的特征空间)为$X \subseteq R ^ n$，输出空间为$y = \{+1, -1\}$。输入位$x \subset X$表示样本的特征向量，对应于输入空间(特征空间)的点；输出$y \subset Y$表示样本类别。由输入空间到输出空间对应的函数关系如下：  
$$f(x) = sign(w\cdot x) + b$$  

此函数被称为感知机。其中，$w$与$b$为感知机的模型参数，$w \subset R^n$为权重(weight)或权值向量(weight vector)，$b \subset R$为偏置(bias)，$w \cdot x$表示$w$与$x$的内积，而$sign$是符合函数，即：  
$$\begin{equation}
sign(x) = 
  \left\{
   \begin{aligned}
  +1, x \geq0 \\
  -1,x \leq 0 \\
   \end{aligned}
   \right.
  \end{equation}$$  
  
  
感知机是一种线性分类模型，属于判别模型。

## 3.异或是线性不可分
异或之所以重要，是因为它相对于其他逻辑关系，例如与（AND）, 或（OR）等，异或是线性不可分的。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/deep-learning/ganzhiji/1.jpeg)  

由这幅简单的示意图可以看出来，and(与)、or(或)、not and(与非)等运算很容易用一条直线分开，但是异或运算中，图示的1,2,3条虚线都无法分开，异或运算就是典型的非线性问题！  

具体的数学证明过程可以看后面的参考内容  

## 参考文献：
1.https://zh.wikipedia.org/wiki/%E6%84%9F%E7%9F%A5%E5%99%A8  
2.https://www.zybuluo.com/ArrowLLL/note/827264 有数学证明过程  
3.https://zhuanlan.zhihu.com/p/30155870  