

import unittest
from mock import MagicMock,patch
import os

from kafka.common import *

import camup

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.SAVE_FOLDER='./test/data'


class test_read_dir(BaseTest):

    @patch("os.listdir")
    def test_no_files(self,osmock):
        """
        check that it doesn't find files
        """
        osmock.return_value=[]
        camup.read_dir(self.SAVE_FOLDER)
        assert osmock.called is True


    @patch("os.listdir")
    def test_with_files(self,osmock):
        """ check with a few files
        """
        osmock.return_value=["foo","bar"]
        camup.read_dir(self.SAVE_FOLDER)
        assert osmock.called is True

    @patch("os.listdir")
    def test_raising(self,osmock):
        """ what if the disk is not there
        """
        osmock.return_value="No folder"
        osmock.side_effect=OSError("No nono noooooo")
        self.assertRaises(OSError, camup.read_dir,self.SAVE_FOLDER)


class test_first_picture(BaseTest):
    def test_none_is_none(self):
        with self.assertRaises(ValueError):
            camup.get_first_picture(None) 

    def test_no_list_no_result(self):
        filelist = []
        file = camup.get_first_picture(filelist)

        assert file is None

    def test_one_jpg_one_pic(self):
        filelist = ["foo.jpg"]
        file = camup.get_first_picture(filelist)
        assert file == "foo.jpg"

    def test_caps_are_the_same(self):
        filelist = ["foo.JpG"]
        file = camup.get_first_picture(filelist)
        assert file == "foo.JpG"

    def test_non_images_are_ignored(self):
        filelist = ["foo.txt","bar.jpog","thumbs.db"]
        file = camup.get_first_picture(filelist)
        assert file is None


class test_clean_files(BaseTest):
    @patch("os.remove")
    def test_os_exception(self,osmock):
        osmock.side_effect=OSError("the filesystem can not perform the operation")

    @patch("os.remove")
    def test_everything_allright(self,osmock):
        camup.clean_files(["samplefile"])
        osmock.assert_called_with("samplefile")

    @patch("os.remove")
    def test_not_a_list_raises(self,osmock):
        assert osmock.called is False
        self.assertRaises(AssertionError,camup.clean_files,"rubis")
    

class test_build_message(BaseTest):
    def test_basic_input(self):
        binary_msg = '111101110001011010011101101110000111001111100101101111111010011100100100010111010100000100010110011011011111101111100010101100100000100010110100111011011100001110011111001011000101110101000001000101011001110110110001101111001101110011011101000101111101'
        result = camup.build_message("foo","bar")
        self.assertEqual(binary_msg, result)

    def test_noinput(self):
        self.assertRaises(TypeError, camup.build_message)


class test_send_message(BaseTest):
    def setUp(self):
        pass

    def test_nomessage(self):
        self.assertRaises(TypeError,camup.send_message)

    def test_samplemessage(self):
        assert camup.send_message("foo") is "Ok"

    @patch("camup.SimpleProducer")
    def test_general_error(self, kafkamock):
        kafkamock.side_effect=IOError("Kafka doesn't want you msg anymore")
        self.assertRaises(IOError, camup.send_message,"foo")

    @patch("camup.SimpleProducer")
    def test_kafka_error(self,kafkamock):
        kafkamock.side_effect=InvalidFetchRequestError("foo")
        self.assertRaises(InvalidFetchRequestError, camup.send_message, "fo")
        #TODO: This test is of little value when we removed custom exception behaviour. delete it or improve it.

    @patch("camup.SimpleProducer")
    def test_kafka_kafkian_exception(self,mockkafka):
        mockkafka.side_effect=MessageSizeTooLargeError("foo")
        self.assertRaises(MessageSizeTooLargeError, camup.send_message,"fo")


class test_publish(BaseTest):
    @patch("camup.raw_input")
    @patch("camup.send_message")
    def test_noinput(self,mockinput,mocksend):
        mockinput.return_value = "yes"
        mocksend.return_value = "Ok"
        self.assertRaises(TypeError, camup.publish)
        #assert mockinput.called is True
        #assert mocksend.called is True
        # Idon't really like it, but when you call assertRaises in unittest, creates a different scope, so you can not really access the mock from here. :( 
    
    @patch("camup.raw_input")
    @patch("camup.send_message")
    def test_normal_input(self,mocksend,mockinput):
        mockinput.return_value = "yes"
        mocksend.return_value = "Ok"
        camup.publish("topic","message")
        assert mockinput.called is True
        mocksend.assert_called_with("message")

    @patch("camup.raw_input")
    @patch("camup.send_message")
    def test_dont_send(self,mocksend,mockinput):
        mockinput.return_value = "NONONONONONONONO MOTHERFUCKER"
        mocksend.return_value = "yes"
        camup.publish("topic","message")
        assert mockinput.called is True
        assert mocksend.called is False

    @patch("camup.raw_input")
    @patch("camup.send_message")
    def test_false_yes(self,mocksend,mockinput):
        """ this shouldn't send the message"""
        mockinput.return_value = "this is not a yes"
        mocksend.return_value = "Ok"
        camup.publish("topic","message")
        assert mockinput.called is True
        assert mocksend.called is False
    

class test_lock_file(BaseTest):
    @patch("os.utime")
    def test_oserror(self,mockos):
        """If there is an issue in the filesystem"""
        mockos.side_effect=OSError("the filesystem is Fake!!")
        result = camup.lock_picture("anyfile")
        assert mockos.called is True

    @patch("os.utime")
    def test_osworks(self,mockos):
        """creating a lock returns the name of the lock"""
        mockos.return_value = "oh yeah"
        result = camup.lock_picture("anyfile")
        assert mockos.called is True
        assert result == "anyfile.lock"


if __name__=="__main__":
    unittest.main()
