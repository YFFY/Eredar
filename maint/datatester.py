#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.databaser import *
from ext.converter import *
from ext.decorator import *
from ext.util import *
import copy



class DataTester(object):

    def __init__(self):
        self.dber = Dber()
        self.converter = QueryConverter()
        self.logger = getLogger()
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
                    druidMapList.append(dict(zip(key, value)))
            self.logger.info('get druid result: {0}'.format(druidMapList))
        except Exception as ex:
            self.logger.error('get druid result failed, get: {0}'.format(druidResult))

        column, sqlquery = self.converter.getSQL(case)
        self.logger.info('get sql case: {0}'.format(sqlquery))
        mysqlResult = list()
        mysqlMapList = list()
        try:
            mysqlResult = list(self.dber.getRecord(sqlquery))
        except TypeError as ex:
            pass

        if mysqlResult:
            for mysqlValue in mysqlResult:
                mysqlValueList = list(mysqlValue)
                mysqlMapList.append(dict(zip(column, mysqlValueList)))
        else:
            pass
        self.logger.info('get mysql result: {0}'.format(mysqlMapList))

        self.resultInfo['druid_result'] = druidMapList
        self.resultInfo['druid_query'] = case
        self.resultInfo['mysql_query'] = sqlquery
        self.resultInfo['mysql_result'] = mysqlMapList
        if druidMapList == list() and mysqlMapList == list():
            self.resultInfo['isPass'] = True
        else:
            self.resultInfo['isPass'] = (JsonDecorator(druidMapList) == JsonDecorator(mysqlMapList))
        return self.resultInfo
