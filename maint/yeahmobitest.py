#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from maint.datapreparations import *
from maint.datatester import *


def eredar(countNum):

    if countNum == -1:
        countNum = int(sys.argv[1])
    logger = getLogger()
    logger.info('get sync time: {0} ~ {1}'.format(sync_start, sync_end))
    dp = SyncData()
    logger.info('sync detail data begin')
    dp.sync(sync_start, sync_end)
    logger.info('sync detail data end')
    for countindex in range(countNum):
        dt = DataTester(countindex)
        dt.isPass


if __name__ == '__main__':
    eredar()