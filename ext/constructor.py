#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import requests
from config.setting import *

class Constructor(object):

    def __init__(self):
        pass

    def send_click(self):
        for data in offer_aff_combination:
            offer_id, aff_id = data
            url = '{0}offer_id={1}&aff_id={2}'.format(click_url, offer_id, aff_id)
            print url
            r = requests.get(url)
            print r.text

if __name__ == '__main__':
    c = Constructor()
    c.send_click()