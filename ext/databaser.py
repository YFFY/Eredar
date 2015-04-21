#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import MySQLdb
from ext.util import *
from config.setting import *


class Dber(object):

    def __init__(self):
        self.host = database.get('host')
        self.port = database.get('port')
        self.user = database.get('user')
        self.password = database.get('password')
        self.dbname = database.get('databasename')
        self.conn = None
        self.setConnection()
        self.logger = getLogger()


    def setConnection(self):
        try:
            self.conn = MySQLdb.Connect(host=self.host,user=self.user,passwd=self.password,db=self.dbname,port=self.port,charset='utf8')
            self.cur = self.conn.cursor()
        except Exception as ex:
            traceback.print_exc()

    def syncDruidData(self, column, druidresult):
        if isinstance(druidresult, list):
            for result in druidresult:
                insertSql = sync_sql.format(database.get('detail_table'), getVaildColumn(column), unicode2str(result))
                self.executSql(insertSql)
                self.logger.info('sync one druid detail record to mysql success')
        else:
            self.logger.error("get druid result is not a list, exit")
        self.setColseCommit()

    def getCase(self, index):
        case = self.getRecord('select * from ym_case')
        return case[index-1]

    def executSql(self, sql):
        try:
            if self.conn:
                result = self.cur.execute(sql)
            return result
        except Exception as ex:
            self.logger.error("execute sql err: ", ex)

    def setColseCommit(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def getRecord(self, sql):
        if self.conn:
            executeStatus = self.cur.execute(sql)
            return self.cur.fetchall()
