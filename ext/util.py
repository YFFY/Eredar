#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import time
import json
import traceback
import requests
from config.setting import *


def get_datatime(value):
    return time.strftime(TIME_FORMAT, time.localtime(value))

def get_clickid(rsp):
    pass

class Logger():

    def __init__(self, logname, loglevel, logger):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

if __name__ == '__main__':
    pass