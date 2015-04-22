#! /usr/bin/env python
# --*-- coding:utf-8 --*--

#解析druid查询语句

import json


class QueryParser(object):

    def __init__(self, druidQuery):
        self.druidQuery = druidQuery
        self.get_json()

    def get_json(self):

        if isinstance(self.druidQuery, dict):
            self.jsonQuery = self.druidQuery
        else:
            try:
                self.jsonQuery = json.loads(self.druidQuery)
            except Exception as ex:
                raise ex

    def get_time(self):
        return self.jsonQuery.get('settings').get('time')

    def get_pagination(self):
        return self.jsonQuery.get('settings').get('pagination')

    def get_data(self):
        return self.jsonQuery.get('data')

    def get_group(self):
        return self.jsonQuery.get('group')

    def get_filter(self):
        return self.jsonQuery.get('filters').get("$and")

    def get_sort(self):
        return self.jsonQuery.get('sort')

if __name__ == '__main__':
    print QueryParser({"filters":{"$and":{"cr":{"$eq":0}},"sort":[],"data":["cr"],"group":["aff_id","offer_id"],"settings":{"return_format":"json","data_source":"ymds_druid_datasource","report_id":"8631614495385992522","pagination":{"page":0,"size":1000000},"time":{"start":1429691985,"end":1429720785,"timezone":0}}}}).get_pagination()