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


def cropImage(path, box):
    image = Image.open(path)
    region = image.crop(box)
    region.save(TEMP_FILE, FORMAT)


def hasContent(box, content):
    cropImage(SCREENSHOT_FILE, box)
    ocrResult = json.dumps(AipOcr.getPicText(TEMP_FILE), ensure_ascii=False)
    result = content in ocrResult
    printLog(ocrResult)
    printLog('判断状态:' + content + '--->' + str(result))
    return result


def printLog(content):
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(currentTime + ': ' + content)
    with open(LOG_FILE, 'a+', encoding='utf8') as f:
        f.write(currentTime + ': ' + content + '\n')


def work():
    printLog('===================================START===================================')

    Timer(20, work).start()
    Android.screenShort(SCREENSHOT_FILE)
    box1 = (40, 1150, 820, 1350)
    if hasContent(box1, '行动结束'):
        Android.click([40, 1150])
        time.sleep(8)

    Android.screenShort(SCREENSHOT_FILE)
    box2 = (2550, 1280, 2800, 1350)
    if hasContent(box2, '开始行动'):
        Android.click([2675, 1315])
        time.sleep(8)

    Android.screenShort(SCREENSHOT_FILE)
    box3 = (2260, 940, 2470, 1243)
    if hasContent(box3, 'OPERATION START'):
        Android.click([2365, 1090])

    printLog('===================================END===================================')

work()
