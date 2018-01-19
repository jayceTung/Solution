# -*- coding: utf-8 -*-
import os


class Director(object):
    result = []

    def __init__(self, name):
        self.name = name

    def __del__(self):
        self.name = ''

    def get_name(self):
        return self.name

if __name__ == '__main__':
    director = Director('天天')
    print(director.get_name())


