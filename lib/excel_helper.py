#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import xlwt as excel


class ExcelHelper(object):
    @staticmethod
    def read_excel(excel_file):
        excel_data = pd.read_excel(excel_file)
        excel_data.fillna('', inplace=True)
        return excel_data.columns.tolist(), excel_data.values

    @staticmethod
    def write_excel(excel_file, data_array, sheet_name="data", header=None, mask_array=None, color_dict=None):
        if color_dict is None:
            color_dict = {1: "red"}
        book = excel.Workbook()
        sheet = book.add_sheet(sheet_name)
        row, column = data_array.shape

        # Write header to the first line if header exist
        if header:
            for i in range(len(header)):
                sheet.write(0, i, header[i])

        # Write body with render color
        for i in range(row):
            for j in range(column):
                style = ExcelHelper.get_style(i, j, mask_array, color_dict)
                if style is not None:
                    sheet.write(i + 1, j, data_array[i, j], style)
                else:
                    sheet.write(i + 1, j, data_array[i, j])
        book.save(excel_file)

    @staticmethod
    def get_style(r, c, mask_array, color_dic):
        if mask_array is None or color_dic is None:
            return None
        mask_value = mask_array[c][r]
        if mask_value not in color_dic.keys():
            return None
        style = 'pattern: pattern solid, fore_colour %s' % color_dic[mask_value]
        return excel.easyxf(style)


if __name__ == '__main__':
    _header, _data = ExcelHelper.read_excel('test.xls')
    _row, _col = _data.shape
    _mask = [[] for i in range(_col)]
    for i in range(_col):
        _mask[i].extend([1 if _data[r, i] < 0 else 0 for r in range(_row)])
    _color_dic = {1: "red"}
    ExcelHelper.write_excel("test_render.xls", _data, "data", _header, _mask, _color_dic)
