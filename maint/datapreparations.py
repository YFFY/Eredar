#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.constructor import *
from ext.databaser import *
from ext.util import *

class SyncData(object):

    def __init__(self):
        self.ymconstructor = Constructor()
        self.ymdatabaser = Dber()
        self.logger = getLogger()

    def sync(self, start_time, end_time):
        self.logger.info('get sync time: {0} - {1}'.format(start_time, end_time))
        transactionid_list = self.ymconstructor.getTranasctionId
        if transactionid_list:
            self.logger.info('get transction_id list success, length: {0} content:{1}'.format(len(transactionid_list), transactionid_list))
            druidResult = getDruidDetailResult(start_time, end_time, transactionid_list)
            if druidResult:
                self.logger.info('get druid detail result success, result: {0}'.format(druidResult))
                self.ymdatabaser.syncDruidData(druidResult)
            else:
                self.logger.error('get empty druid detail result list, check collector, kafka, realtime carefully')
        else:
            self.logger.error('get transaction_id list failed, check vn and cc first')


if __name__ == '__main__':
    sd = SyncData()
    sd.sync(1429142400, 1429228800)