#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
sys.path.append(os.path.split(os.path.abspath(sys.path[0]))[0])


#  构造跳转数据
import string
from random import randint
from config.setting import *
from ext.util import *


class Constructor(object):

    def __init__(self):
        self.transactionidList = list()
        self.clickdatacount = 0
        self.convdatacount = 0
        self.logger = getLogger()

    @property
    def setClick(self):
        for runtime in range(cycletimes):
            for data in offer_aff_combination:
                offer_id, aff_id = data
                t = string.Template(click_url_template)
                click_url = t.substitute({"offerid":offer_id, "affid":aff_id})
                try:
                    r = requests.get(click_url, headers=headers, allow_redirects=False)
                    if r.status_code != 302:
                        self.logger.error('send click data get a error response code: [{0}]'.format(r.status_code))
                        sys.exit()
                    else:
                        self.clickdatacount += 1
                        self.logger.info('set click data success')
                except Exception as ex:
                    traceback.print_exc()
                else:
                    jumpaddress = r.text
                    transaction_id = get_clickid(jumpaddress)
                    self.transactionidList.append(transaction_id)
        self.logger.info('set click data count: {0}'.format(self.clickdatacount))

    @property
    def setConv(self):
        for tid in self.transactionidList:
            t = string.Template(conv_url_template)
            conv_url = t.substitute({"transactionid":tid})
            if randint(2,2) % 2 == 0:  # 100% percent to mock conversion data
                try:
                    r = requests.get(conv_url)
                    if r.text != "success=true;conversioned":
                        self.logger.error(r.text)
                    else:
                        self.convdatacount += 1
                        self.logger.info('set conv data success')
                except Exception as ex:
                    traceback.print_exc()
        self.logger.info('set click data count: {0}'.format(self.convdatacount))

    @property
    def getTranasctionId(self):
        self.logger.info('set click and conversion data begin')
        self.setClick
        time.sleep(10)
        self.setConv
        self.logger.info('set click and conversion data end')
        datacount = add(self.clickdatacount, self.convdatacount)
        return datacount, self.transactionidList

if __name__ == '__main__':
    c = Constructor()
    c.getTranasctionId