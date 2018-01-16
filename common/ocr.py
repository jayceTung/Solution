# -*- coding: utf-8 -*-

# @Author  : super
# @Time    : 2018/1/15
# @desc    : image translate word

from PIL import Image
import pytesseract


# 二值化算法
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 去除干扰线算法
def depoint(img):  # input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:
                count = count + 1
            if pixdata[x, y + 1] > 245:
                count = count + 1
            if pixdata[x - 1, y] > 245:
                count = count + 1
            if pixdata[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x, y] = 255
    return img


def img_ocr(image):
    # 冲顶大会
    # question_im = image.crop((75, 250, 669, 414))
    # choices_im = image.crop((70, 436, 673, 747))

    # yy
    question_im = image.crop((38, 348, 509, 422))
    choices_im = image.crop((47, 458, 510, 644))

    # 边缘增强滤波,不一定适用
    # question_im = question_im.filter(ImageFilter.EDGE_ENHANCE)
    # choices_im = choices_im.filter(ImageFilter.EDGE_ENHANCE)

    # 转化为灰度图
    question_im = question_im.convert('L')
    choices_im = choices_im.convert('L')
    # 把图片变成二值图像
    question_im = binarizing(question_im, 190)
    choices_im = binarizing(choices_im, 190)
    # img=depoint(choices_im)
    # img.show()

    # win环境
    # tesseract 路径
    # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    # 语言包目录和参数
    # tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6'

    # mac 环境 记得自己安装训练文件
    # tesseract 路径
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'
    # 语言包目录和参数
    tessdata_dir_config = '--tessdata-dir "/usr/local/Cellar/tesseract/3.05.01/share/tessdata/" --psm 6'

    # lang 指定中文简体
    question = pytesseract.image_to_string(question_im, lang='chi_sim', config=tessdata_dir_config)
    question = question.replace("\n", "")[2:]
    # 处理将"一"识别为"_"的问题
    question = question.replace("_", "一")

    choice = pytesseract.image_to_string(choices_im, lang='chi_sim', config=tessdata_dir_config)
    # 处理将"一"识别为"_"的问题
    choices = choice.strip().replace("_", "一").split("\n")
    choices = [x for x in choices if x != '']

    # 兼容截图设置不对，意外出现问题为两行或三行
    if (choices[0].endswith('?')):
        question += choices[0]
        choices.pop(0)
    if (choices[1].endswith('?')):
        question += choices[0]
        question += choices[1]
        choices.pop(0)
        choices.pop(1)

    return question, choices

if __name__ == '__main__':
    image = Image.open("./screenshot.png")
    question, choices = img_ocr(image)
    print("识别结果")
    print(question)
    print(choices)
