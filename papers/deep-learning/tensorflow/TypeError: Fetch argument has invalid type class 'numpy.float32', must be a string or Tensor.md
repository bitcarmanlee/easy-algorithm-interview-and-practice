## 1.问题
tensorflow代码在运行的时候，出现如下错误  

```
Epoch: 0010 cost= 0.080483146 W= 0.23614137 b= 0.97142047
...
TypeError: Fetch argument 0.080483146 has invalid type <class 'numpy.float32'>, must be a string or Tensor. (Can not convert a float32 into a Tensor or Operation.)

```  

对应部分的代码如下  

```
	...
    loss = tf.reduce_sum(tf.pow(pred-Y, 2) / (2*n_samples))
    # optmize
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        for epoch in range(training_epochs):
            for (x, y) in zip(train_X, train_Y):
                sess.run(optimizer, feed_dict={
                    X: x, Y: y
                })

            if (epoch+1) % display_step == 0:
                loss = sess.run(loss, feed_dict={X: train_X, Y:train_Y})
                print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(loss), "W=", sess.run(W), "b=", sess.run(b))
	...
```  

## 2.原因分析  
很明显是loss函数那边出了问题。第一次loss有正常输出，而后面loss则有异常，原因是Fetch需要的参数为一个Tensor或者String，但是现在传过来的确实个float32。  

再查看一下  

```
    loss = tf.reduce_sum(tf.pow(pred-Y, 2) / (2*n_samples))

```  
第一轮迭代的时候，这个loss是个Tensor。但是后面 run方法返回的，确实个float，所以会出现异常！  

## 3.解决方法  
因为是loss的异常引起的，所以我们将run方法返回的loss重新命令，给个新变量即可。  

```
    loss = tf.reduce_sum(tf.pow(pred-Y, 2) / (2*n_samples))
    # optmize
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        for epoch in range(training_epochs):
            for (x, y) in zip(train_X, train_Y):
                sess.run(optimizer, feed_dict={
                    X: x, Y: y
                })

            if (epoch+1) % display_step == 0:
                newloss = sess.run(loss, feed_dict={X: train_X, Y:train_Y})
                print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(newloss), "W=", sess.run(W), "b=", sess.run(b))
```  

像上面这样，将run方法返回的值重新命名为newloss即可解决上述问题！  

