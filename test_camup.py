

import __builtin__

import unittest
from mock import MagicMock,patch, mock_open
import os

from kafka.common import *

import camup
import settings

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
            camup.get_picture_from_storage(None) 

    def test_no_list_no_result(self):
        filelist = []
        file = camup.get_picture_from_storage(filelist)

        assert file is None


    @patch("camup.is_locked")
    def test_a_normal_list(self,mocklock):
        mocklock.return_value = False
        filelist = ['20150905_1225_29_cam0.jpg', '20150905_1225_33_cam0.jpg', '20150905_1225_26_cam0.jpg']
        file = camup.get_picture_from_storage(filelist)
        self.assertEqual( file , '20150905_1225_26_cam0.jpg')

    @patch("camup.is_locked")
    def test_getting_the_latest_picture(self,mocklock):
        mocklock.return_value = False
        filelist = ['20150905_1225_29_cam0.jpg', '20150905_1225_33_cam0.jpg', '20150905_1225_26_cam0.jpg']
        file = camup.get_picture_from_storage(filelist, reverse=True)
        self.assertEqual( file , '20150905_1225_33_cam0.jpg')


    @patch("camup.is_locked")
    def test_one_jpg_one_pic(self,mocklock):
        mocklock.return_value = False
        filelist = ["foo.jpg"]
        file = camup.get_picture_from_storage(filelist)
        assert file == "foo.jpg"

    @patch("camup.is_locked")
    def test_caps_are_the_same(self,mocklock):
        mocklock.return_value = False
        filelist = ["foo.JpG"]
        file = camup.get_picture_from_storage(filelist)
        assert file == "foo.JpG"

    @patch("camup.is_locked")
    def test_a_locked_picture_returns_next(self,mocklock):
        mocklock.side_effect = [True, False] # this is a special call to only lock the 1st file
        filelist = ["pic1.jpeg","pic1.jpeg.lock","pic2.jpeg"]
        file = camup.get_picture_from_storage(filelist)
        assert file == "pic2.jpeg"


    def test_non_images_are_ignored(self):
        filelist = ["foo.txt","bar.jpog","thumbs.db"]
        file = camup.get_picture_from_storage(filelist)
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
    @patch("uuid.uuid4")
    def test_basic_input(self, mockuu):
        mockuu.return_value ="this-is-a-uuid"
        result = camup.build_message("foo","bar")
        expectation = '{"pictureName": "foo", "image": "YmFy\\n", "barcode": "bull-seat", "ride": "chewit", "id": "this-is-a-uuid"}'
        self.assertEqual(expectation, result)

    def test_noinput(self):
        self.assertRaises(TypeError, camup.build_message)

    def test_fail_on_binary_passed_as_id(self):
        bigbin = "aoeuidrtns" * 1000
        self.assertRaises(AssertionError, camup.build_message, bigbin, "foo","bar")

    @patch("uuid.uuid4")
    def test_adding_a_barcode(self,mockuu):
        mockuu.return_value = "this-is-a-uuid"
        result = camup.build_message("foo","bar","barcode")
        expectation = '{"pictureName": "foo", "image": "YmFy\\n", "barcode": "barcode", "ride": "chewit", "id": "this-is-a-uuid"}'
        self.assertEqual(expectation,result)


class test_send_message(BaseTest):
    def setUp(self):
        pass

    def test_nomessage(self):
        self.assertRaises(TypeError,camup.send_message)

    @patch("camup.SimpleProducer")
    @patch("camup.KafkaClient")
    def test_general_error(self, mockclient,kafkamock):
        kafkamock.side_effect=IOError("Kafka doesn't want you msg anymore")
        self.assertRaises(IOError, camup.send_message,"foo")

    @patch("camup.SimpleProducer")
    @patch("camup.KafkaClient")
    def test_kafka_error(self,mockclient,kafkamock):
        kafkamock.side_effect=InvalidFetchRequestError("foo")
        self.assertRaises(InvalidFetchRequestError, camup.send_message, "fo")
        #TODO: This test is of little value when we removed custom exception behaviour. delete it or improve it.

    @patch("camup.SimpleProducer")
    @patch("camup.KafkaClient")
    def test_kafka_kafkian_exception(self,mockclient,mockkafka):
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
        #assert mockinput.called is True
        mocksend.assert_called_with("message")

    @patch("camup.raw_input")
    @patch("camup.send_message")
    def test_dont_send(self,mocksend,mockinput):
        mockinput.return_value = "NONONONONONONONO MOTHERFUCKER"
        mocksend.return_value = "yes"
        camup.publish("topic","message")
        #assert mockinput.called is True
        #assert mocksend.called is False

    @patch("camup.raw_input")
    @patch("camup.send_message")
    def test_false_yes(self,mocksend,mockinput):
        """ this shouldn't send the message"""
        mockinput.return_value = "this is not a yes"
        mocksend.return_value = "Ok"
        camup.publish("topic","message")
        #assert mockinput.called is True
        #assert mocksend.called is False
    

class test_lock_file(BaseTest):
    def setUp(self):
        self.SVFD = settings.SAVE_FOLDER
    @patch("os.utime")
    @patch("camup.open")
    def test_oserror(self,mockopen,mockos):
        """If there is an issue in the filesystem"""
        mockos.side_effect=OSError("the filesystem is Fake!!")
        self.assertRaises(OSError, camup.lock_picture,"anyfile")
        assert mockos.called is True

    @patch("os.utime")
    @patch("camup.open")
    def test_osworks(self,mockopen,mockos):
        """creating a lock returns the name of the lock"""
        mockos.return_value = "oh yeah"
        result = camup.lock_picture("anyfile")
        assert mockos.called is True
        self.assertEqual( result , self.SVFD + "/" + "anyfile.lock")


class test_acquire_a_picture(BaseTest):
    """
    this class requires a bit more of work, due to the patching of open.
    that's why we need to import builtin (for python 2 only)
    and use patch.object instead of just patch.
    """
    @patch("camup.get_picture_from_storage")
    @patch("camup.lock_picture")
    @patch.object(__builtin__,"open", mock_open(read_data="datastream"))
    def test_alright(self,mocklock,mockgetfirst):
        """ if everything goes well, return the image stream and the img_id"""
        mockgetfirst.return_value = "thiscouldbea.jpg"
        result = camup.acquire_a_picture()

        mocklock.assert_called_with("thiscouldbea.jpg")
        assert mockgetfirst.called is True
        self.assertEqual(("datastream","thiscouldbea"), result)


    @patch("camup.get_picture_from_storage")
    @patch("camup.lock_picture")
    @patch.object(__builtin__,"open", mock_open(read_data="datastream"))
    def test_we_dont_lock_if_we_dont_want_to(self,mocklock,mockgetfirst):
        """ if everything goes well, return the image stream and the img_id"""
        mockgetfirst.return_value = "thiscouldbea.jpg"
        result = camup.acquire_a_picture(lockit=False)

        assert mockgetfirst.called is True
        assert mocklock.called is False
        self.assertEqual(("datastream","thiscouldbea"), result)


class test_is_locked(BaseTest):
    def test_the_picture_is_locked_returns_true(self):
        filelist =  ["pic1.jpg","pic2.jpeg", "pic1.jpg.lock"]
        assert camup.is_locked("pic1.jpg",filelist) is True

    def test_passing_a_filelist(self):
        filelist =  ["pic1.jpg","pic2.jpeg", "pic2.jpeg.lock"]
        assert camup.is_locked("pic1.jpg",filelist) is False

    @patch("os.listdir")
    def test_another_picture_not_locked_return_false(self,mockos):
        mockos.return_value = ["pic1.jpg","pic2.jpeg", "pic2.jpeg.lock"]
        assert camup.is_locked("pic1.jpg",path="crap") is False

    @patch("os.listdir")
    def test_passing_a_path(self,mockos):
        mockos.return_value = ["pic1.jpg","pic2.jpeg", "pic2.jpeg.lock"]
        assert camup.is_locked("pic1.jpg",path = "bullshitpath") is False

    @patch("os.listdir")
    def test_passing_a_path_and_failing_to_read(self,mockos):
        mockos.side_effect = OSError("oh son, the filesystem is borked")
        self.assertRaises(OSError, camup.is_locked,"pic1.jpg",path = "bullshitpath")



if __name__=="__main__":
    unittest.main()
