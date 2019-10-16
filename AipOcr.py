# coding=utf-8
from aip import AipOcr

APP_ID = '17518892'
API_KEY = 'hs3FjrKEFW55u2uknfG98DeP'
SECRET_KEY = 'sY9lZTguhZbosIy6fgpZz5kSZVPiv3wF'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def getPicText(filePath):
    client.setConnectionTimeoutInMillis(20000)
    client.setSocketTimeoutInMillis(15000)
    image = get_file_content(filePath)
    return client.basicGeneral(image)
