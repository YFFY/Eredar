#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.constructor import *
from ext.databaser import *
from ext.util import *

class SyncData(object):

    def __init__(self):
        self.ymconstructor = Constructor()
        self.ymdatabaser = Dber()

    def sync(self, start_time, end_time):
        transactionid_list = self.ymconstructor.getTranasctionId
        if transactionid_list:
            column, druidResult = getDruidDetailResult(start_time, end_time, transactionid_list)
            if druidResult:
                self.ymdatabaser.syncDruidData(column, druidResult)
            else:
                pass
        else:
            pass

if __name__ == '__main__':
    pass