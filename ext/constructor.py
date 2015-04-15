#! /usr/bin/env python
# --*-- coding:utf-8 --*--

#  构造跳转数据
import string
from config.setting import *
from ext.util import *


class Constructor(object):

    def __init__(self):
        self.transactionidList = list()
        logname = getLogPath('constructor.log')
        self.logger = Logger(logname, 1, 'root').getlog()

    @property
    def setClickConv(self):
        for runtime in range(cycletimes):
            for data in offer_aff_combination:
                offer_id, aff_id = data
                t = string.Template(click_url_template)
                click_url = t.substitute({"offerid":offer_id, "affid":aff_id})
                try:
                    r = requests.get(click_url, allow_redirects=False)
                except Exception as ex:
                    self.logger.error(ex)
                else:
                    jumpaddress = r.text
                    transaction_id = get_clickid(jumpaddress)
                    t = string.Template(conv_url_template)
                    conv_url = t.substitute({"transactionid":transaction_id})
                    r = requests.get(conv_url)
                    if r.text == 'success=true;conversioned':
                        self.logger.info('data structure success:{0}'.format(transaction_id))
                        self.transactionidList.append(transaction_id)
                    else:
                        self.logger.error('{0} transaction_id:{1}'.format(r.text, transaction_id))

    @property
    def getTranasctionId(self):
        self.setClickConv
        return self.transactionidList

if __name__ == '__main__':
    c = Constructor()
    print c.getTranasctionId