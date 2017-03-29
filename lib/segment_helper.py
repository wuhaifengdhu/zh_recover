#!/usr/bin/python
# -*- coding: utf-8 -*-
import zh_segment
from subprocess import call


class SegmentHelper(object):
    def __init__(self, excel_file, dict_file):
        self.excel_file = excel_file
        self.dict_file = dict_file
        self.user_dict = None

    @staticmethod
    def generate_user_dict(excel_name, dict_output):
        """
        Read excel file and generate dict file
        :param excel_name:  excel file name, currently only support xls file
        :param dict_output:  dict output
        :return: None
        """
        call(['java', '-jar', 'problems.jar', excel_name, dict_output])

    def segment(self, words, probability=0.3):
        if self.user_dict is None:
            SegmentHelper.generate_user_dict(self.excel_file, self.dict_file)
            self.user_dict = zh_segment.parse_file(self.dict_file)
        return zh_segment.segment_phrase(words, self.user_dict, probability)


if __name__ == '__main__':
    SegmentHelper.generate_user_dict("test.xls", "my.dic")



