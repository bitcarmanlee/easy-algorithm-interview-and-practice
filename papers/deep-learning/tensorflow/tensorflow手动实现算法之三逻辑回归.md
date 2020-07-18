## 1.逻辑回归算法
逻辑回归是日常工作中最常用的算法之一。虽然逻辑回归很简单，出现的年代也比较久远，但是实现简单，可解释性强，一般效果也不会太差，尤其在处理海量数据集的时候具有性能上的巨大优势，因此逻辑回归一般会被用作线上算法的baseline版本之一。  

之前逻辑回归系列文章  
[为什么要使用logistic函数](https://blog.csdn.net/bitcarmanlee/article/details/51154481)  
[损失函数（cost function）详解](https://blog.csdn.net/bitcarmanlee/article/details/51165444)  
[梯度下降训练方法](https://blog.csdn.net/bitcarmanlee/article/details/51473567)  


## 2.tensorflow实现  
有了上面的理论基础以后，基于tensorflow我们来实现一把逻辑回归，采用的数据集为mnist。  

```
import tensorflow as tf


def logistic_regression():
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets("data/", one_hot=True)

    # tf graph input
    X = tf.placeholder(tf.float32, [None, 784]) # mnist data image of shape 28*28=784
    Y = tf.placeholder(tf.float32, [None, 10])

    # Weights
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    # model
    pred = tf.nn.softmax(tf.matmul(X, W) + b)

    # loss: 交叉熵损失函数
    loss = tf.reduce_mean(- tf.reduce_sum(Y * tf.log(pred), reduction_indices=1))

    # opt: 梯度下降
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.02).minimize(loss)

    init = tf.global_variables_initializer()

    batch_size = 100

    with tf.Session() as sess:
        sess.run(init)

        for epoch in range(50):
            avg_loss = 0.0
            total_batch = int(mnist.train.num_examples / batch_size)
            for i in range(total_batch):
                batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                _, l = sess.run([optimizer, loss], feed_dict={X: batch_xs, Y: batch_ys})
                avg_loss += l / total_batch

            print("epoch %d loss is: %f" %(epoch, avg_loss))

        print('\n\n')
        print("W is: ", W.eval()[300:320, :])
        print("b is: ", b.eval())
        print("W shape is: ", W.eval().shape)
        print("b shape is: ", b.eval().shape)

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))

        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        print("Accuracy: ", accuracy.eval({X: mnist.test.images, Y: mnist.test.labels}))


logistic_regression()
```  

输出：  

```
epoch 0 loss is: 0.925885
epoch 1 loss is: 0.526170
epoch 2 loss is: 0.454383
epoch 3 loss is: 0.419288
epoch 4 loss is: 0.397402
epoch 5 loss is: 0.381946
epoch 6 loss is: 0.370278
epoch 7 loss is: 0.361055
epoch 8 loss is: 0.353631
epoch 9 loss is: 0.347324
epoch 10 loss is: 0.341956
epoch 11 loss is: 0.337216
epoch 12 loss is: 0.333048
epoch 13 loss is: 0.329546
epoch 14 loss is: 0.326188
epoch 15 loss is: 0.323263
epoch 16 loss is: 0.320566
epoch 17 loss is: 0.318108
epoch 18 loss is: 0.315884
epoch 19 loss is: 0.313779
epoch 20 loss is: 0.311729
epoch 21 loss is: 0.309981
epoch 22 loss is: 0.308338
epoch 23 loss is: 0.306725
epoch 24 loss is: 0.305222
epoch 25 loss is: 0.303862
epoch 26 loss is: 0.302433
epoch 27 loss is: 0.301285
epoch 28 loss is: 0.300108
epoch 29 loss is: 0.298947
epoch 30 loss is: 0.297839
epoch 31 loss is: 0.296805
epoch 32 loss is: 0.295821
epoch 33 loss is: 0.294917
epoch 34 loss is: 0.293935
epoch 35 loss is: 0.293092
epoch 36 loss is: 0.292298
epoch 37 loss is: 0.291464
epoch 38 loss is: 0.290767
epoch 39 loss is: 0.289950
epoch 40 loss is: 0.289225
epoch 41 loss is: 0.288532
epoch 42 loss is: 0.287839
epoch 43 loss is: 0.287262
epoch 44 loss is: 0.286554
epoch 45 loss is: 0.285947
epoch 46 loss is: 0.285375
epoch 47 loss is: 0.284844
epoch 48 loss is: 0.284207
epoch 49 loss is: 0.283784



W is:  [[ 1.30058274e-01 -2.43340924e-01 -2.88325530e-02  2.33772218e-01
  -9.86490175e-02 -9.76923853e-02 -2.35121310e-01  2.35980958e-01
   5.27126603e-02  5.11115305e-02]
 [ 9.32730213e-02 -2.27573335e-01 -4.64867800e-02  1.07791178e-01
  -9.04569626e-02 -7.11493136e-04 -1.82566136e-01  2.22163513e-01
   1.07116044e-01  1.74529087e-02]
 [ 1.88447177e-01 -2.02589765e-01 -4.72486354e-02 -3.71847395e-03
  -1.13012344e-01  7.77632222e-02 -1.59778014e-01  1.04445107e-01
   1.82390571e-01 -2.66976375e-02]
 [ 2.84826338e-01 -1.67852297e-01 -9.68634710e-02 -8.53038132e-02
  -1.96322858e-01  3.31335187e-01 -8.84726346e-02 -7.75983706e-02
   1.82672381e-01 -8.64163712e-02]
 [ 1.11412644e-01 -1.11834183e-01 -9.90691558e-02 -7.97616988e-02
  -1.61673650e-01  6.03716910e-01 -1.09354012e-01 -7.34354481e-02
   3.73539254e-02 -1.17341466e-01]
 [-8.59155580e-02 -3.89751643e-02 -2.86357161e-02 -1.60242077e-02
  -9.84951109e-02  4.94616568e-01 -1.11441180e-01 -2.78114546e-02
  -3.23890485e-02 -5.49230687e-02]
 [-3.36165093e-02 -8.39466415e-03 -1.98007881e-04 -2.61049788e-03
  -2.68098358e-02  1.26275659e-01 -3.57160829e-02 -5.30548953e-03
   3.29373917e-03 -1.69179160e-02]
 [-4.63828037e-04  3.53039541e-05 -3.86474276e-04 -6.74947805e-05
  -7.93245155e-04  4.53931652e-03 -5.11363195e-03  9.23962216e-04
   3.78094311e-03 -2.45485152e-03]
 [-2.32933871e-05 -5.23060453e-06 -1.34871498e-05 -5.77266692e-05
  -6.71111120e-05 -4.80900053e-05 -9.40263817e-06  7.19755713e-04
  -2.79757987e-05 -4.67438367e-04]
 [ 8.65108101e-04  9.09597729e-05 -3.11443349e-04 -1.47864106e-03
  -6.83900435e-03 -2.77064624e-03 -3.86913482e-04  2.58669052e-02
  -8.54679325e-04 -1.41816465e-02]
 [-2.63929088e-03 -2.64492322e-04 -1.53854780e-03  4.31185850e-04
  -3.15029547e-02 -7.15911528e-03 -1.23515935e-03  9.76308361e-02
  -5.08135464e-03 -4.86406647e-02]
 [-1.19008878e-02 -5.28532686e-03 -5.90232015e-03  4.48378287e-02
  -3.87149863e-02 -3.90309207e-02 -2.01594979e-02  1.49421439e-01
  -1.14256218e-02 -6.18363917e-02]
 [-6.87927529e-02 -8.77870712e-03 -4.94896695e-02  2.03535855e-02
  -7.20102340e-02 -3.36355865e-02 -3.02698240e-02  2.09295705e-01
   3.57626490e-02 -2.43041757e-03]
 [-6.52488619e-02 -3.42066772e-02 -1.01321273e-01 -1.07673272e-01
  -6.53655455e-02  4.46031569e-03 -2.43143365e-02  1.28288701e-01
   1.22475803e-01  1.42906830e-01]
 [-1.80723500e-02 -8.89688134e-02 -2.10183084e-01 -2.18472376e-01
  -2.55523417e-02  1.34961814e-01 -6.41731219e-03  5.13334572e-02
   1.82656676e-01  1.98715582e-01]
 [ 8.76079965e-03 -1.15071632e-01 -3.15628499e-01 -3.39576840e-01
   3.33518460e-02  1.49892882e-01  8.10965970e-02  6.31594658e-02
   2.69269615e-01  1.64745867e-01]
 [-8.59805103e-03 -1.37789100e-01 -3.33113641e-01 -3.76729548e-01
   1.30424783e-01  1.63710088e-01  4.69603762e-02 -8.52634199e-03
   2.47313410e-01  2.76347369e-01]
 [-5.59019931e-02 -1.81571841e-01 -3.58628988e-01 -3.46353084e-01
   2.19564497e-01  1.55591249e-01  5.56244776e-02  8.47302899e-02
   2.68048823e-01  1.58896521e-01]
 [-4.31540869e-02 -1.74465016e-01 -4.56743926e-01 -2.85489947e-01
   2.57946610e-01  1.54958680e-01  4.15352397e-02  1.08570904e-01
   1.84646279e-01  2.12190300e-01]
 [-2.23886557e-02 -1.72276974e-01 -4.75257486e-01 -2.02534094e-01
   2.45876372e-01  2.05934808e-01  9.71724372e-03  7.21609220e-02
   1.30991027e-01  2.07777485e-01]]
b is:  [-0.3816464   0.36356112  0.0971376  -0.27018493  0.00226471  1.328009
 -0.104314    0.64620227 -1.4425566  -0.23847117]
W shape is:  (784, 10)
b shape is:  (10,)
Accuracy:  0.9217
```  

## 3.算法分析  
### 3.1 数据集  
为了方便分析算法，先写个简单的方法看看数据都长啥样  

```
def read_data():
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets("data/", one_hot=True)

    print(mnist.train.images[0:10])
    print(mnist.train.labels[0:10])
    print(mnist.train.images.shape)
    print(mnist.train.labels.shape)

read_data()
```  

输出为  

```
[[0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 ...
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]]
[[0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]
 [0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]
 [0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
 [0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]]
(55000, 784)
(55000, 10)
```  

train包含55000个样本，每个样本一共有28*28=784维，所以mnist.train.images是个55000 * 784的矩阵。  
每个图片是0-9之间的一个数字，所以总类别是10，one-hot完以后就是个10维向量，只有一维为1，其余九维为0，为1的那一维对应的index就表示是数字几。train.label是个55000 * 784的矩阵。  


## 3.2 参数
W: 维度为784 * 10。  
b: 维度为(10,)  
`pred = tf.nn.softmax(tf.matmul(X, W) + b)`表示用softmax进行预测分类结果，`tf.matmul(X, W)`的结果为55000 * 10维，与b相加的时候，b会进行广播保证与其维度一致。  

## 3.3交叉熵损失函数  
重点看看loss函数  

`loss = tf.reduce_mean(- tf.reduce_sum(Y * tf.log(pred), reduction_indices=1))`  

`Y * tf.log(pred)`是交叉熵的定义，Y的维度为55000 * 10， pred的维度也为55000 * 10，这一步的结果为55000 * 10。  
 
 
`- tf.reduce_sum(Y * tf.log(pred), reduction_indices=1)`表示在`reduction_indices=1`的轴上求和。如果将reduction_indices类比成axis参数，这个操作表示要消灭的是内层的维度，即将55000 * 10的矩阵变成55000的数组，相当于对每行求和。  

`tf.reduce_mean`则是求loss的平均值了。  

## 4.优化求解
后面的步骤就都是优化求解了  

## 5.预测
`correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))`  
`tf.argmax(pred, 1)`表示预测值中概率最高的index，就是预测数字为几。  
`tf.argmax(Y, 1))`表示真实值中为1的index(因为别的位置都为0，为1的那个index就是最大值)。  
`tf.equal`会将其变成一个boolean数组  

`accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))`  
就是算最终的准确率了。  

