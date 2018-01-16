# -*- coding: utf-8 -*-

# @Author  : super
# @Time    : 2018/1/16
# @desc    :

import io
import urllib.parse
import webbrowser
import requests
import base64
import matplotlib.pyplot as plt
from PIL import Image
import os

from colorama import init, Fore
init()

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/baidu_screenshot.png')
    os.system('adb pull /sdcard/baidu_screenshot.png .')


def pull_choices_screenshot():
    os.system('adb shell screencap -p /sdcard/baidu_choices_screenshot.png')
    os.system('adb pull /sdcard/baidu_choices_screenshot.png .')


def get_question():
    pull_screenshot()
    img = Image.open("./baidu_screenshot.png")

    # 用 matplot 查看测试分辨率，切割

    # region = img.crop((50, 350, 1000, 560)) # 坚果 pro1
    # region = img.crop((75, 315, 1167, 789)) # iPhone 7P

    # 冲顶大会
    region = img.crop((55, 220, 669, 390))

    # yy
    # region = img.crop((38, 400, 680, 580))

    # inkee
    # region = img.crop((37, 250, 680, 350))


    # im = plt.imshow(img, animated=True)
    # im2 = plt.imshow(region, animated=True)
    # plt.show()

    # 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
    api_key = 'Aj2u7EZvVmNgBdFkDj9pcR7X'
    api_secret = 'cSjS4Ee346nFhobcqBU3Gh1xo6wpZnD4'

    # 获取token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + api_secret
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }

    res = requests.get(url=host, headers=headers).json()
    token = res['access_token']

    imgByteArr = io.BytesIO()
    region.save(imgByteArr, format='PNG')
    image_data = imgByteArr.getvalue()
    base64_data = base64.b64encode(image_data)
    r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                      params={'access_token': token}, data={'image': base64_data})
    result = ''
    for i in r.json()['words_result']:
        result += i['words']
    # result = urllib.parse.quote(result)
    # webbrowser.open('https://baidu.com/s?wd=' + result)
    return result


def get_choices():
    pull_choices_screenshot()
    img = Image.open("./baidu_choices_screenshot.png")

    # 用 matplot 查看测试分辨率，切割

    # region = img.crop((50, 350, 1000, 560)) # 坚果 pro1
    # region = img.crop((75, 315, 1167, 789)) # iPhone 7P

    # 冲顶大会
    region = img.crop((65, 436, 673, 747))

    # yy
    # region = img.crop((47, 600, 510, 840))

    # inkee
    # region = img.crop((37, 350, 507, 780))


    # im = plt.imshow(img, animated=True)
    # im2 = plt.imshow(region, animated=True)
    # plt.show()

    # 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
    api_key = 'Aj2u7EZvVmNgBdFkDj9pcR7X'
    api_secret = 'cSjS4Ee346nFhobcqBU3Gh1xo6wpZnD4'

    # 获取token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + api_secret
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }

    res = requests.get(url=host, headers=headers).json()
    token = res['access_token']

    imgByteArr = io.BytesIO()
    region.save(imgByteArr, format='PNG')
    image_data = imgByteArr.getvalue()
    base64_data = base64.b64encode(image_data)
    r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                      params={'access_token': token}, data={'image': base64_data})

    result = []
    for i in r.json()['words_result']:
        word = i['words']
        result.append(word)
    # result = urllib.parse.quote(result)
    # webbrowser.open('https://baidu.com/s?wd=' + result)
    return result

def count_base(question, choices):
    print('\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n')
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question})
    content = req.text
    # print(content)
    counts = []
    print('Question: '+ question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')
    for i in range(len(choices)):
        print(choices[i])
        counts.append(content.count(choices[i]))
        #print(choices[i] + " : " + str(counts[i]))
    output(choices, counts)


def output(choices, counts):
    counts = list(map(int, counts))
    #print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return

    for i in range(len(choices)):
        print()
        if i == index_max:
            # 绿色为计数最高的答案
            print(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
        elif i == index_min:
            # 红色为计数最低的答案
            print(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
        else:
            print("{0} : {1}".format(choices[i], counts[i]))
