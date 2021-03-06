#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
sys.path.append(os.path.split(os.path.abspath(sys.path[0]))[0])

from ext.constructor import *
from ext.databaser import *
from ext.util import *

class SyncData(object):

    def __init__(self):
        self.ymconstructor = Constructor()
        self.logger = getLogger()
        self.ymdatabaser = Dber()

    def sync(self, start_time, end_time):
        realDataCount, transactionid_list = self.ymconstructor.getTranasctionId

        if transactionid_list:
            column, druidResult = getDruidDetailResult(start_time, end_time, transactionid_list, realDataCount)
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