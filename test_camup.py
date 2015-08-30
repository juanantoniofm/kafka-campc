

import unittest
from mock import MagicMock,patch
import os

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
        assert camup.get_first_picture(None) is None

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


if __name__=="__main__":
    unittest.main()
