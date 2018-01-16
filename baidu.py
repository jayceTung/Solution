# -*- coding: utf-8 -*-

# @Author  : super
# @Time    : 2018/1/16
# @desc    :
from common import baiduApi

while True:
    go = input("请输入n暂停:")

    if go == 'n':
        break

    print("------------------")
    baiduApi.start_search()
