#! /usr/bin/env python
# --*-- coding:utf-8 --*--


import os
import sys
sys.path.append(os.path.split(os.path.abspath(sys.path[0]))[0])

from ext.databaser import *
from ext.converter import *
from ext.decorator import *
from ext.util import *
import copy



class DataTester(object):

    def __init__(self):
        self.dber = Dber()
        self.converter = QueryConverter()
        self.resultInfo = copy.deepcopy(detailresultinfo)

    def runCase(self, case):

        druidMapList = list()
        druidResult = getResponse(case)
        try:
            druidData = json.loads(druidResult).get('data').get('data')
            if len(druidData) == 1:  # empty set
                pass
            else:
                key = druidData[0]
                for value in druidData[1:]:
                    druidMapList.append(dict(zip(key, getStrList(value))))
        except Exception as ex:
            pass

        column, sqlquery = self.converter.getSQL(case)
        mysqlResult = list()
        mysqlMapList = list()
        try:
            mysqlResult = list(self.dber.getRecord(sqlquery))
        except TypeError as ex:
            pass

        if mysqlResult:
            for mysqlValue in mysqlResult:
                mysqlValueList = getStrList(mysqlValue)
                mysqlMapList.append(dict(zip(column, mysqlValueList)))
        else:
            pass

        self.resultInfo['druid_result'] = druidMapList
        self.resultInfo['druid_query'] = case
        self.resultInfo['mysql_query'] = sqlquery
        self.resultInfo['mysql_result'] = mysqlMapList
        if druidMapList == list() and mysqlMapList == list():
            self.resultInfo['isPass'] = True
        else:
            self.resultInfo['isPass'] = (JsonDecorator(druidMapList) == JsonDecorator(mysqlMapList))
        return self.resultInfo
