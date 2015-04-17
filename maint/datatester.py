#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.databaser import *
from ext.converter import *
from ext.decorator import *
from ext.util import *



class DataTester(object):

    def __init__(self, caseindex):
        self.dber = Dber()
        self.converter = QueryConverter()
        self.caseindex = caseindex
        self.get_case()
        self.get_sql()

    def get_case(self):
        self.caseinfo = self.dber.getCase(self.caseindex)
        self.caseno, self.casename, self.casecontent = self.caseinfo[0], self.caseinfo[1], self.caseinfo[2]

    def get_sql(self):
        self.sql = self.converter.getSQL(self.casecontent)

    def get_druid_result(self):
        return getResponse(self.casecontent)

    def get_mysql_result(self):
        return list(self.dber.getRecord(self.sql)[0])

    @property
    def isPass(self):
        druidResult = self.get_druid_result()
        mysqlResult = self.get_mysql_result()

        druidData = json.loads(druidResult).get('data').get('data')
        column = druidData[0]
        druidMap = dict(zip(column, druidData[1]))

        for i in range(len(mysqlResult) - len(column)):
            mysqlResult.pop()
        mysqlMap = dict(zip(column, mysqlResult))
        if JsonDecorator(druidData) == JsonDecorator(mysqlMap):
            result = 'success'
        else:
            result = 'failed'
        current = get_now()
        updateSql = "update {0} set run_time='{1}',run_result='{2}' where caseno={3}".format(database.get('case_table'), current, result, self.caseno)
        self.dber.executSql(updateSql)
        self.dber.setColseCommit()
        return result

if __name__ == '__main__':
    dt = DataTester(0)
    dt.isPass