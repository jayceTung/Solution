# -*- coding: utf-8 -*-

# @Author  : super
# @Time    : 2018/1/23
# @desc    :

import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def make_layer(inputs, in_size, out_size, activate=None):
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    basis = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    result = tf.matmul(inputs, weights) + basis
    if activate is None:
        return result
    else:
        return activate(result)


class BPNeuralNetwork:
    def __init__(self):
        self.session = tf.Session()
        self.loss = None
        self.optimizer = None
        self.input_n = 0
        self.hidden_n = 0
        self.hidden_size = []
        self.output_n = 0
        self.input_layer = None
        self.hidden_layers = []
        self.output_layer = None
        self.label_layer = None

    def __del__(self):
        self.session.close()

    def setup(self, ni, nh, no):
        # 设置参数个数
        self.input_n = ni
        self.hidden_n = len(nh)  #隐藏层的数量
        self.hidden_size = nh  #每个隐藏层中的单元格数
        self.output_n = no
        #构建输入层
        self.input_layer = tf.placeholder(tf.float32, [None, self.input_n])
        #构建标签层
        self.label_layer = tf.placeholder(tf.float32, [None, self.output_n])
        #构建隐藏层
        in_size = self.input_n
        out_size = self.hidden_size[0]
        inputs = self.input_layer
        self.hidden_layers.append(make_layer(inputs, in_size, out_size, activate=tf.nn.relu))
        for i in range(self.hidden_n-1):
            in_size = out_size
            out_size = self.hidden_size[i+1]
            inputs = self.hidden_layers[-1]
            self.hidden_layers.append(make_layer(inputs, in_size, out_size, activate=tf.nn.relu))
        #构建输出层
        self.output_layer = make_layer(self.hidden_layers[-1], self.hidden_size[-1], self.output_n)

    def train(self, cases, labels, limit=100, learn_rate=0.05):
        self.loss = tf.reduce_mean(tf.reduce_sum(tf.square((self.label_layer - self.output_layer)), reduction_indices=[1]))
        self.optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(self.loss)
        initer = tf.initialize_all_variables()
        #做训练
        self.session.run(initer)
        for i in range(limit):
            self.session.run(self.optimizer, feed_dict={self.input_layer: cases, self.label_layer: labels})

    def predict(self, case):
        return self.session.run(self.output_layer, feed_dict={self.input_layer: case})

    def test(self):
        x_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y_data = np.array([[0, 1, 1, 0]]).transpose()
        test_data = np.array([[0, 1]])
        self.setup(2, [10, 5], 1)
        self.train(x_data, y_data)
        print(self.predict(test_data))

if __name__ == '__main__':
    # nn = BPNeuralNetwork()
    # nn.test()
    hello = tf.constant('Hello, TensorFlow')
    sess = tf.Session()
    print(sess.run(hello))
    # a = tf.constant(10)
    # b = tf.constant(32)
    # sess.run(a + b)
    sess.close()
