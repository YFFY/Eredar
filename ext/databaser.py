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
                self.logger.info('get sync data sql: {0}'.format(insertSql))
                self.executSql(insertSql)
        else:
            self.logger.error("get druid result is not a list, exit")
        self.setColseCommit()
        self.logger.info('insert druid detail data to mysql success')

    def getCase(self, index):
        case = self.getRecord('select * from ym_case')
        return case[index-1]

    def executSql(self, sql):
        if self.conn:
            result = self.cur.execute(sql)
        return result

    def setColseCommit(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def getRecord(self, sql):
        if self.conn:
            executeStatus = self.cur.execute(sql)
            return self.cur.fetchall()
