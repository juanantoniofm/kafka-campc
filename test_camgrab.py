#!/usr/bin/python

import unittest
import mock

import time
import camgrab


class test_get_img_id(unittest.TestCase):
    def test_fails_on_no_input(self):
        self.assertRaises(AssertionError, camgrab.get_img_id)

    def test_accepts_string_id(self):
        """
        a static timestamp for gmtime
            1440818444
        which is 
            time.struct_time(tm_year=2015, tm_mon=8, tm_mday=29, tm_hour=3, tm_min=20, tm_sec=44, tm_wday=5, tm_yday=241, tm_isdst=0)
        """

        self.assertEqual("20150829_0320_44_cam999",camgrab.get_img_id(time.gmtime(1440818444),"999"))
    
    def test_accepts_number_id(self):
        self.assertEqual("20150829_0320_44_cam999",camgrab.get_img_id(time.gmtime(1440818444),999))


if __name__=="__main__":
    unittest.main()
