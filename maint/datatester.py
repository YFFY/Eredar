#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.databaser import *
from ext.converter import *
from ext.decorator import *
from ext.util import *



class DataTester(object):

    def __init__(self, taskid, caseindex):
        self.dber = Dber()
        self.converter = QueryConverter()
        self.caseindex = caseindex
        self.taskid = taskid
        self.logger = getLogger()
        self.get_case()
        self.get_sql()

    def get_case(self):
        self.caseinfo = self.dber.getCase(self.caseindex)
        self.caseid, self.casename, self.start, self.end , self.casecontent = self.caseinfo[0], self.caseinfo[1], self.caseinfo[2], self.caseinfo[3], self.caseinfo[4]
        if isinstance(self.start, basestring):
            self.start = int(self.start)
        if isinstance(self.end, basestring):
            self.end = int(self.end)
        self.casecontent = self.casecontent % (self.start, self.end)
        self.logger.info('get case :{0}'.format(self.casecontent))

    def get_sql(self):
        self.sql = self.converter.getSQL(self.casecontent)
        self.logger.info('get sql: {0}'.format(self.sql))

    def get_druid_result(self):
        return getResponse(self.casecontent)

    def get_mysql_result(self):
        try:
            return list(self.dber.getRecord(self.sql)[0])
        except IndexError as ex:
            self.logger.error('get mysql result is empty set, check ym_detail table first')

    @property
    def isPass(self):
        druidResult = self.get_druid_result()
        mysqlResult = self.get_mysql_result()

        self.logger.info('get druid result: {0}'.format(druidResult))
        self.logger.info('get mysql result: {0}'.format(mysqlResult))

        druidData = json.loads(druidResult).get('data').get('data')
        column = druidData[0]
        druidMap = dict(zip(column, druidData[1]))

        resultinfo = dict()

        for i in range(len(mysqlResult) - len(column)):
            mysqlResult.pop()
        mysqlMap = dict(zip(column, mysqlResult))
        if JsonDecorator(druidMap) == JsonDecorator(mysqlMap):
            result = 'success'
        else:
            result = 'failed'
        current = get_now()
        updateSql = """update ym_result set druid_result = "{0}", druid_query = '{1}', mysql_query = "{2}", mysql_result = "{3}", run_time = "{4}" where taskid = {5} and caseid = {6}""".format(
            druidMap, self.casecontent, self.sql, mysqlMap, get_now(), self.taskid, self.caseid
        )
        self.logger.info('get update case info sql: {0}'.format(updateSql))
        self.dber.executSql(updateSql)
        self.dber.setCommit()
        self.dber.setColse()
        self.logger.info('exexute update case info sql success')
        resultinfo["result"] = result
        self.logger.info('get druid map result: {0}'.format(druidMap))
        self.logger.info('get mysql map result: {0}'.format(mysqlMap))
        resultinfo["druid_result"] = druidMap
        resultinfo["mysql_result"] = mysqlMap
        return resultinfo

if __name__ == '__main__':
    dt = DataTester(0)
    dt.isPass