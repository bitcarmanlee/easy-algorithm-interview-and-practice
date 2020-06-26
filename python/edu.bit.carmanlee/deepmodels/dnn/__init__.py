#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author: WangLei
#date: 2020/6/24

import os
from six.moves.urllib.request import urlopen

import pandas as pd
import tensorflow as tf


# Data sets
IRIS_TRAINING = "data/iris_training.csv"
IRIS_TRAINING_URL = "http://download.tensorflow.org/data/iris_training.csv"

IRIS_TEST = "data/iris_test.csv"
IRIS_TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

if not os.path.exists(IRIS_TRAINING):
    raw = urlopen(IRIS_TRAINING_URL).read()
    with open(IRIS_TRAINING, 'wb') as f:
        f.write(raw)


if not os.path.exists(IRIS_TEST):
    raw = urlopen(IRIS_TEST_URL).read()
    with open(IRIS_TEST, 'wb') as f:
        f.write(raw)

FEATURES = ['SepalLength', 'SepalWidth','PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']

train = pd.read_csv(IRIS_TRAINING, names=FEATURES, header=0)
train_x = train[['SepalLength', 'SepalWidth','PetalLength', 'PetalWidth']]
train_y = train['Species']
del train

test = pd.read_csv(IRIS_TEST, names=FEATURES, header=0)
test_x = test[['SepalLength', 'SepalWidth','PetalLength', 'PetalWidth']]
test_y = test['Species']
del test

feature_columns = []
for key in train_x.keys():
    feature_columns.append(tf.feature_column.numeric_column(key=key))

classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units = [10, 10],
    n_classes=3
)


def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()

batch_size = 100
classifier.train(input_fn=lambda :train_input_fn(train_x, train_y, batch_size),steps=1000)


def eval_input_fn(features, labels, batch_size):
    features = dict(features)
    inputs = (features, labels)
    dataset = tf.data.Dataset.from_tensor_slices(inputs)
    dataset = dataset.batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()

eval_result = classifier.evaluate(
    input_fn = lambda :eval_input_fn(test_x, test_y, batch_size))

print(eval_result)







