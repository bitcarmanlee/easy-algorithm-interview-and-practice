#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author: WangLei
#date: 2020/6/26

#下载mnist数据集
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf

#定义一些参数
learning_rate = 0.001
train_epochs = 20
batch_size = 64

#定义3层感知机的神经单元个数
n_input = 784
n_hidden1 = 100
n_hidden2 = 100
n_classes = 10

#定义网络输入参数占位符
x = tf.placeholder(tf.float32, shape=[None, n_input])
y = tf.placeholder(tf.float32, shape=[None, n_classes])

#定义权重与偏置
weights = {'h1': tf.Variable(tf.random_normal([n_input, n_hidden1])),
                  'h2': tf.Variable(tf.random_normal([n_hidden1, n_hidden2])),
                  'out': tf.Variable(tf.random_normal([n_hidden2, n_classes]))}

biases = {'b1': tf.Variable(tf.random_normal([n_hidden1])),
                'b2': tf.Variable(tf.random_normal([n_hidden2])),
                'out': tf.Variable(tf.random_normal([n_classes]))}


#网络结构
def inference(input_x):
    layer_1 = tf.nn.relu(tf.matmul(input_x, weights['h1']) + biases['b1'])
    layer_2 = tf.nn.relu(tf.matmul(layer_1, weights['h2']) + biases['b2'])
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

#构建网络
logits = inference(x)
prediction = tf.nn.softmax(logits)

#loss与optimizer
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss)

# accuracy
pre_correct = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
accuracy = tf.reduce_mean(tf.cast(pre_correct, tf.float32))

#初始化所有变量
init = tf.global_variables_initializer()

#开始训练
with tf.Session() as sess:
    sess.run(init)
    total_batch = int(mnist.train.num_examples / batch_size)

    for epoch in range(train_epochs):
        for batch in range(total_batch):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            sess.run(train_op, feed_dict={x:batch_x, y:batch_y})
            if epoch == 10 and batch == 1:
                print(batch_x)
                print(batch_y)
                print(type(batch_x))
                print(type(batch_y))

        loss_, acc = sess.run([loss, accuracy], feed_dict={x:batch_x, y:batch_y})
        print("epoch {},  loss {:.4f}, acc {:.3f}".format(epoch, loss_, acc))

    print("optimizer finished!")

    #计算测试集的准确度
    test_acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels})
    print('test accuracy', test_acc)
