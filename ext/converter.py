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
            sql_list.append(',')

        for data in parser_data:
            sql_list.append(DATAMAP.get(data).get("formula"))
            sql_list.append(',')

        for filterkey in filterKeys:
            sql_list.append(filterkey)
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
                    sql_list.append(filtervalue)
                    sql_list.append('and')
            sql_list.pop()

        if order_items:
            sql_list.append("order by")
            for order_item in order_items:
                sql_list.append(order_item.get("orderBy"))
                sql_list.append(ORDERMAP.get(str(order_item.get("order"))))

        sql_list.append("limit")
        offset = pagination.get('offset', 0)
        if not offset:
            offset = 0
        size = pagination.get('size')
        if offset != 0:
            sql_list.append(offset)
            sql_list.append(size - offset)
        else:
            sql_list.append(str(size))
        return ' '.join(sql_list)

if __name__ == '__main__':
    pass