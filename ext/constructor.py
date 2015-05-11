#! /usr/bin/env python
# --*-- coding:utf-8 --*--

#  构造跳转数据
import string
from random import randint
from config.setting import *
from ext.util import *


class Constructor(object):

    def __init__(self):
        self.transactionidList = list()
        self.logger = getLogger()

    @property
    def setClickConv(self):
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
                except Exception as ex:
                    traceback.print_exc()
                else:
                    jumpaddress = r.text
                    transaction_id = get_clickid(jumpaddress)
                    t = string.Template(conv_url_template)
                    conv_url = t.substitute({"transactionid":transaction_id})
                    time.sleep(randint(1,3))
                    try:
                        r = requests.get(conv_url)
                        if r.text == 'success=true;conversioned':
                            self.transactionidList.append(transaction_id)
                        else:
                            pass
                    except Exception as ex:
                        self.logger.error('set conv data failed')


    @property
    def getTranasctionId(self):
        self.logger.info('set click and conversion data begin')
        self.setClickConv
        self.logger.info('set click and conversion data end')
        return self.transactionidList

if __name__ == '__main__':
    c = Constructor()
    print c.getTranasctionId