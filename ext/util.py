#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
sys.path.append(os.path.split(os.path.abspath(sys.path[0]))[0])

from datetime import datetime
import time
import json
import traceback
from bs4 import BeautifulSoup
import requests
import logging
import logging.config
from decimal import Decimal
from config.setting import *


def get_datatime(value):
    return time.strftime(TIME_FORMAT, time.localtime(value))

def get_now():
    return time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()))

def get_unixtime_range():
     start = int(time.mktime(time.strptime(get_now(), '%Y-%m-%dT%H:%M:%S'))) - 120
     end = start + unix_end_offset_seconds
     return start, end

def datetime_timestamp(datetime):
    return int(time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S')))

def get_clickid(content):
    soup = BeautifulSoup(content)
    for link in soup.find_all('a'):
        return link.get('href').split('=')[1]

def getLogger():
    logging.config.fileConfig(os.path.join(os.path.split(sys.path[0])[0],'config/logging.conf'))
    logger = logging.getLogger("eredar")
    return logger

def getDruidDetailResult(start_time, end_time, transaction_id_list, realDataCount):
    logger = getLogger()
    param = param_template % (start_time, end_time, transaction_id_list)
    if "'" in param:
        param = param.replace("'",'"')
    geturl = query_url + param
    isEnvOK()
    logger.info('get detail query param: {0}'.format(param))
    logger.info('wait {0} seconds that flow data to druid'.format(timewaitquerydetail))
    time.sleep(timewaitquerydetail)
    try:
        r = requests.get(geturl)
        data = json.loads(r.text).get('data').get('data')
        if realDataCount != len(data[1:]):
            logger.error('imitate data count: {0} != query detail data count: {1}'.format(realDataCount, len(data[1:])))
            sys.exit()
        else:
            logger.info('imitate data count: {0} equal to query detail data count: {1}'.format(realDataCount, len(data[1:])))
        return data[0], data[1:]
    except Exception as ex:
        logger.error('get druid detail result failed: {0}'.format(ex))
        sys.exit()
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

def getTaskFlag():
    return 'tf{0}'.format(int(time.time()))

def unicode2str(unicodeList):
    strList = list()
    if unicodeList:
        for u in unicodeList:
            if not isinstance(u, basestring):
                strList.append(u)
            else:
                strList.append(u.encode())
    return tuple(strList)

def getStrList(valueList):
    strValueList = list()
    for v in valueList:
        if v == datetime.now().year:
            strValueList.append(str(v))
        elif isinstance(v, Decimal):
            if str(v).find('.') != -1:
                strValueList.append(float(v))
        else:
            strValueList.append(v)
    return strValueList

def getVaildColumn(column):
    if isinstance(column, list):
        columnString = ','.join(column)
    return '({0})'.format(columnString)

def setCache():
    logger = getLogger()
    result = os.popen(cachecmd).read()
    if result.startswith("success"):
        logger.info('reset l1 cache and l2 cache false success')
    result = os.popen(routercmd).read()
    if result.startswith("successfully"):
        logger.info('reset router to druid success')

def portScanner(machine):
    import socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect(machine)
    except Exception as ex:
        return ex
    sk.close()
    return "OK"

def isEnvOK():
    logger = getLogger()
    for machine in machineList:
        if portScanner(machine) != "OK":
            logger.error('telnet {0} on port {1} failed'.format(machine[0], machine[1]))
            sys.exit()
    logger.info('check envirment success')
