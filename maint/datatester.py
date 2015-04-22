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

        sql = self.converter.getSQL(case)
        self.logger.info('get sql: {0}'.format(sql))
        druidResult = getResponse(case)
        try:
            mysqlResult = list(self.dber.getRecord(sql, isAll=True))
        except TypeError as ex:
            self.logger.error('get empty set from mysql')
            return self.resultInfo

        druidData = json.loads(druidResult).get('data').get('data')
        column = druidData[0]
        druidMapList = list()
        for value in druidData[1:]:
            druidMapList.append(dict(zip(column, value)))

        mysqlMapList = list()
        for mysqlValue in mysqlResult:
            mysqlValueList = list(mysqlValue)
            for i in range(len(mysqlValueList) - len(column)):
                mysqlValueList.pop()
            mysqlMapList.append(dict(zip(column, mysqlValueList)))
        self.resultInfo['druid_result'] = druidMapList
        self.resultInfo['druid_query'] = druid_query
        self.resultInfo['mysql_query'] = sql
        self.resultInfo['mysql_result'] = mysqlMapList
        self.resultInfo['isPass'] = (JsonDecorator(druidMapList) == JsonDecorator(mysqlMapList))
        return self.resultInfo
