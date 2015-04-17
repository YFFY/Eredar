#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
import time
import json
import traceback
from bs4 import BeautifulSoup
import requests
from config.setting import *


def get_datatime(value):
    return time.strftime(TIME_FORMAT, time.localtime(value))

def get_now():
    return time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()))

def get_unixtime_range():
    unix_start = int(time.time())
    unix_end = unix_start + 28800
    return unix_start, unix_end

def datetime_timestamp(datetime):
    return int(time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S')))

def get_clickid(content):
    soup = BeautifulSoup(content)
    for link in soup.find_all('a'):
        return link.get('href').split('=')[1]

def getLogger(logname = 'sync.log'):
    logger = Logger(getLogPath(logname), 1, 'root').getlog()
    return logger

def getLogPath(logname):
    return os.path.join(os.path.split(os.path.abspath(sys.path[0]))[0], 'log/{0}'.format(logname))

def getDruidDetailResult(start_time, end_time, transaction_id_list):
    param = param_template % (start_time, end_time, transaction_id_list)
    if "'" in param:
        param = param.replace("'",'"')
    geturl = query_url + param
    try:
        r = requests.get(geturl)
        data = json.loads(r.text).get('data').get('data')
        return data[0], data[1:]
    except Exception as ex:
        traceback.print_exc()
    else:
        return None

def getResponse(param):
    url = query_url + param
    try:
        r = requests.get(url)
    except Exception as ex:
        traceback.print_exc()
    else:
        return r.text


def unicode2str(unicodeList):
    strList = list()
    if unicodeList:
        for u in unicodeList:
            if not isinstance(u, basestring):
                strList.append(u)
            else:
                strList.append(u.encode())
    return tuple(strList)

def getVaildColumn(column):
    if isinstance(column, list):
        columnString = ','.join(column)
    return '({0})'.format(columnString)


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