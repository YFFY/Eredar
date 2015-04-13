#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import time
from config.setting import TIME_FORMAT

def get_datatime(value):
    return time.strftime(TIME_FORMAT, time.localtime(value))