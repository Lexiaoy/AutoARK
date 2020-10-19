# coding=utf-8
import re
import subprocess as sub
import xml.etree.cElementTree as ET
from android import Constants
from android.Constants import INPUT_TYPE
from android.Constants import KEYEVENT


def __parseBounds__(bounds):
    bounds = bounds[1:len(bounds) - 1]
    positions = bounds.split("][")
    leftTop = positions[0].split(",")
    rightBottom = positions[1].split(",")
    x = (int(rightBottom[0]) + int(leftTop[0])) / 2
    y = (int(rightBottom[1]) + int(leftTop[1])) / 2
    return [x, y]


def getDevices():
    devices = []
    for device in sub.check_output(Constants.ADB_DEVICE).splitlines():
        deviceStr = bytes.decode(device)
        if 'device' in deviceStr and 'devices' not in deviceStr:
            devices.append(deviceStr[:deviceStr.index('\t')])
    return devices


def pullFile(fromFile, toFile):
    sub.check_output(Constants.PULL_FILE % (fromFile, toFile))


def deleteFile(path):
    sub.check_output(Constants.DELETE_FILE % path)


def readFile(path):
    return sub.check_output(Constants.CAT % path)


def screenShort(pcTarget):
    fileName = pcTarget[pcTarget.rindex("/", 0, len(pcTarget)):len(pcTarget)]
    cacheFile = Constants.PHONE_PATH + fileName
    sub.check_output(Constants.SCREEN_CAP % cacheFile)
    pullFile(cacheFile, pcTarget)
    # deleteFile(cacheFile)


# def screenRecord( name, dirPath=CommonConstants.ROOT_PATH):
#     filePath = PHONE_PATH + name
#     sub.check_output(SCREEN_RECORD + filePath, shell=True)
#
# def finishScreenRecord():
#     sub.check_output(KILL_SERVER, shell=True)

def getUIcontent():
    cachePath = Constants.PHONE_PATH + "ui.xml"
    sub.check_output(Constants.UI_ELEMENT % cachePath)
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
    windowDisplays = sub.check_output(Constants.WINDOW_DIPLAYS)
    screenSize = re.findall(r"init=[^\s]*", windowDisplays)
    if len(screenSize) > 0:
        screenSize = (screenSize[0].replace("init=", "")).split("x")
        screenSize[0] = int(screenSize[0])
        screenSize[1] = int(screenSize[1])
    return screenSize


def isScreenOn():
    policy = sub.check_output(Constants.WINDOW_POLICY)
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
        Constants.INPUT % INPUT_TYPE.SWIPE % (start[0], start[1], end[0], end[1]))


def inputText(content):
    sub.check_output(Constants.INPUT % INPUT_TYPE.TEXT % content)


def keyEvent(key):
    sub.check_output(Constants.INPUT % INPUT_TYPE.KEYEVENT % key)


def click(position):
    sub.check_output(Constants.INPUT % INPUT_TYPE.TAP % (position[0], position[1]))


def clickText(text=None):
    click(getElementPositionByText(text))


def clickId(id=None):
    click(getElementPositionByText(getElementPositionByID(id)))


def startApp(path):
    sub.check_output(Constants.START_APP % path)


def installApp(path):
    sub.check_output(Constants.INSTALL_APP % path)


def unInstallApp(path):
    sub.check_output(Constants.UNINSTALL_APP % path)


def getCurrentActivity(package):
    result = sub.check_output(Constants.FIND_ACTIVITY % package)
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
