#! --*-- coding:utf-8 --*--
import MySQLdb
import time

class MySql(object):  
    def __init__(self):  
        pass
   
    def mysqlConnection(self,dbName):
        try:
            self.conn=MySQLdb.connect(host='172.20.0.123',
                                 user='robin',
                                 passwd='111111',
                                 use_unicode = True,
                                 charset = "utf8",
                                 db=dbName,
                                 port=3306)
        except Exception, e:  
            print e  
            raise Exception("failed to connect to DB server")  
   
    def mysqlDelete(self, sql):  
        self.cursor = self.conn.cursor()  
        self.cursor.execute(sql) 
        self.conn.commit()  
        self.cursor.close()  
    
    def mysqlInsert(self, tableName, sqlmap):  
        self.cursor = self.conn.cursor()  
        dimensionKey = ''
        dimensionValue = ''
        dimensionIndex = 1 
        
        for key in sqlmap.keys():
            dimensionKey = dimensionKey + key
            dimensionValue = dimensionValue + '"'+ str(sqlmap[str(key)]) + '"'
            if dimensionIndex < len(sqlmap):
                dimensionKey = dimensionKey + ','
                dimensionValue = dimensionValue + ','
            dimensionIndex += 1
        sql = 'insert into %s(%s) values(%s)'%(tableName,dimensionKey,dimensionValue)
        
        print sql
        self.cursor.execute(sql) 
        self.conn.commit()  
        self.cursor.close()  
   
    def mysqlInsert2(self, tableName, groupname,groupvalue):  
        self.cursor = self.conn.cursor()  
        sql = 'insert into %s(%s) values(%s)'%(tableName,groupname,groupvalue)        
        print sql
        self.cursor.execute(sql) 
        self.conn.commit()  
        self.cursor.close()  
   
    def mysqlQuery(self, sql):  
        self.cursor = self.conn.cursor()  
        self.cursor.execute(sql)
        qres = self.cursor.fetchall() 
        self.cursor.close()  
        return qres
      
    def mysqlClose(self):  
        self.conn.close()  

def getTimeStampdruid():
    ISOTIMEFORMAT='%Y-%m-%dT%XZ'
    return time.strftime(ISOTIMEFORMAT, time.localtime())

def getTimeStampmysql():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    return time.strftime(ISOTIMEFORMAT, time.localtime())
        
def main():
    test = MySql()
    test.mysqlConnection('ym_mysql')
    i = 0 
    while i < 50:
        sqlmap = {'offer_id':i,'aff_sub1':'supermarket4','click_time':str(getTimeStampmysql()) }
        test.mysqlInsert('ym_druid', sqlmap)
        time.sleep(0.1)
    result = test.mysqlQuery('select offer_id,aff_sub1,click_time from ym_mysql')
    print result

    test.mysqlClose()
    
if __name__=='__main__':
    main()
        
