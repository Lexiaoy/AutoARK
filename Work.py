# coding=utf-8
from threading import Timer
from PIL import Image
import AipOcr
import Android
import json
import time

# 1.adb保存截图
# 3.分析截图
# 4.adb操作界面
TEMP_ROOT = 'temp/%s'
SCREENSHOT_FILE = TEMP_ROOT % 'screen_shot.png'
TEMP_FILE = TEMP_ROOT % 'temp.png'
LOG_FILE = 'temp/log.txt'
FORMAT = 'png'
CIRCLE_TIME = 50
SLEEP_TIME = 5


# 裁剪指定区域的内容
def cropImage(path, box):
    image = Image.open(path)
    region = image.crop(box)
    region.save(TEMP_FILE, FORMAT)


# 判断指定区域的内容
def hasContent(box, content):
    cropImage(SCREENSHOT_FILE, box)
    ocrResult = json.dumps(AipOcr.getPicText(TEMP_FILE), ensure_ascii=False)
    result = content in ocrResult
    printLog(ocrResult)
    printLog('判断状态:' + content + '--->' + str(result))
    return result


# 打印日志
def printLog(content):
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(currentTime + ': ' + content)
    with open(LOG_FILE, 'a+', encoding='utf8') as f:
        f.write(currentTime + ': ' + content + '\n')


# 点击屏幕
def androidClick(box):
    x = (box[0] + box[2]) / 2
    y = (box[1] + box[3]) / 2
    Android.click([x, y])


def work():
    printLog('===================================START===================================')

    Timer(CIRCLE_TIME, work).start()
    Android.screenShort(SCREENSHOT_FILE)
    box1 = (40, 1150, 820, 1350)
    if hasContent(box1, '行动结束'):
        androidClick(box1)
        time.sleep(SLEEP_TIME)

    Android.screenShort(SCREENSHOT_FILE)
    box2 = (2550, 1280, 2800, 1350)
    if hasContent(box2, '开始行动'):
        androidClick(box2)
        time.sleep(SLEEP_TIME)

    Android.screenShort(SCREENSHOT_FILE)
    box3 = (2260, 940, 2470, 1243)
    if hasContent(box3, 'OPERATION START'):
        androidClick(box3)
        time.sleep(SLEEP_TIME)

    Android.screenShort(SCREENSHOT_FILE)
    box4 = (740, 690, 1100, 800)
    if hasContent(box4, '等级提升'):
        androidClick(box4)
        time.sleep(SLEEP_TIME)

    printLog('===================================END===================================')


def initBox():
    print()


# initBox()
work()
