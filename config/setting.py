#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from random import choice, randint

# SQL 配置
OPERATEMAP = {
    "$eq":"=",
    "$neq":"<>",
    "$gt":">",
    "$gte":">=",
    "$lt":"<",
    "$lte":"<=",
    "$nin":"not in",
    "$in":"in",
    "$match":"like"
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
    "formula" : "round(sum(revenue) - sum(cost), 3) as profit",
    "level" : 2,
    "precision" : 3
  },
  "epc" : {
    "alisa" : "epc",
    "name" : "(cost/click)",
    "formula" : "round(sum(cost) / sum(click),3) as epc",
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
    "formula" : "round(sum(revenue) / sum(conversion),2) as arpa",
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
    "formula" : "round(sum(cost) / sum(conversion),2) as acpa",
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
    "formula" : "round(sum(conversion) / sum(click),4) as cr",
    "level" : 2,
    "precision" : 4
  },
  "rpc" : {
    "alisa" : "rpc",
    "name" : "(revenue/click)",
    "formula" : "round(sum(revenue) / sum(click),3) as rpc",
    "level" : 2,
    "precision" : 3
  },
  "cpc" : {
    "alisa" : "cpc",
    "name" : "(cost/click)",
    "formula" : "round(sum(cost) / sum(click),3) as cpc",
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
offer_aff_combination = [(200044,90010409),
                         (200044,90010409),
                         (200044,90010409),
                         (200044,90010409),
                         (200044,90010409),
                         (200105,90010409),
                         (200105,90010409),
                         (200105,90010409),
                         (200105,90010409),
                         (200045,90010409),
                         (200045,90010409),
                         (200045,90010409),
                         (200106,90010409),
                         (200106,90010409),
                         (200002,90010409)]
click_url_template = "http://172.30.10.207:8080/ymtrace/trace?offer_id=$offerid&aff_id=$affid&aff_sub=affsub1&aff_sub2=affsub2&aff_sub3=affsub3&aff_sub4=affsub4&aff_sub5=affsub5&aff_sub6=affsub6&aff_sub7=affsub7&aff_sub8=affsub8"
conv_url_template = "http://172.30.10.207:8080/ymtrace/conv?transaction_id=$transactionid&adv_sub=advsub1&adv_sub2=advsub2&adv_sub3=advsub3&adv_sub4=advsub4&adv_sub5=advsub5&adv_sub6=advsub6&adv_sub7=advsub7&adv_sub8=advsub8"


headers =  {"Host": "net.tutsplus.com",
           "User-Agent": choice(['Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5',
                                'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                                'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                                'JUC (Linux; U; 2.3.7; zh-cn; MB200; 320*480) UCWEB7.9.3.103/139/999',
                                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1',
                                'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
                                'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
                                'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3',
                                'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
                                'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
                                'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
                                'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7']),
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us,en;q=0.5",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
           "Keep-Alive": "300",
           "Connection": "keep-alive",
           "Cookie": "PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120",
           "Pragma": "no-cache",
           "Cache-Control": "no-cache"}
cycletimes = 1


# Druid明细查询
query_url = 'http://172.20.0.164:8080/impala/report?report_param='
param_template = '{"settings":{"report_id":"111111111111","process_type":"druid","return_format":"json","data_source":"ymds_druid_datasource","time":{"start":%d,"end":%d,"timezone":0},"pagination":{"size":100000,"page":0}},"data":["profit","epc","conversion","arpa","click","acpa","cost","cr","rpc","cpc","unique_click","revenue","rows","conversion2"],"filters":{"$and":{"transaction_id":{"$in":%s},"offer_id":{"$neq":"-1"}}},"group":["aff_id", "aff_manager", "aff_sub1", "aff_sub2", "aff_sub3", "aff_sub4", "aff_sub5", "aff_sub6", "aff_sub7", "aff_sub8", "adv_id", "adv_manager", "adv_sub1", "adv_sub2", "adv_sub3", "adv_sub4", "adv_sub5", "adv_sub6", "adv_sub7", "adv_sub8", "offer_id", "rpa", "cpa", "ref_track", "ref_track_site", "click_ip", "conv_ip", "transaction_id", "click_time", "conv_time", "user_agent", "browser", "device_brand", "device_model", "device_os", "device_type", "country", "time_stamp", "log_tye", "visitor_id", "x_forwarded_for", "state", "city", "isp", "mobile_brand", "platform_id", "screen_width", "screen_height", "conversions", "track_type", "session_id", "visitor_node_id", "expiration_date", "is_unique_click", "gcid", "gcname", "os_ver", "datasource", "source", "request_url", "matched_format", "status", "message", "year", "month", "week", "day", "hour"]}'
unix_end_offset_seconds = 300
timewaitquerydetail = 300  # wait data flow to druid

# 测试配置
detailresultinfo = {
    "isPass" : False,
    "druid_result": "",
    "druid_query": "",
    "mysql_result": "",
    "mysql_query": ""
}

machineList = [
    ('172.30.10.207', 8080),         # VN
    ('172.30.10.209', 8080),         # CC
    ('172.20.0.35', 18085),          # collector
    ('172.20.0.172', 9092),          # kafka
    ('172.20.0.186', 8080),          # realtime
    ('172.20.0.189', 8080),          # realtime
    ('172.20.0.190', 8080),          # coor
    ('172.20.0.172', 2181),          # zk
    ('172.20.0.186', 2181),          # zk
    ('172.20.0.189', 2181),          # zk
    ('172.20.0.164', 8080),          # realquery
    ('172.20.0.190', 9092)           # h2
]

cachecmd = """curl http://172.20.0.164:8080/impala/cache -X POST -H 'content-type: application/json' -d '{"enableL1":false,"enableL2":false,"clearL1":false,"clearL2":false,"maxCapacityL2":10003,"timeUnit":300}'"""
routercmd = """curl http://172.20.0.51:8080/datasystem-druid-router/impala_platform -X POST -H 'content-type: text/plain'  -d '{"datasources":{"ymds_druid_datasource": "DRUID","ndpsearch":"IMPALA"}}'"""