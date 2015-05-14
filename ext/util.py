#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
import time
import json
import traceback
from bs4 import BeautifulSoup
import requests
import logging
import logging.config
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
    time.sleep(timewaitquerydetail)
    logging.info('wait {0} seconds that flow data to druid'.format(timewaitquerydetail))
    try:
        r = requests.get(geturl)
        data = json.loads(r.text).get('data').get('data')
        if realDataCount != len(data[1:]):
            logger.error('imitate data count: {0} != query detail data count: {1}'.format(realDataCount, len(data[1:])))
            sys.exit()
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
        strValueList.append(str(v))
    return strValueList

def getVaildColumn(column):
    if isinstance(column, list):
        columnString = ','.join(column)
    return '({0})'.format(columnString)


if __name__ == '__main__':
    print get_unixtime_range()