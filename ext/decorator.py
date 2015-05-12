#! /usr/bin/env python
# --*-- coding:utf-8 --*--

# json比较类

import json
from decimal import *

class JsonDecorator(object):

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):

        if not isinstance(self.data, list) and not isinstance(self.data, list):
            return False
        else:
            if len(self.data) != len(other.data):
                return False
            else:
                for thisData in self.data:
                    if thisData not in other.data:
                        print '{0} not in other data'.format(thisData)
                        return False
                for otherData in other.data:
                    if otherData not in self.data:
                        print '{0} not in self data'.format(otherData)
                        return False
        return True

if __name__ == '__main__':
    d = [{u'click': 1, u'offer_id': u'200002', u'aff_manager': u'90010413', u'conversion': 1, u'year': 2015}]
    m = [{u'click': Decimal('1'), u'offer_id': u'200002', u'aff_manager': u'90010413', u'conversion': Decimal('1'), u'year': u'2015'}]
    print JsonDecorator(d) == JsonDecorator(m)