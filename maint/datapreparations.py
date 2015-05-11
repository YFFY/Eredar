#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.constructor import *
from ext.databaser import *
from ext.util import *

class SyncData(object):

    def __init__(self):
        self.ymconstructor = Constructor()
        self.logger = getLogger()
        self.ymdatabaser = Dber()

    def sync(self, start_time, end_time):
        transactionid_list = self.ymconstructor.getTranasctionId
        time.sleep(timewaitquerydetail)
        if transactionid_list:
            column, druidResult = getDruidDetailResult(start_time, end_time, transactionid_list)
            if druidResult:
                self.ymdatabaser.syncDruidData(column, druidResult)
            else:
                self.logger.error('get druid detail result is None, exit')
                sys.exit()
        else:
            self.logger.error('get transaction_id list failed')
            sys.exit()

if __name__ == '__main__':
    pass