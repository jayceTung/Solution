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
    question = baiduApi.get_question()
    choices = baiduApi.get_choices()
    baiduApi.count_base(question, choices)
