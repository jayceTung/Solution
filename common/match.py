# -*- coding: utf-8 -*-

# @Author  : super
# @Time    : 2018/1/23
# @desc    : 正则表达式

import re
import os


def match(string):
    if re.match(r'\d*', string):
        return True
    else:
        return False


if __name__ == '__main__':
    print(match('1211111'))
    print(os.getpid())
