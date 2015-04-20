#! /usr/bin/env python
# --*-- coding:utf-8 --*--

# json比较类

import json
from decimal import *

class JsonDecorator(object):

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        if isinstance(self.data, dict) and isinstance(other.data, dict):
            thisData = self.data
            otherData = other.data
        else:
            try:
                thisData = json.loads(self.data)
                otherData = json.loads(other.data)
            except Exception as ex:
                return False

        if len(thisData) != len(otherData):
            return False

        if thisData and otherData:
            for thisKey in thisData:
                if thisData.get(thisKey) != otherData.get(thisKey):
                    return False
            for otherKey in otherData:
                if thisData.get(otherKey) != otherData.get(otherKey):
                    return False

        return True