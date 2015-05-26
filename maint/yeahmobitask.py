#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
sys.path.append(os.path.split(os.path.abspath(sys.path[0]))[0])

from datapreparations import *
from datatester import *


class Tasker(object):

    def __init__(self, taskid, taskname, caseidlist, queryNow = True) :
        self.dber = Dber()
        self.dter = DataTester()
        self.dper = SyncData()
        self.logger = getLogger()
        self.caseidlist = caseidlist.split(',')
        self.queryNow = queryNow
        if self.queryNow:
            start, end = get_unixtime_range()
            self.dper.sync(start, end)
            self.updateCase(start, end, self.caseidlist)
        self.taskid = taskid
        self.taskname = taskname
        self.passcount = 0
        self.failcount = 0
        self.getCaseList()

    def updateCase(self, start, end, caseidList):
        for caseid in caseidList:
            updateCaseSql = 'update ym_case set start_time_of_case="{0}", end_time_of_case="{1}" where caseid = {2}'.format(start, end, caseid)
            self.dber.executSql(updateCaseSql)
            self.dber.setCommit()
        self.logger.info('update case success, change start and end time of case to now')

    def getTaskId(self):
        return self.taskid

    def getTaskName(self):
        return self.taskname

    def getCaseIdList(self):
        return self.caseidlist

    def getCaseList(self):
        self.caseList = list()
        getCaseSql = 'select casename, start_time_of_case, end_time_of_case, casecontent from ym_case where caseid = {0}'
        for caseid in self.caseidlist:
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
                self.logger.info('can not find case by caseid : {0} skip it'.format(caseid))
        self.logger.info('get yeahmobi report case success')

    def runTask(self):
        setCache()
        self.logger.info('get task success. taskid: {0} task name: {1} caseid of task: {2}'.format(self.taskid, self.taskname, self.caseidlist))
        taskflag = getTaskFlag()
        for case in self.caseList:
            caseid = case.get('caseid')
            casename = case.get('casename')
            case = case.get('casecontent') % (int(case.get('start_time_of_case')), int(case.get('end_time_of_case')))
            resultInfo = self.dter.runCase(case)
            isPass = resultInfo.get('isPass')
            druid_result = resultInfo['druid_result']
            druid_query = resultInfo['druid_query']
            mysql_query = resultInfo['mysql_query']
            mysql_result = resultInfo['mysql_result']
            if isPass:
                self.passcount += 1
                detailResult = "success"
                self.logger.info('run case_id: {0} {1}'.format(caseid, detailResult))
            else:
                self.failcount += 1
                detailResult = "failed"
                self.logger.info('run case_id [{0}] [{1}] druid_query: [{2}] mysql_query: [{3}]'.format(
                    caseid, detailResult, druid_query, mysql_query
                ))
            syncDetailResultSql = """insert into ym_detail_result(taskid, caseid, result, druid_result, druid_query, mysql_query, mysql_result, run_time, taskflag) values ({0}, {1}, "{2}", "{3}", '{4}', "{5}", "{6}", "{7}", "{8}")""".format(
                self.taskid, caseid, detailResult, druid_result, druid_query, mysql_query, mysql_result, get_now(), taskflag
            )
            self.dber.executSql(syncDetailResultSql)
            # time.sleep(5)
        if self.failcount == 0 and self.passcount != 0:
            taskResult = 'success'
        else:
            taskResult = 'failed'
        syncTaskResultSql = 'insert into ym_task_result(taskid, passcount, failcount, taskresult, runtime, taskflag) values({0}, {1}, {2}, "{3}", "{4}", "{5}")'.format(
            self.taskid, self.passcount, self.failcount, taskResult, get_now(), taskflag
        )
        self.dber.executSql(syncTaskResultSql)
        self.dber.setCommit()
        self.dber.setColse()


def taskCenter():

    dber = Dber()
    logger = getLogger()
    taskTuple = dber.getRecord('select taskid, taskname, caselist, isrealtime from ym_task', True)
    for task in taskTuple:
        taskid, taskname, caselist, isrealtime = task[0], task[1], task[2], task[3]
        if isrealtime == 'no':
            isrealtime = False
            message = "so we don't construct new data"
        else:
            isrealtime = True
            message = "so we construct new data"
        logger.info('get task: {0}, isrealtime: {1}, {2}'.format(taskname, isrealtime, message))
        time.sleep(5)
        tasker = Tasker(taskid, taskname, caselist, isrealtime)
        tasker.runTask()

if __name__ == '__main__':
    taskCenter()





