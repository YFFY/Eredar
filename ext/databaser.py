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

    def syncDruidData(self, druidresult):
        if isinstance(druidresult, list):
            for result in druidresult:
                insertSql = "insert into {0} values {1}".format(database.get('tablename'), unicode2str(result))
                self.insertRecord(insertSql)
        self.setColseCommit()

    def insertRecord(self, sql):
        if self.conn:
            self.cur.execute(sql)

    def setColseCommit(self):
        self.cur.commit()
        self.conn.commit()
        self.conn.close()

    def getRecord(self, sql):
        if self.conn:
            executeStatus = self.cur.execute(sql)
            return self.cur.fetchall()
