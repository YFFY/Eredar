#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import logging

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

database = {
    "host":"172.20.0.123",
    "port":"3306",
    "user":"robin",
    "password":"111111",
    "databasename":"ym_mysql",
    "table":"ym_druid"
}


format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}

offer_aff_combination = [('90010508', '90010622')]
click_url = "http://172.30.10.146:8080/trace?"