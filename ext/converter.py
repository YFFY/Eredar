#! /usr/bin/env python
# --*-- coding:utf-8 --*--

# 将druid 查询转化为 SQL

from ext.parser import QueryParser
from config.setting import *
from ext.util import get_datatime


class QueryConverter(object):

    def __init__(self):
        pass

    def getSQL(self, druidQuery):
        columnList = list()
        parser = QueryParser(druidQuery)
        sql_list = list()
        sql_list.append("select")

        parser_data = parser.get_data()
        group_data = parser.get_group()
        filter_items = parser.get_filter()
        filterKeys = filter_items.keys()
        order_items = parser.get_sort()
        pagination = parser.get_pagination()

        for group in group_data:
            sql_list.append(group)
            columnList.append(group)
            sql_list.append(',')

        for data in parser_data:
            sql_list.append(DATAMAP.get(data).get("formula"))
            columnList.append(data)
            sql_list.append(',')

        for filterkey in filterKeys:
            if filterkey not in sql_list:
                sql_list.append(filterkey)
                columnList.append(filterkey)
                sql_list.append(',')

        sql_list.pop()

        sql_list.append("from")
        sql_list.append("ym_detail")
        sql_list.append("where")
        sql_list.append("unix_timestamp(time_stamp)")
        sql_list.append("between")
        sql_list.append(str(parser.get_time().get("start") - 28800))
        sql_list.append("and")
        sql_list.append(str(parser.get_time().get("end") - 28800))

        if group_data:
            sql_list.append("group by")
            for group in group_data:
                sql_list.append(group)
                sql_list.append(',')
            sql_list.pop()

        if filter_items:
            sql_list.append("having")
            for filter_key in filterKeys:
                filter_item = filter_items.get(filter_key)
                for filteroperate in filter_item:
                    filtervalue = filter_item.get(filteroperate)
                    if isinstance(filtervalue, list):
                        filtervalue = str(tuple(filtervalue)).replace('u','')
                    else:
                        pass
                    sql_list.append(filter_key)
                    sql_list.append(OPERATEMAP.get(filteroperate))
                    if filteroperate == '$match':
                        filtervalue = "'{0}'".format(filtervalue)
                    else:
                        if filter_key in ("week", "month", "day"):
                            filtervalue = "'{0}'".format(filtervalue)
                        else:
                            filtervalue = str(filtervalue)
                    sql_list.append(filtervalue)
                    sql_list.append('and')
            sql_list.pop()

        if order_items:
            sql_list.append("order by")
            for order_item in order_items:
                sql_list.append(order_item.get("orderBy"))
                sql_list.append(ORDERMAP.get(str(order_item.get("order"))))
                sql_list.append(',')
            sql_list.pop()

        sql_list.append("limit")
        offset = pagination.get('offset', 0)
        page = pagination.get('page')
        size = pagination.get('size')
        if page != 0:
            sql_list.append(str(page * size))
            sql_list.append(',')
            sql_list.append(str((page+1) * size))
        else:
            sql_list.append(str((page+1) * size))
        return columnList, ' '.join(sql_list)

if __name__ == '__main__':
    print QueryConverter().getSQL({"filters":{"$and":{"year":{"$eq":"2015"}}},"sort":[{"orderBy":"conversion","order":-1}],"data":["click","conversion"],"group":["offer_id","aff_manager","year"],"settings":{"return_format":"json","data_source":"ymds_druid_datasource","report_id":"8631614495385992522","pagination":{"page":0,"size":1000000},"time":{"start":1430964811,"end":1430965111,"timezone":0}}})