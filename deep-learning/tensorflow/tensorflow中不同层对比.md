## 1.各种层
1.tf.nn：最底层的函数，其他各种库可以说都是基于这个底层库来进行扩展的。  
2.tf.layers：比tf.nn更高级的库，对tf.nn进行了多方位功能的扩展。用程序员的话来说，就是用tf.nn造的轮子。最大的特点就是库中每个函数都有相应的类（函数名为大写,看了下底层源码，是从kears那迁移过来的）。  
3.tf.keras：如果说tf.layers是轮子，那么keras可以说是汽车。tf.keras是基于tf.layers和tf.nn的高度封装。  
4.tf.contrib.layers:tf.contrib.layers提供够将计算图中的  网络层、正则化、摘要操作、是构建计算图的高级操作，但是tf.contrib包含不稳定和实验代码，有可能以后API会改变。
