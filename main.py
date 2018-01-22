# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd


class Director(object):
    result = []
    METHOD = 'method hello'

    def __init__(self, name):
        self.name = name

    def __del__(self):
        self.name = ''

    def get_name(self):
        return self.name

    def quicksort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[int(len(arr) / 2)]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x < pivot]
        right = [x for x in arr if x > pivot]
        return middle

    @staticmethod
    def test3():
        print(Director.METHOD)
        print('test3')

    @classmethod
    def test2(cls):
        print(cls)
        print('test2')


if __name__ == '__main__':
    director = Director('天天')
    print(director.get_name())
    test = [3, 6, 8, 10, 1, 2, 1]
    print(director.quicksort(test))
    Director.test3()
    Director.test2()
    a = np.arange(30)
    a.shape = 2, -1, 3
    print(a.shape)
    print(a)
    s = pd.Series(np.array([1, 1, 2, 3, 5, 8]))
    print(s)


