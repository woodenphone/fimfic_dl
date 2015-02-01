#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     01/02/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------



import unittest

from fimfic_dl import *




class Test_generate_full_path(unittest.TestCase):
    """generate_full_path(root_path,story_id,version_number,filename)"""
    def test_minimum_values(self):
        expected_result = os.path.join("", "000", "000", "000", "v1", "filename.txt")
        result = generate_full_path("",0,1,"filename.txt")
        self.assertEqual(result,expected_result)

    def test_maximum_values(self):
        expected_result = os.path.join("", "999", "999", "999", "v999999999", "filename.txt")
        result = generate_full_path("",999999999,999999999,"filename.txt")
        self.assertEqual(result,expected_result)

    def test_different_values(self):
        expected_result = os.path.join("", "123", "456", "789", "v987654321", "filename.txt")
        result = generate_full_path("",123456789,987654321,"filename.txt")
        self.assertEqual(result,expected_result)


class Test_generate_story_folder_path(unittest.TestCase):
    """generate_story_folder_path(root_path,story_id)"""
    def test_minimum_values(self):
        expected_result = os.path.join("", "000", "000", "000")
        result = generate_story_folder_path("",0)
        self.assertEqual(result,expected_result)

    def test_maximum_values(self):
        expected_result = os.path.join("", "999", "999", "999")
        result = generate_story_folder_path("",999999999)
        self.assertEqual(result,expected_result)

    def test_different_values(self):
        expected_result = os.path.join("", "123", "456", "789")
        result = generate_story_folder_path("",123456789)
        self.assertEqual(result,expected_result)













def main():
    unittest.main()

if __name__ == '__main__':
    main()
