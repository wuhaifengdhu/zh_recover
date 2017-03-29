#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import pandas as pd
from sklearn import tree
import unicodedata
import random
import os
import copy
from segment_helper import SegmentHelper
from lib.feature_extractor import FeatureExtractor
from lib.label_helper import LabelHelper
from lib.excel_helper import ExcelHelper
from sklearn import tree


class Recover(object):
    def __init__(self, excel_name, dict_file="wu.dic"):
        self.excel_name = excel_name
        self.dict_file = dict_file
        self.header, self.raw_data = ExcelHelper.read_excel(self.excel_name)
        self.row_number, self.column_number = self.raw_data.shape
        self.label = [[] for i in range(self.column_number)]
        self.model_list = []      # store model information
        self.error_base = [[] for i in range(self.row_number)]
        self.repair_data = copy.deepcopy(self.raw_data)
        self.has_label = False
        self.segment = SegmentHelper(self.excel_name, self.dict_file)

    def mark_error(self, excel_output):
        self._mark_label()
        ExcelHelper.write_excel(excel_output, self.raw_data, header=self.header, mask_array=self.label)

    def repair_excel(self, excel_output):
        self._mark_label()
        self._collect_error_knowledge_base()
        self._training_model()
        self._repair()
        ExcelHelper.write_excel(excel_output, self.repair_data, "repair", self.header, self.label, {1: 'red',
                                                                                                    2: 'yellow'})

    def _mark_label(self):
        if self.has_label:
            return
        for i in range(self.column_number):
            column_list = self.raw_data[:, i]
            column_features = FeatureExtractor(column_list).generate_features()
            self.label[i].extend(LabelHelper(column_features).get_label())
        self.has_label = True

    def _collect_error_knowledge_base(self):
        for i in range(self.row_number):
            for j in range(self.column_number):
                if self.label[j][i] != 0 and len(str(self.raw_data[i, j])) > 0:
                    self.error_base[i].append(self.raw_data[i, j])
                    self.error_base[i].extend(self.segment.segment(str(self.raw_data[i, j])))
        print(self.error_base)

    def _training_model(self):
        for i in range(self.column_number):
            model = tree.DecisionTreeRegressor(max_depth=4)
            column_list = self.raw_data[:, i]
            column_features = FeatureExtractor(column_list).generate_features()
            model = model.fit(column_features, self.label[i])
            self.model_list.append(model)

    def _repair(self):
        for i in range(self.row_number):
            for j in range(self.column_number):
                if self.label[j][i] != 0:
                    best_candidate = self._get_recover_data(i, j)
                    if best_candidate is not None:
                        self.repair_data[i, j] = best_candidate
                        print("(" + str(i) + "," + str(j) + ") choose " + str(best_candidate))
                        self.label[j][i] = 2  # 0 means good cell, 1 means error cell, 2 means repaired cell
                        self.error_base[i].remove(best_candidate)  # remove the data from knowledge base
                    else:
                        print("Can not find suitable error test for (%i, %i)" % (i, j))

    def _get_recover_data(self, row, column):
        candidates = None
        min_error_probability = 1
        for phrase in self.error_base[row]:
            element_features = FeatureExtractor([phrase]).generate_features()
            tmp_probability = self.model_list[column].predict(element_features)[0]
            print("Get probability %s for %s in (%i, %i)" %(tmp_probability, phrase, row, column))
            if tmp_probability < min_error_probability:
                max_probability = tmp_probability
                candidates = phrase
        return candidates


if __name__ == '__main__':
    _recover = Recover("test.xls", "wu.dic")
    # _recover.mark_error("error_mark.xls")
    _recover.repair_excel("repair.xls")
