#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from datapreparations import *
from datatester import *
from random import randint


class YeahMobiTask(object):

    def __init__(self):
        self.executor = Dber()
        self.setTaskCaseNum()
        self.setTaskCaseNum()
        self.logger = getLogger()

    def setTaskName(self, taskName):
        self.taskName = taskName

    def getTaskName(self):
        return self.taskName

    def setTaskCaseNum(self, caseNum):
        self.caseNum = caseNum

    def getTaskCaseNum(self):
        return self.caseNum

    def getTaskId(self):
        return randint(1, 1000000)

    def sync2db(self):
        taskId = self.getTaskId()
        ymtasksql = 'insert into ym_task(taskid, taskname, createtime) values("{0}", "{1}", "{2}")'.format(
            taskId, self.getTaskName(), get_now()
        )
        self.executor.executSql(ymtasksql)
        self.logger.info('create task {0} success'.format(self.getTaskName()))
        if isinstance(int(caseNum), int):
            for caseid in range(caseNum):
                ymresultsql = 'insert into ym_result(taskid, caseid) values("{0}", "{1}")'.format(
                    taskId, caseid
                )
                self.executor.executSql(ymresultsql)
                self.logger.info('add taskid {0} caseid {1} success'.format(taskId, caseid))
        self.executor.setColseCommit()

    def runTask(self, needSyncNewData = True, needUpdateCase = True):
        sync_start, sync_end = get_unixtime_range()
        if needSyncNewData:
            self.logger.info('set sync time: {0} ~ {1}'.format(sync_start, sync_end))
            dp = SyncData()
            self.logger.info('sync detail data begin')
            dp.sync(sync_start, sync_end)
            self.logger.info('sync detail data success')

        if needUpdateCase:
            updateCase = "update ym_case set start_time_of_case='{0}', end_time_of_case='{1}'".format(sync_start, sync_end)
            self.executor.executSql(updateCase)
            self.executor.setColseCommit()
            self.logger.info("update case success")

        self.sync2db()
        for index in range(caseNum):
            dt = DataTester(index)
            resultinfo = dt.isPass
            self.logger.info('test:{0} case:{1} durid_result:{2} mysql_result:{3}'.format(countindex+1, resultinfo.get('result'), resultinfo.get('druid_result'), resultinfo.get('mysql_result')))



if __name__ == '__main__':
    try:
        taskName, caseNum, needSyncNewData, needUpdateCase = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    except Exception as ex:
        print 'use error:\n\t\targv[1]: the name of this task\n\t\targv[2]: the max number of run case\n\t\targv[3]: is need sync new detail data\n\t\targv[4]: is need update case'
    ymt = YeahMobiTask()
    ymt.setTaskCaseNum(taskName)
    ymt.setTaskCaseNum(caseNum)
    ymt.runTask(needSyncNewData, needUpdateCase)
