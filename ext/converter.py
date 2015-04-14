#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from ext.parser import QueryParser
from config.setting import *
from ext.util import get_datatime


class QueryConverter(object):

    def __init__(self):
        pass

    def getSQL(self, druidQuery):
        parser = QueryParser(druidQuery)
        sql_list = list()
        sql_list.append("select")

        parser_data = parser.get_data()
        group_data = parser.get_group()

        for data in parser_data:
            sql_list.append(DATAMAP.get(data).get("formula"))
            sql_list.append(',')

        for group in group_data:
            sql_list.append(group)
            sql_list.append(',')
        sql_list.pop()

        sql_list.append("from")
        sql_list.append("ymds_mysql_datasource")
        sql_list.append("where")
        sql_list.append("time")
        sql_list.append("between")
        sql_list.append(get_datatime(parser.get_time().get("start")))
        sql_list.append("and")
        sql_list.append(get_datatime(parser.get_time().get("end")))


        if group_data:
            sql_list.append("group by")
            for group in group_data:
                sql_list.append(group)

        filter_items = parser.get_filter()
        if filter_items:
            sql_list.append("having")
            for filter_key in filter_items:
                operate_item = filter_items.get(filter_key)
                for operate in operate_item:
                    sql_list.append('{0} {1} "{2}"'.format(filter_key, OPERATEMAP.get(operate), operate_item.get(operate)))
                    sql_list.append('and')
        sql_list.pop()
        order_items = parser.get_sort()
        if order_items:
            sql_list.append("order by")
            for order_item in order_items:
                sql_list.append(order_item.get("orderBy"))
                sql_list.append(ORDERMAP.get(order_item.get("order")))

        sql_list.append("limit")
        offset = parser.get_pagination().get("offset")
        sql_list.append("0")
        if offset != 0:
            sql_list.append(offset)
        else:
            sql_list.append(str(parser.get_pagination().get("size")))

        print sql_list
        return ' '.join(sql_list)

if __name__ == '__main__':
    converter = QueryConverter()
    sql = converter.getSQL({"settings":{"time":{"start":1428249600,"end":1428336000,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"convesionLogQuery","pagination":{"size":50,"page":0,"offset":0}},"data":["conversion2"],"group":["day"],"filters":{"$and":{"log_tye":{"$eq":"1"},"status":{"$eq":"Confirmed"},"datasource":{"$neq":"hasoffer"}}}})
    print sql