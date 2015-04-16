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
            self.conn = MySQLdb.Connect(host=self.host,user=self.user,passwd=self.password,db=self.dbname,port=self.port)
            self.cur = self.conn.cursor()
        except Exception as ex:
            traceback.print_exc()

    def syncDruidData(self, druidresult):
        insertSql = "insert into {0} values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(database.get('tablename'))
        if druidresult:
            self.insertRecord(insertSql, druidresult)

    def insertRecord(self, sql, record):
        if self.conn:
            if isinstance(record, list):
                self.cur.executemany(sql, record)
            else:
                self.cur.execute(sql, record)
        self.conn.commit()

    def getRecord(self, sql):
        if self.conn:
            executeStatus = self.cur.execute(sql)
            return self.cur.fetchall()
