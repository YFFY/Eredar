#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import logging


# SQL 配置
OPERATEMAP = {
    "$eq":"=",
    "$neq":"<>",
    "$gt":">",
    "$gte":">=",
    "lt":"<",
    "lte":"<=",
}

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

ORDERMAP = {
    "1":"asc",
    "-1":"desc"
}

DATAMAP = {
  "profit" : {
    "alisa" : "profit",
    "name" : "(revenue-cost)",
    "formula" : "(count(revenue) - count(cost)) as profit",
    "level" : 2,
    "precision" : 3
  },
  "epc" : {
    "alisa" : "epc",
    "name" : "(cost/click)",
    "formula" : "count(cost) / count(click) as epc",
    "level" : 2,
    "precision" : 3
  },
  "conversion" : {
    "alisa" : "conversion",
    "name" : "count(conversion)",
    "formula" : "count(conversion) as conversion",
    "level" : 1,
    "precision" : 0
  },
  "arpa" : {
    "alisa" : "arpa",
    "name" : "(revenue/conversion)",
    "formula" : "count(revenue) / count(conversion) as arpa",
    "level" : 2,
    "precision" : 2
  },
  "click" : {
    "alisa" : "click",
    "name" : "count(click)",
    "formula" : "count(click) as click",
    "level" : 1,
    "precision" : 0
  },
  "acpa" : {
    "alisa" : "acpa",
    "name" : "(cost/conversion)",
    "formula" : "count(cost) / count(conversion) as acpa",
    "level" : 2,
    "precision" : 2
  },
  "cost" : {
    "alisa" : "cost",
    "name" : "count(cost)",
    "formula" : "count(cost) as cost",
    "level" : 1,
    "precision" : 3
  },
  "cr" : {
    "alisa" : "cr",
    "name" : "(conversion/click)",
    "formula" : "count(conversion) / count(click) as cr",
    "level" : 2,
    "precision" : 4
  },
  "rpc" : {
    "alisa" : "rpc",
    "name" : "(revenue/click)",
    "formula" : "count(revenue) / count(click) as rpc",
    "level" : 2,
    "precision" : 3
  },
  "cpc" : {
    "alisa" : "cpc",
    "name" : "(cost/click)",
    "formula" : "count(cost) / count(click) as cpc",
    "level" : 2,
    "precision" : 3
  },
  "unique_click" : {
    "alisa" : "unique_click",
    "name" : "count(unique_click)",
    "formula" : "count(unique_click) as unique_click",
    "level" : 1,
    "precision" : 0
  },
  "revenue" : {
    "alisa" : "revenue",
    "name" : "count(revenue)",
    "formula" : "count(revenue) as revenue",
    "level" : 1,
    "precision" : 3
  },
  "rows" : {
    "alisa" : "rows",
    "name" : "count(rows)",
    "formula" : "count(*) as rows",
    "level" : 1,
    "precision" : 0
  },
  "conversion2" : {
    "alisa" : "conversion2",
    "name" : "count(conversion2)",
    "formula" : "count(conversion2) as conversion2",
    "level" : 1,
    "precision" : 0
  }
}


# 数据库配置
database = {
    "host":"172.20.0.123",
    "port":3306,
    "user":"robin",
    "password":"111111",
    "databasename":"ym_mysql",
    "tablename":"ymdetaildata"
}


# 日志配置
format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}


# 跳转数据配置
offer_aff_combination = [(200002, 90010409), (200044,90010409), (200045,90010409),
                         (200105, 90010409), (200106,90010409), (200002,90010409)]
click_url_template = "http://172.30.10.146:8080/trace?offer_id=$offerid&aff_id=$affid&aff_sub=affsub1&aff_sub2=affsub2&aff_sub3=affsub3&aff_sub4=affsub4&aff_sub5=affsub5&aff_sub6=affsub6&aff_sub7=affsub7&aff_sub8=affsub8"
conv_url_template = "http://172.30.10.146:8080/conv?transaction_id=$transactionid&adv_sub=advsub1&adv_sub2=advsub2&adv_sub3=advsub3&adv_sub4=advsub4&adv_sub5=advsub5&adv_sub6=advsub6&adv_sub7=advsub7&adv_sub8=advsub8"


headers = {"Host": "net.tutsplus.com",
           "User-Agent": 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5',
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us,en;q=0.5",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
           "Keep-Alive": "300",
           "Connection": "keep-alive",
           "Cookie": "PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120",
           "Pragma": "no-cache",
           "Cache-Control": "no-cache"}
cycletimes = 1       #  data count = cycletimes * len(offer_aff_combination)


# Druid Detail Query
query_url = 'http://172.20.0.92:8080/impala/report?report_param='
param_template = '{"settings":{"report_id":"111111111111","process_type":"druid","return_format":"json","data_source":"ymds_druid_datasource","time":{"start":%d,"end":%d,"timezone":0},"pagination":{"size":100000,"page":0}},"data":["profit","epc","conversion","arpa","click","acpa","cost","cr","rpc","cpc","unique_click","revenue","rows","conversion2"],"filters":{"$and":{"transaction_id":{"$in":%s}}},"group":["aff_id", "aff_manager", "aff_sub1", "aff_sub2", "aff_sub3", "aff_sub4", "aff_sub5", "aff_sub6", "aff_sub7", "aff_sub8", "adv_id", "adv_manager", "adv_sub1", "adv_sub2", "adv_sub3", "adv_sub4", "adv_sub5", "adv_sub6", "adv_sub7", "adv_sub8", "offer_id", "rpa", "cpa", "ref_track", "ref_track_site", "ref_conv_track", "click_ip", "conv_ip", "transaction_id", "click_time", "conv_time", "time_diff", "user_agent", "browser", "device_brand", "device_model", "device_os", "device_type", "country", "time_stamp", "log_tye", "visitor_id", "x_forwarded_for", "state", "city", "isp", "mobile_brand", "platform_id", "screen_width", "screen_height", "type_id", "conversions", "track_type", "session_id", "visitor_node_id", "expiration_date", "is_unique_click", "gcid", "gcname", "browser_name", "device_brand_name", "device_model_name", "platform_name", "device_type_name", "os_ver_name", "os_ver", "datasource", "source", "request_url", "matched_format", "status", "message", "client_ip"]}'
