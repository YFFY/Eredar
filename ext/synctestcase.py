#! /usr/bin/env python
# --*-- coding: utf-8 --*--

import os
from databaser import Dber
from util import *


class SyncTestCase(object):

    def __init__(self, casepath):
        self.casePath = casepath
        self.executor = Dber()

    @property
    def getCase(self):
        self.caseList = list()
        if os.path.isdir(self.casePath):
            for f in [os.path.join(self.casePath, caseFile) for caseFile in os.listdir(self.casePath)]:
                with open(f, 'r') as fr:
                    for line in fr:
                        self.caseList.append(line)
        else:
            with open(self.casePath, 'r') as fr:
                for line in fr:
                    self.caseList.append(line)

    @property
    def sync2db(self):
        self.getCase
        for caseindex, case in enumerate(self.caseList):
            casename = 'case_{0}'.format(caseindex+1)
            sql = "insert into ym_case(id, casename, casecontent, createtime) values ('{0}', '{1}', '{2}', '{3}')".format(
                caseindex, casename, case, get_now())
            success = self.executor.executSql(sql)
            if success:
                print 'sync case success'
            else:
                print 'sync case failed'
        self.executor.setCommit()
        self.executor.setColse()

if __name__ == '__main__':
    stc = SyncTestCase(r'C:\Users\jeff.yu\Desktop\cases')
    stc.sync2db