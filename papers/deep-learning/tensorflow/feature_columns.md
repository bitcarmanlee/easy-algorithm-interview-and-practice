## 1 tensorflow中的特征工程
传统的机器学习中，特征工程占有非常重要的地位。与其说算法工程师是在做算法，不如说是做数据，做特征。通常花费60%-70%的时间做特征工程也是很常见。由此可见特征工程的重要性与复杂性。  
深度学习的崛起，很大程度上是减少了特征工程的工作量，可以让网络自己去学习各种特征之间的组合，即所谓的端到端(end to end)学习。    
即便如此，特征工程仍然是深度学习算法中的重要一环，前期数据的预处理质量仍然很大程度决定了算法的最终效果。  

tensorflow中提供了feature columns的相关API。feature columns是输入特征数据与estimator(真正的算法模型)之间沟通的桥梁。  
因为深度神经网络只能处理数值类的数据，算法的核心步骤是前向的加法模型与梯度的反向传播，这里面其实就是数值的加法与乘法运算。但在实际中，除了连续的数值变量，更多的是非数值的类别特征，比如性别，地域这种。  
因此，feature column可以将特征作为单个语义单元来操作,指定转换并选择要包括的特征，然后就可以直接喂给模型，而不需要人工再进行复杂的转换与运算。  

## 2.数值类特征转换
### 2.1  numeric_column
numeric_column主要处理连续型变量，可以是float也可以是int，从table中读取对应的key，并将其转成相应的dtype。  

```
import numpy as np
import tensorflow as tf

def t1():
    features = {"price": [1.5, 1.3, 2.1, 2.5, 0.6, 3.1, 3.2]}
    price = tf.feature_column.numeric_column("price", default_value=2.5)
    columns = [price]

    # 输入层(数据列，特征列)
    input_layer = tf.feature_column.input_layer(features, columns)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(input_layer)
        print(result)
        print(type(result))

```

最终结果为  
```
[[1.5]
 [1.3]
 [2.1]
 [2.5]
 [0.6]
 [3.1]
 [3.2]]
<class 'numpy.ndarray'>
```

### 2.2 bucketized_column
bucketized_column也是用来处理连续变量类型。与numeric_column不同的是，其会将特征bucketized(分桶)离散化，最后得到的是离散化以后的one-hot结果。  
```
'''
[-inf, 0), [0, 1), [1, 2), [2, 3), [3, +inf)
'''
def t2():
    features = {"price": [1.5, 1.3, 2.1, 2.5, 0.6, 3.1, 3.2]}
    step = 1.0
    boundaries = list(np.arange(0, 4, step))
    price = tf.feature_column.bucketized_column(tf.feature_column.numeric_column("price", default_value=2.5),
                                                boundaries=boundaries)
    columns = [price]
    input_layer = tf.feature_column.input_layer(features, columns)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(input_layer)
        print(result)
```  
最终结果为  
```
[[0. 0. 1. 0. 0.]
 [0. 0. 1. 0. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]
 [0. 1. 0. 0. 0.]
 [0. 0. 0. 0. 1.]
 [0. 0. 0. 0. 1.]]
```

上面的代码将数值空间分成了五个部分，所以最终one-hot出来的结果总共有5维。注意各区间是左闭右开。  


## 3.category类特征转换

### 3.1 categorical_column_with_identity
categorical_column_with_identity的作用就是对特征进行one-hot编码。  
```
def t1():
    features = {"category": [[1], [3], [1], [3], [2], [1]]}

    category = tf.feature_column.categorical_column_with_identity("category", num_buckets=4, default_value=0)
    category = tf.feature_column.indicator_column(category)

    columns = [category]

    input_layer = tf.feature_column.input_layer(features, columns)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(input_layer)
        print(result)
```  

最终结果为  
```
[[0. 1. 0. 0.]
 [0. 0. 0. 1.]
 [0. 1. 0. 0.]
 [0. 0. 0. 1.]
 [0. 0. 1. 0.]
 [0. 1. 0. 0.]]
```  
源码中的有相关注释  
```
@tf_export('feature_column.categorical_column_with_identity')
def categorical_column_with_identity(key, num_buckets, default_value=None):
  """A `CategoricalColumn` that returns identity values.

  Use this when your inputs are integers in the range `[0, num_buckets)`, and
  you want to use the input value itself as the categorical ID. Values outside
  this range will result in `default_value` if specified, otherwise it will
  fail.

  Typically, this is used for contiguous ranges of integer indexes, but
  it doesn't have to be. This might be inefficient, however, if many of IDs
  are unused. Consider `categorical_column_with_hash_bucket` in that case.

  For input dictionary `features`, `features[key]` is either `Tensor` or
  `SparseTensor`. If `Tensor`, missing values can be represented by `-1` for int
  and `''` for string, which will be dropped by this feature column.

```  
根据注释不难看出，该方法只适用于值为整数的类别变量，其中num_buckets为类别的总数。

### 3.2 categorical_column_with_vocabulary_list categorical_column_with_vocabulary_file

上面的两个方法是根据单词出现的序列顺序，将其进行one-hot编码。  
如果对应的类别比较少，可以一一列举出来，则可以使用vocabulary_list方法。  
如果对应的类别比较多，无法一一列举而需要从文件中输入，则可以使用vocabulary_file。  


```
def t2():
    features = {'sex': ['male', 'male', 'female', 'female']}
    sex_column = tf.feature_column.categorical_column_with_vocabulary_list('sex', ['male', 'female'])
    sex_column = tf.feature_column.indicator_column(sex_column)

    columns = [sex_column]

    input_layer = tf.feature_column.input_layer(features, columns)
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(input_layer)
        print(result)
```  
最终的结果为  
```
[[1. 0.]
 [1. 0.]
 [0. 1.]
 [0. 1.]]
```

### 3.3 categorical_column_with_hash_bucket
顾名思义，该方法对特征的处理方式为hash分桶。因为是hash算法，所以就有可能存在冲突。  
```
def t3():
    features = {'department': ['sport', 'sport', 'drawing', 'gardening', 'travelling']}
    department = tf.feature_column.categorical_column_with_hash_bucket('department', 4, dtype=tf.string)
    department = tf.feature_column.indicator_column(department)

    columns = [department]

    input_layer = tf.feature_column.input_layer(features, columns)
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(input_layer)
        print(result)
```  
最终输出结果为  
```
[[0. 1. 0. 0.]
 [0. 1. 0. 0.]
 [0. 1. 0. 0.]
 [1. 0. 0. 0.]

```

### 3.4 crossed_column
crossed_column是用来处理交叉特征的。传统机器学习方法中，我们经常人工设计各种交叉特征，比如最常见的将年龄与性别交叉，得到一维新的特征。  

```
def t4():
    features = {
        'sex': [1, 2, 1, 1, 2],
        'department': ['sport', 'sport', 'drawing', 'gardening', 'travelling'],
    }

    # 特征列
    department = tf.feature_column.categorical_column_with_vocabulary_list('department',
                                                                           ['sport', 'drawing', 'gardening',
                                                                            'travelling'], dtype=tf.string)
    sex = tf.feature_column.categorical_column_with_identity('sex', num_buckets=2, default_value=0)
    sex_department = tf.feature_column.crossed_column([department, sex], 16)
    sex_department = tf.feature_column.indicator_column(sex_department)
    # 组合特征列
    columns = [sex_department]
    input_layer = tf.feature_column.input_layer(features, columns)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(input_layer)
        print(type(result))
        print(result)
```  

最终输出结果为  
```
<class 'numpy.ndarray'>
[[0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]]

```

### 3.5 embedding_column
对高维稀疏类别特征进行低维稠密压缩，是深度学习中各算法的标配。embedding_column就是用来处理embedding的。  

```
def t5():
    color_data = {'color': [['R'], ['G'], ['B'], ['A']]}
    color = tf.feature_column.categorical_column_with_vocabulary_list(
        'color', ['R', 'G', 'B'], dtype=tf.string, default_value=-1)

    color_embeding = tf.feature_column.embedding_column(color, 8)
    color_embeding_dense_tensor = tf.feature_column.input_layer(color_data, color_embeding)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(tf.tables_initializer())
        sess.run(init)

        result = sess.run(color_embeding_dense_tensor)
        print(result)
```  

最终输出的结果为  
```
[[ 0.06087255  0.14802316 -0.53089684  0.3792207  -0.07220224  0.11126718
   0.13428093  0.05913785]
 [ 0.11378041  0.09111454  0.13312939  0.4688532   0.16119204 -0.00828113
  -0.07480547 -0.19241782]
 [-0.505195    0.14229129  0.17853943 -0.05520723 -0.19731279 -0.28580233
  -0.16668914 -0.68252677]
 [ 0.          0.          0.          0.          0.          0.
   0.          0.        ]]
```

简单看一下embedding_column的源码  
```
@tf_export('feature_column.embedding_column')
def embedding_column(categorical_column,
                     dimension,
                     combiner='mean',
                     initializer=None,
                     ckpt_to_load_from=None,
                     tensor_name_in_ckpt=None,
                     max_norm=None,
                     trainable=True):
  """`DenseColumn` that converts from sparse, categorical input.

  Use this when your inputs are sparse, but you want to convert them to a dense
  representation (e.g., to feed to a DNN).

  Inputs must be a `CategoricalColumn` created by any of the
  `categorical_column_*` function. Here is an example of using
  `embedding_column` with `DNNClassifier`:
    ...
  Args:
    categorical_column: A `CategoricalColumn` created by a
      `categorical_column_with_*` function. This column produces the sparse IDs
      that are inputs to the embedding lookup.
    dimension: An integer specifying dimension of the embedding, must be > 0.
    combiner: A string specifying how to reduce if there are multiple entries in
      a single row. Currently 'mean', 'sqrtn' and 'sum' are supported, with
      'mean' the default. 'sqrtn' often achieves good accuracy, in particular
      with bag-of-words columns. Each of this can be thought as example level
      normalizations on the column. For more information, see
      `tf.embedding_lookup_sparse`.
    initializer: A variable initializer function to be used in embedding
      variable initialization. If not specified, defaults to
      `tf.truncated_normal_initializer` with mean `0.0` and standard deviation
      `1/sqrt(dimension)`.
    ckpt_to_load_from: String representing checkpoint name/pattern from which to
      restore column weights. Required if `tensor_name_in_ckpt` is not `None`.
    tensor_name_in_ckpt: Name of the `Tensor` in `ckpt_to_load_from` from which
      to restore the column weights. Required if `ckpt_to_load_from` is not
      `None`.
    max_norm: If not `None`, embedding values are l2-normalized to this value.
    trainable: Whether or not the embedding is trainable. Default is True.

  Returns:
    `DenseColumn` that converts from sparse input.
```  

重点关注一下两个参数：  
1.combiner。当一行有多个entries时，可以使用'mean', 'sqrtn', 'sum'的方式来对向量进行处理，默认的方法是mean。  
2.initializer 初始化embedding向量的方法，默认的是用`tf.truncated_normal_initializer`方法，均值为0.0，方差为`1/sqrt(dimension)`。