# coding=utf-8
import re
import subprocess as sub
import xml.etree.cElementTree as ET
import AndroidConstants
from AndroidConstants import INPUT_TYPE
from AndroidConstants import KEYEVENT
import CommonConstants


def __parseBounds__(bounds):
    bounds = bounds[1:len(bounds) - 1]
    positions = bounds.split("][")
    leftTop = positions[0].split(",")
    rightBottom = positions[1].split(",")
    x = (int(rightBottom[0]) + int(leftTop[0])) / 2
    y = (int(rightBottom[1]) + int(leftTop[1])) / 2
    return [x, y]


def pullFile(fromFile, toFile=CommonConstants.DEFAULT_FILE):
    sub.check_output(AndroidConstants.PULL_FILE % (fromFile, toFile))


def deleteFile(path):
    sub.check_output(AndroidConstants.DELETE_FILE % path)


def readFile(path):
    return sub.check_output(AndroidConstants.CAT % path)


def screenShort(pcTarget):
    fileName = pcTarget[pcTarget.rindex("/", 0, len(pcTarget)):len(pcTarget)]
    cacheFile = AndroidConstants.PHONE_PATH + fileName
    sub.check_output(AndroidConstants.SCREEN_CAP % cacheFile)
    pullFile(cacheFile, pcTarget)
    deleteFile(cacheFile)


# def screenRecord( name, dirPath=CommonConstants.ROOT_PATH):
#     filePath = PHONE_PATH + name
#     sub.check_output(SCREEN_RECORD + filePath, shell=True)
#
# def finishScreenRecord():
#     sub.check_output(KILL_SERVER, shell=True)

def getUIcontent():
    cachePath = AndroidConstants.PHONE_PATH + "ui.xml"
    sub.check_output(AndroidConstants.UI_ELEMENT % cachePath)
    uiContent = readFile(cachePath)
    deleteFile(cachePath)
    return uiContent


def getElementByText(content=None):
    uiContent = getUIcontent()
    root = ET.fromstring(uiContent)
    for child in root.iter("node"):
        if child.get("text") == content:
            return child
    return None


def getElementsByText(content=None):
    result = []
    uiContent = getUIcontent()
    root = ET.fromstring(uiContent)
    for child in root.iter("node"):
        if child.get("text") == content:
            result.append(child)
    return result


def getElementById(id=None):
    uiContent = getUIcontent()
    root = ET.fromstring(uiContent)
    for child in root.iter("node"):
        if child.get("resource-id").endswith(id):
            return child
    return None


def getElementsById(id=None):
    result = []
    uiContent = getUIcontent()
    root = ET.fromstring(uiContent)
    for child in root.iter("node"):
        if child.get("resource-id").endswith(id):
            result.append(child)
    return result


def getElementPositionByText(content=None):
    element = getElementByText(content)
    if element is None: return None
    bounds = element.get("bounds")
    return __parseBounds__(bounds)


def getElementsPositionByText(content=None):
    elements = getElementsByText(content)
    positions = []
    for element in elements:
        bounds = element.get("bounds")
        positions.append(__parseBounds__(bounds))
    return positions


def getElementPositionByID(id=None):
    element = getElementById(id)
    if element is None: return None
    bounds = element.get("bounds")
    return __parseBounds__(bounds)


def getElementsPositionByID(id=None):
    elements = getElementsById(id)
    positions = []
    for element in elements:
        bounds = element.get("bounds")
        positions.append(__parseBounds__(bounds))
    return positions


def getScreenDimension():
    windowDisplays = sub.check_output(AndroidConstants.WINDOW_DIPLAYS)
    screenSize = re.findall(r"init=[^\s]*", windowDisplays)
    if len(screenSize) > 0:
        screenSize = (screenSize[0].replace("init=", "")).split("x")
        screenSize[0] = int(screenSize[0])
        screenSize[1] = int(screenSize[1])
    return screenSize


def isScreenOn():
    policy = sub.check_output(AndroidConstants.WINDOW_POLICY)
    if "mScreenOnFully=true" in policy:
        return True
    return False


def unlockScreen(psw=None):
    screenState = isScreenOn()
    print(screenState)
    if not isScreenOn():
        keyEvent(KEYEVENT.KEYCODE_POWER)
    keyEvent(KEYEVENT.KEYCODE_MENU)


def swip(start, end):
    sub.check_output(
        AndroidConstants.INPUT % INPUT_TYPE.SWIPE % (start[0], start[1], end[0], end[1]))


def inputText(content):
    sub.check_output(AndroidConstants.INPUT % INPUT_TYPE.TEXT % content)


def keyEvent(key):
    sub.check_output(AndroidConstants.INPUT % INPUT_TYPE.KEYEVENT % key)


def click(position):
    sub.check_output(AndroidConstants.INPUT % INPUT_TYPE.TAP % (position[0], position[1]))


def clickText(text=None):
    click(getElementPositionByText(text))


def clickId(id=None):
    click(getElementPositionByText(getElementPositionByID(id)))


def startApp(path):
    sub.check_output(AndroidConstants.START_APP % path)


def installApp(path):
    sub.check_output(AndroidConstants.INSTALL_APP % path)


def unInstallApp(path):
    sub.check_output(AndroidConstants.UNINSTALL_APP % path)


def getCurrentActivity(package):
    result = sub.check_output(AndroidConstants.FIND_ACTIVITY % package, shell=True)
    result = re.findall(r"%s[^)]*" % package, result)
    if len(result) > 0:
        result = result[0]
    else:
        result = ""
    return result


def verifyActivity(package, activity):
    output = getCurrentActivity(package)
    if activity in output:
        return True
    return False
