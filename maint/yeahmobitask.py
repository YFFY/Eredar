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
        if isinstance(int(caseNum), int):
            for caseid in range(caseNum):
                ymresultsql = 'insert into ym_result(taskid, caseid) values("{0}", "{1}")'.format(
                    taskId, caseid
                )
                self.executor.executSql(ymresultsql)
        self.executor.setColseCommit()

    @property
    def runTask(self):
        self.sync2db()
        for index in range(caseNum):
            dt = DataTester(index)
            resultinfo = dt.isPass
            logger.info('test:{0} case:{1} durid_result:{2} mysql_result:{3}'.format(countindex+1, resultinfo.get('result'), resultinfo.get('druid_result'), resultinfo.get('mysql_result')))




if __name__ == '__main__':
    try:
        taskName, caseNum = sys.argv[1], sys.argv[2]
    except Exception as ex:
        print 'use error:\n\t\targv[1]: the name of this task\n\t\targv[2]: the max number of run case'
    ymt = YeahMobiTask()
    ymt.setTaskCaseNum(taskName)
    ymt.setTaskCaseNum(caseNum)
    ymt.runTask
