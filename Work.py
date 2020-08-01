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
WORK_TIME = 30
SLEEP_TIME = 3


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


def work(box):
    time.sleep(SLEEP_TIME)
    Android.screenShort(SCREENSHOT_FILE)
    img_box = (box[0], box[1], box[2], box[3])
    if hasContent(img_box, box[4]):
        androidClick(box)


def start():
    printLog('===================================START===================================')

    # box1 = (90, 870, 630, 1010)
    # box2 = (1940, 940, 2250, 1030)
    # box3 = (1760, 550, 1970, 970)
    box1 = (2550, 1280, 2800, 1350, '开始行动')
    box2 = (2260, 940, 2470, 1243, 'OPERATION START')
    box3 = (40, 1150, 820, 1350, '行动结束')
    box4 = (740, 690, 1100, 800, '等级提升')

    work(box1)
    work(box2)
    work(box3)
    work(box4)

    printLog('===================================END===================================')
    start()


start()
