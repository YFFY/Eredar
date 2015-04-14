#! --*-- coding:utf-8 --*--
import MySQLdb
import time
import requests
import json
import urllib2
from  PYtest import *
from idlelib.ReplaceDialog import replace

def extractYMdata(transaction_id):

    for itransaction_id in transaction_id:
        #remove 'u' 
        trns_id = itransaction_id.replace('u\'','\'')
        print trns_id
        #call url request
        rul = 'http://172.20.0.123:8080/impala/report?report_param={"settings":{"time": {"start":1428681600,"end":1447171200,"timezone":0},"return_format":"json", "report_id":"232sds32322","data_source":"ymds_druid_datasource","pagination":{"size":5,"page":0}},"group":["visitor_node_id","aff_manager","track_type","offer_id","aff_sub6","aff_sub7","aff_sub8","adv_sub3","aff_sub2","adv_sub2","aff_sub3","adv_sub1","aff_sub4","aff_sub5","city","click_ip","device_model","aff_sub1","platform_id","rpa","cpa","log_tye","click_time","adv_id","conv_time","isp","gcname","screen_width","ref_track_site","aff_id","transaction_id","country","expiration_date","mobile_brand","is_unique_click","session_id","device_type","adv_sub7","state","adv_sub6","adv_sub5","adv_sub4","gcid","currency","adv_sub8","ref_track","device_os","browser","conversions","visitor_id","conv_ip","x_forwarded_for","device_brand","type_id","adv_manager","user_agent","screen_height","datasource","request_url","source","matched_format","status","message","year","month","week","day","hour"],"data": ["profit","epc","conversion","arpa","click","acpa","cost","cr","rpc","cpc","unique_click","revenue","rows","conversion2"],"filters":{"$and":{"transaction_id":{"$eq":"%s"}}},"sort":[]}'%(trns_id)
        r=requests.get(rul).text
        s=json.loads(r)
        print s
        #extract name of dimension 
        ds = s['data']['data']  
        #get dimension name which used to query in mysql as column
        dimensionName = (((str(s['data']['data'][0])).replace('u\'','')).replace('\'',''))[1:-1]
        #print ds4
        #get dimension value to insert in mysql
        dimensionData = (((str(s['data']['data'][1])).replace('u\'','\'')).replace('L',''))[1:-1]
        #print dv4
        #add data to list        
        test = MySql()
        test.mysqlConnection('ym_mysql')
        test.mysqlInsert2('ym_druid', dimensionName,dimensionData)      

def main():
    s = ['ce11e71f-c985-4c61-b9d7-6003daa497e0', '6cce346c-7461-4742-a336-208b9fa35eac'] 
    extractYMdata(s)
 
    
if __name__=='__main__':
    main()
        
