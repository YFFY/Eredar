#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from maint.datapreparations import *
from maint.datatester import *


def eredar():

    countNum = int(sys.argv[1])
    logger = getLogger()
    sync_start, sync_end = get_unixtime_range()
    logger.info('get sync time: {0} ~ {1}'.format(sync_start, sync_end))
    dp = SyncData()
    logger.info('sync detail data begin')
    dp.sync(sync_start, sync_end)
    logger.info('sync detail data end')

    # update start and end of case
    updateCase = "update ym_case set start_time_of_case='{0}', end_time_of_case='{1}'".format(sync_start, sync_end)
    dber = Dber()
    dber.executSql(updateCase)
    dber.setColseCommit()
    logger.info("update case's time success")

    for countindex in range(countNum):
        dt = DataTester(countindex)
        resultinfo = dt.isPass
        logger.info('test:{0} case:{1} durid_result:{2} mysql_result:{3}'.format(countindex+1, result, resultinfo.get('druid_result'), resultinfo.get('mysql_result')))


if __name__ == '__main__':
    eredar()