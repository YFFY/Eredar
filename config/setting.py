#! /usr/bin/env python
# --*-- coding:utf-8 --*--



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
    "formula" : "(sum(revenue) - sum(cost)) as profit",
    "level" : 2,
    "precision" : 3
  },
  "epc" : {
    "alisa" : "epc",
    "name" : "(cost/click)",
    "formula" : "sum(cost) / sum(click) as epc",
    "level" : 2,
    "precision" : 3
  },
  "conversion" : {
    "alisa" : "conversion",
    "name" : "sum(conversion)",
    "formula" : "sum(conversion) as conversion",
    "level" : 1,
    "precision" : 0
  },
  "arpa" : {
    "alisa" : "arpa",
    "name" : "(revenue/conversion)",
    "formula" : "sum(revenue) / sum(conversion) as arpa",
    "level" : 2,
    "precision" : 2
  },
  "click" : {
    "alisa" : "click",
    "name" : "sum(click)",
    "formula" : "sum(click) as click",
    "level" : 1,
    "precision" : 0
  },
  "acpa" : {
    "alisa" : "acpa",
    "name" : "(cost/conversion)",
    "formula" : "sum(cost) / sum(conversion) as acpa",
    "level" : 2,
    "precision" : 2
  },
  "cost" : {
    "alisa" : "cost",
    "name" : "sum(cost)",
    "formula" : "sum(cost) as cost",
    "level" : 1,
    "precision" : 3
  },
  "cr" : {
    "alisa" : "cr",
    "name" : "(conversion/click)",
    "formula" : "sum(conversion) / sum(click) as cr",
    "level" : 2,
    "precision" : 4
  },
  "rpc" : {
    "alisa" : "rpc",
    "name" : "(revenue/click)",
    "formula" : "sum(revenue) / sum(click) as rpc",
    "level" : 2,
    "precision" : 3
  },
  "cpc" : {
    "alisa" : "cpc",
    "name" : "(cost/click)",
    "formula" : "sum(cost) / sum(click) as cpc",
    "level" : 2,
    "precision" : 3
  },
  "unique_click" : {
    "alisa" : "unique_click",
    "name" : "sum(unique_click)",
    "formula" : "sum(unique_click) as unique_click",
    "level" : 1,
    "precision" : 0
  },
  "revenue" : {
    "alisa" : "revenue",
    "name" : "sum(revenue)",
    "formula" : "sum(revenue) as revenue",
    "level" : 1,
    "precision" : 3
  },
  "rows" : {
    "alisa" : "rows",
    "name" : "sum(rows)",
    "formula" : "sum(*) as rows",
    "level" : 1,
    "precision" : 0
  },
  "conversion2" : {
    "alisa" : "conversion2",
    "name" : "sum(conversion2)",
    "formula" : "sum(conversion2) as conversion2",
    "level" : 1,
    "precision" : 0
  }
}

sync_sql = "insert into {0}{1} values {2}"


# 数据库配置
database = {
    "host":"172.20.0.123",
    "port":3306,
    "user":"robin",
    "password":"111111",
    "databasename":"ym_mysql",
    "detail_table":"ym_detail",
    "case_table": "ym_case"
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
cycletimes = 1       #  data sum = cycletimes * len(offer_aff_combination)


# Druid明细查询
query_url = 'http://172.20.0.92:8080/impala/report?report_param='
param_template = '{"settings":{"report_id":"111111111111","process_type":"druid","return_format":"json","data_source":"ymds_druid_datasource","time":{"start":%d,"end":%d,"timezone":0},"pagination":{"size":100000,"page":0}},"data":["profit","epc","conversion","arpa","click","acpa","cost","cr","rpc","cpc","unique_click","revenue","rows","conversion2"],"filters":{"$and":{"transaction_id":{"$in":%s}}},"group":["aff_id", "aff_manager", "aff_sub1", "aff_sub2", "aff_sub3", "aff_sub4", "aff_sub5", "aff_sub6", "aff_sub7", "aff_sub8", "adv_id", "adv_manager", "adv_sub1", "adv_sub2", "adv_sub3", "adv_sub4", "adv_sub5", "adv_sub6", "adv_sub7", "adv_sub8", "offer_id", "rpa", "cpa", "ref_track", "ref_track_site", "click_ip", "conv_ip", "transaction_id", "click_time", "conv_time", "user_agent", "browser", "device_brand", "device_model", "device_os", "device_type", "country", "time_stamp", "log_tye", "visitor_id", "x_forwarded_for", "state", "city", "isp", "mobile_brand", "platform_id", "screen_width", "screen_height", "conversions", "track_type", "session_id", "visitor_node_id", "expiration_date", "is_unique_click", "gcid", "gcname", "browser_name", "device_brand_name", "device_model_name", "platform_name", "device_type_name", "os_ver_name", "os_ver", "datasource", "source", "request_url", "matched_format", "status", "message", "year", "month", "week", "day", "hour"]}'


# 同步数据配置
sync_start = 1429228800
sync_end = 1429315200


# 测试配置
countNum = 1  #运行的case个数，-1 则取sys.argv[1]