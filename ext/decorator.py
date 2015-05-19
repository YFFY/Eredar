#! /usr/bin/env python
# --*-- coding:utf-8 --*--

# json比较类

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
                    for otherData in other.data:
                        if thisData != otherData:
                            return False
                return True