#! /usr/bin/env python
# --*-- coding:utf-8 --*--


class DataTester(object):

    def __init__(self):
        pass

    def get_case(self):
        return '{"settings":{"time":{"start":1428249600,"end":1428336000,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"convesionLogQuery","pagination":{"size":50,"page":0,"offset":0}},"data":["conversion2"],"group":["day"],"filters":{"$and":{"log_tye":{"$eq":"1"},"status":{"$eq":"Confirmed"},"datasource":{"$neq":"hasoffer"}}}}'

    def get_sql(self):
        pass

    def get_druid_result(self):
        pass

    def get_mysql_result(self):
        pass

    def isPass(self):
        pass
