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
        self.setColseCommit()

    def getCase(self):
        case = self.getRecord('select * from ym_case limit 1')
        return case[0]

    def executSql(self, sql):
        if self.conn:
            self.cur.execute(sql)

    def setColseCommit(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def getRecord(self, sql):
        if self.conn:
            executeStatus = self.cur.execute(sql)
            return self.cur.fetchall()
