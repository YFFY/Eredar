#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from datapreparations import *
from datatester import *


class YeahMobiTask(object):

    def __init__(self, taskid, taskname, caseidlist, queryNow = True) :
        self.dber = Dber()
        self.dter = DataTester()
        self.dper = SyncData()
        self.logger = getLogger()
        self.queryNow = queryNow
        if self.queryNow:
            start, end = get_unixtime_range()
            self.dper.sync(start, end)
            self.updateCase()
        self.taskid = taskid
        self.taskname = taskname
        self.caseidlist = caseidlist
        self.passcount = 0
        self.failcount = 0
        self.getCaseList()

    def updateCase(self):
        unix_range = get_unixtime_range()
        start, end = unix_range[0], unix_range[1]
        updateCaseSql = 'update ym_case set start_time_of_case="{0}", end_time_of_case="{1}"'.format(start, end)
        self.logger.info('update case sql : {0}'.format(updateCaseSql))
        self.dber.executSql(updateCaseSql)
        self.dber.setCommit()
        self.logger.info('update case success')


    def getTaskId(self):
        return self.taskid

    def getTaskName(self):
        return self.taskname

    def getCaseIdList(self):
        return self.caseidlist

    def getCaseList(self):
        self.caseList = list()
        getCaseSql = 'select casename, start_time_of_case, end_time_of_case, casecontent from ym_case where caseid = {0}'
        for caseid in self.caseidlist.split(','):
            caseMap = dict()
            self.logger.info(getCaseSql.format(caseid))
            caseinfo = self.dber.getRecord(getCaseSql.format(caseid))
            caseMap['caseid'] = caseid
            caseMap['casename'] = caseinfo[0]
            caseMap['start_time_of_case'] = caseinfo[1]
            caseMap['end_time_of_case'] = caseinfo[2]
            caseMap['casecontent'] = caseinfo[3]
            self.caseList.append(caseMap)

    def runTask(self):
        self.logger.info('get task success. taskid: {0} task name: {1} caseid of task: {2}'.format(self.taskid, self.taskname, self.caseidlist))
        for case in self.caseList:
            caseid = case.get('caseid')
            casename = case.get('casename')
            case = case.get('casecontent') % (int(case.get('start_time_of_case')), int(case.get('end_time_of_case')))
            self.logger.info('get case: {0} query: {1}'.format(casename, case))
            resultInfo = self.dter.runCase(case)
            isPass = resultInfo.get('isPass')
            druid_result = resultInfo['druid_result']
            druid_query = resultInfo['druid_query']
            mysql_query = resultInfo['mysql_query']
            mysql_result = resultInfo['mysql_result']
            if isPass:
                self.passcount += 1
            else:
                self.failcount += 1
            syncDetailResultSql = "insert into ym_detail_result(taskid, caseid, druid_result, druid_query, mysql_query, mysql_result, run_time) values ({0}, {1}, '{2}', '{3}', '{4}', '{5}', '{6}')".format(
                self.taskid, caseid, druid_result, druid_query, mysql_query, mysql_result, get_now()
            )
            self.dber.executSql(syncDetailResultSql)
        if self.failcount == 0 and self.passcount != 0:
            taskResult = 'success'
        else:
            taskResult = 'failed'
        syncTaskResultSql = 'insert into ym_task_result(taskid, passcount, failcount, taskresult, runtime) values({0}, {1}, {2}, "{3}", "{4}")'.format(
            self.taskid, self.passcount, self.failcount, taskResult, get_now()
        )
        self.dber.executSql(syncTaskResultSql)
        self.dber.setCommit()
        self.dber.setColse()

if __name__ == '__main__':
    ymt = YeahMobiTask('1', 'task001', '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149')
    ymt.runTask()





