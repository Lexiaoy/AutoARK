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

    Timer(CIRCLE_TIME, work).start()
    Android.click([1000, 2400])
    Android.click([840, 1740])
    work()

work()