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
                        return False
                for otherData in other.data:
                    if otherData not in self.data:
                        return False
        return True