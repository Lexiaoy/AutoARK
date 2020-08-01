# coding=utf-8
from threading import Timer
from PIL import Image
import AipOcr
import Android
import json
import time

TEMP_ROOT = 'temp/%s'
SCREENSHOT_FILE = TEMP_ROOT % 'screen_shot.png'
TEMP_FILE = TEMP_ROOT % 'temp.png'
LOG_FILE = 'temp/log.txt'
FORMAT = 'png'
CIRCLE_TIME = 20
SLEEP_TIME = 5

def work():
    time.sleep(0.4)
    Android.click([1000, 2480])
    time.sleep(0.4)
    Android.click([840, 1740])
    # Android.click([755, 2170])
    # time.sleep(0.1)
    # Android.click([630, 1450])
    work()

work()