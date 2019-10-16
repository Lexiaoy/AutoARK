# coding=utf-8
import subprocess as sub

TYPE = "type %s"  # windows读取文件内容


class CMDUtils:

    def readFile(self, path):
        return sub.check_output(TYPE % path)
