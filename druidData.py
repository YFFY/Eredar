#! --*-- coding:utf-8 --*--
import MySQLdb
import time
import requests
import json
import urllib2
from  PYtest import *
from idlelib.ReplaceDialog import replace

def extractYMdata(transaction_id):
    
    #url request
    trns_id = transaction_id
    #r=requests.get('http://172.20.0.69:8080/impala/report?report_param={"settings":{"time": {"start":1407744000,"end":1408093200,"timezone":0},"return_format":"json", "report_id":"232sds32322","data_source":"ymds_druid_datasource","pagination":{"size":5,"page":0}},"group":["transaction_id","offer_id","click_ip","conv_ip","click_time","cpa"],"data": ["click"],"filters":{"$and":{"transaction_id":{"$eq":"002b4af5-731e-43f7-aa37-7b523e71d63f"}}},"sort":[]}').text
    #rul = 'http://172.20.0.69:8080/impala/report?report_param={"settings":{"time": {"start":1407744000,"end":1408093200,"timezone":0},"return_format":"json", "report_id":"232sds32322","data_source":"ymds_druid_datasource","pagination":{"size":5,"page":0}},"group":["transaction_id","offer_id","click_ip","conv_ip","click_time","cpa"],"data": ["click"],"filters":{"$and":{"transaction_id":{"$eq":"%s"}}},"sort":[]}'%(trns_id)
    rul = 'http://172.20.0.69:8080/impala/report?report_param={"settings":{"time": {"start":1407744000,"end":1408093200,"timezone":0},"return_format":"json", "report_id":"232sds32322","data_source":"ymds_druid_datasource","pagination":{"size":5,"page":0}},"group":["visitor_node_id","aff_manager","track_type","offer_id","aff_sub6","aff_sub7","aff_sub8","adv_sub3","aff_sub2","adv_sub2","aff_sub3","adv_sub1","aff_sub4","aff_sub5","city","click_ip","device_model","aff_sub1","platform_id","rpa","cpa","log_tye","click_time","adv_id","conv_time","isp","gcname","screen_width","ref_track_site","aff_id","transaction_id","country","expiration_date","mobile_brand","is_unique_click","session_id","device_type","adv_sub7","state","adv_sub6","adv_sub5","adv_sub4","gcid","currency","adv_sub8","ref_track","device_os","browser","conversions","visitor_id","conv_ip","x_forwarded_for","device_brand","type_id","adv_manager","user_agent","screen_height","datasource","request_url","source","matched_format","status","message","year","month","week","day","hour"],"data": ["profit","epc","conversion","arpa","click","acpa","cost","cr","rpc","cpc","unique_click","revenue","rows","conversion2"],"filters":{"$and":{"transaction_id":{"$eq":"%s"}}},"sort":[]}'%(trns_id)
    r=requests.get(rul).text
    s=json.loads(r)
    #get data
    ds = s['data']['data']  
    #print ds
      
    #get dimension name which used to query in mysql as column
    ds1 = str(ds[0])
    ds2 = ds1.replace('u\'','')
    ds3 = ds2.replace('\'','')
    ds4 = ds3[1:-1]
    #print ds4
    #get dimension value to insert in mysql
    dv1 = str(ds[1])
    dv2 = dv1.replace('u\'','\'')
    dv3 = dv2.replace('L','')
    dv4 = dv3[1:-1]
    #print dv4
    #add data to list
    ss = {}
    ss[0] = ds4
    ss[1] = dv4
    
    return ss


def main():
    s = '002b4af5-731e-43f7-aa37-7b523e71d63f'
    re = extractYMdata(s)
    print re[0]
    print re[1]
    #call mysql to query
    test = MySql()
    test.mysqlConnection('ym_mysql')
    test.mysqlInsert2('ym_druid', re[0],re[1])
    
if __name__=='__main__':
    main()
        
