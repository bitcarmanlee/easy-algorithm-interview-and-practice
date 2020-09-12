## 0.前言
现在算法相关的框架与工具，封装得越来越好，调用越来越方便，以至于很多算法工程师被嘲笑或者自嘲为"调包侠"，"调参侠"。确实在实际工作中，需要自己从头到尾实现算法的机会越来越少，尤其是分布式的系统，最多就是在框架实现的基础之上拉出一部分逻辑进行二次开发重新封装一下。即便如此，弄清楚算法的原理与流程，也还是有必要的，这样更方便实际中debug，定位问题，调整参数等等。因此，本人打算基于tensorflow来实现一下各种常用的算法，包括深度学习的各种算法，网络结构，以及传统的机器学习算法。  

## 1.线性回归
线性回归算是最简单的一种数据模拟方式了，有过初中数学基础的同学都能理解。现在我们考虑一种最简单的情况：单变量的线性回归。  
假设  
$$y = 2x + 0.1$$  
有一组数据满足以上的解析关系，然后现在求解线性回归，求参数$w$与$b$。  

先看我们不使用tensorflow，只使用numpy求解的解法。  

```
import numpy as np

# simulate y = 2x + 0.1
def linear_reg_gd():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2.1, 4.1, 6.1, 8.1, 10.1])

    w = np.random.rand()
    b = np.random.rand()

    learning_rate = 0.02
    for i in range(3000):
        ww = np.array([w] * len(x))
        bb = np.array([b] * len(x))

        loss = np.linalg.norm(ww * x + bb - y, 2)

        if loss < 0.00001:
            break
        if i % 100 == 0:
            print("第 %d 次loss为: %f" % (i, loss))

        grad_w = np.sum((ww * x + bb - y) * x) / len(x)
        grad_b = np.sum(ww * x + bb - y) / len(x)

        w -= learning_rate * grad_w
        b -= learning_rate * grad_b

    print(w)
    print(b)
```  

上面的代码几个关键步骤：  

```
        loss = np.linalg.norm(ww * x + bb - y, 2)
```  
本行定义了损失函数，为MSE。  

```
        grad_w = np.sum((ww * x + bb - y) * x) / len(x)
        grad_b = np.sum(ww * x + bb - y) / len(x)

```  

分别计算$w$与$b$的梯度，然后进行迭代梯度下降即可。  

## 2.tensorflow进行线性回归

```
import numpy as np
import tensorflow as tf

def linear_reg_tf():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.1, 4.1, 6.1, 8.1, 10.1])

    n = x.shape[0]

    W = tf.Variable(np.random.rand())
    b = tf.Variable(np.random.rand())

    X = tf.placeholder(tf.float32, name='X')
    Y = tf.placeholder(tf.float32, name='Y')
	
	# model
    pred = tf.add(tf.multiply(X, W), b)

	# loss
    loss = tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * n)

	# optmize
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        for i in range(3000):
            l, _ = sess.run([loss, optimizer], feed_dict={X: x, Y: y})
            print("第 %d 次loss: %f" %(i, l))

            if l < 0.000001:
                break

        print("W is: ", W.eval())
        print("b is: ", b.eval())

linear_reg_tf()
```  

```
...
第 2998 次loss: 0.000004
第 2999 次loss: 0.000004
W is:  1.9981396
b is:  0.10671652
```  
首先看最终的结果，$w=1.998, b = 0.1067$，已经比较接近准确的数值了。  

代码结构：  
1.定义W, b变量。  
2.声名X, Y的placeholder。  
3.pred为模型，其实就是$y = wx + b$  
4.loss为MSE损失函数  
5.optimizer为优化器，这里选的是梯度下降。  
6.然后起个sess开始run即可。  

可以看出，tf的代码结构还是比较简单清晰的，实现起来确实也比较快。  