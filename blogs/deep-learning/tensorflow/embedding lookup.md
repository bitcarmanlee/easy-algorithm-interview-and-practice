## 1.embedding
embedding现在在推荐系统、ctr预估系统中的使用无处不在。简单来理解就是，对于各种高维稀疏的特征，工作将单个特征映射成为一个低维稠密向量，将高维稀疏特征由"精确匹配"变成一个在embedding向量上的"模糊匹配"，从而提高了算法的性能，将高维稀疏特征的可用性大大提高。  

## 2.lookup
embedding lookup本质上是用矩阵的乘法来实现的，可以将其看成一个特殊的"全连接层"。  
假设embedding矩阵为一个[feature_size, embed_size]的稠密矩阵W，其中feature_size大小为n, embed_size大小为m。tensorflow中的embedding_lookup(W, id)接口，可以想象一下，一个one_hot向量，大小为[1, feature_size]，其中只有一位id1为1，其他位均为0。这个向量与W矩阵相乘，结果是为一个[1, embed_size]的向量，他就是原始的one_hot向量对应的embedding向量，实际上就是W矩阵中对应的id1行。  

## 3.实际代码
lookup实际上就相当于下面的过程。  

```
def demo():
    matrix = np.random.random([1024, 10])
    print matrix.shape
    ids = np.array([0, 10, 10, 1000])
    print matrix[ids]
```  
最后代码的输出为:  

```
(1024, 10)
[[0.33932276 0.62978868 0.7680067  0.25169595 0.11889698 0.73487671
  0.39302831 0.71313575 0.95295298 0.06929405]
 [0.74972394 0.08380492 0.08302023 0.2560098  0.16114254 0.77196436
  0.8019449  0.36280887 0.2578033  0.95712909]
 [0.74972394 0.08380492 0.08302023 0.2560098  0.16114254 0.77196436
  0.8019449  0.36280887 0.2578033  0.95712909]
 [0.68516928 0.32181592 0.3170977  0.67795956 0.78001478 0.87844269
  0.09535475 0.54031062 0.80873737 0.21879871]]
```  


tensorflow中的用法:  

```
def demo():
    # 输入ids
    input_ids = tf.placeholder(dtype=tf.int32, shape=[None])

    # 已知变量的embedding
    embedding = np.asarray([[0.1, 0.2, 0.3], [1.1, 1.2, 1.3], [2.1, 2.2, 2.3], [3.1, 3.2, 3.3], [4.1, 4.2, 4.3]])

    # 根据input_ids中的id，查找embedding中对应的元素
    input_embedding = tf.nn.embedding_lookup(embedding, input_ids)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print sess.run(input_embedding, feed_dict={input_ids: [2]})
```  
最后的输出为:  

```
[[2.1 2.2 2.3]]
```  
