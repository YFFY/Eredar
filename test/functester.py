#! /usr/bin/env python
# --*-- coding:utf-8 --*--


import unittest
from ext.jsoner import JsonDecorator



class FuncTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testJson_1(self):
        self.assertFalse(JsonDecorator({"programmers":{"firstName":"Brett","lastName":"McLaughlin","email":"aaaa"}}) == JsonDecorator({"programmers":{"firstName":"Brett","email":"aaaa","lastName":"McLaughlin"}}))


if __name__ == '__main__':
    unittest.main()
