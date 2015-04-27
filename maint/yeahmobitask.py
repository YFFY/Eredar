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
            caseinfo = self.dber.getRecord(getCaseSql.format(caseid), False)
            try:
                caseMap['caseid'] = caseid
                caseMap['casename'] = caseinfo[0]
                caseMap['start_time_of_case'] = caseinfo[1]
                caseMap['end_time_of_case'] = caseinfo[2]
                caseMap['casecontent'] = caseinfo[3].strip()
                self.caseList.append(caseMap)
            except Exception as ex:
                self.logger.info('can not find caseid : {0} skip it'.format(caseid))
        self.logger.info('get yeahmobi report case success')

    def runTask(self):
        self.logger.info('get task success. taskid: {0} task name: {1} caseid of task: {2}'.format(self.taskid, self.taskname, self.caseidlist))
        for case in self.caseList:
            caseid = case.get('caseid')
            casename = case.get('casename')
            case = case.get('casecontent') % (int(case.get('start_time_of_case')), int(case.get('end_time_of_case')))
            self.logger.info('get druid case: {0} {1}'.format(casename, case))
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
            syncDetailResultSql = """insert into ym_detail_result(taskid, caseid, druid_result, druid_query, mysql_query, mysql_result, run_time) values ({0}, {1}, "{2}", '{3}', "{4}", "{5}", "{6}")""".format(
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
    ymt = YeahMobiTask('1', 'task001', ','.join([str(i) for i in range(142)]), False)
    ymt.runTask()





