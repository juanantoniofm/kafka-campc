

import genutils
import unittest
import mock

class BaseTest(unittest.TestCase):
    def test_basic(self):
        pass


class test_message_processing(BaseTest):
    def test_normal_processing(self):
        input_data = """{"id":"value1","image":"value2","barcode":"value2","ride":"testride"}"""
        result = genutils.process_message_from_kafka(input_data)
        assert result["id"] == "value1"


if __name__=="__main__":
    unittest.main()
