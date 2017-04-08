#!/usr/bin/python3
# -*- coding: utf8 -*-

from unittest import TestCase, main

def to_str(data) :
    if isinstance(data, str) :
        return data
    elif isinstance(data, bytes) :
        return data.decode('utf-8')
    else :
        raise TypeError('Must supply str or byte')


class ToStrTestCase(TestCase) :
    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tear down")

    def this_is_not_called(self) :
        print('test function start must start with test')
        
    def test_is_called(self) :
        print('test_is_called')

    def test_to_str_byte(self) :
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self) :
        self.assertEqual('hello', to_str('hello'))

    def test_to_str_bad(self) :
        self.assertRaises(TypeError, to_str, object())

if __name__ == '__main__' :
    main()