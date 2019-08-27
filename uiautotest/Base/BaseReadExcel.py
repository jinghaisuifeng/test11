#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import os


def cell_value(fp, sheet_name, row, col):
    """
    获取单元格的值
    :param fp:
    :param sheet_name:
    :param row:
    :param col:
    :return:
    """
    test_data = xlrd.open_workbook(fp)
    sheet_name = test_data.sheet_by_name(sheet_name)
    return sheet_name.cell_value(row-1, col-1)


def row_value(fp, sheet_name):
    """
    获取指定sheet所有行的值
    :param fp:
    :param sheet_name:
    :return:列表形式
    """
    test_data = xlrd.open_workbook(fp, 'br')
    sheet_name = test_data.sheet_by_name('%s' % sheet_name)
    return [sheet_name.row_values(row_i) for row_i in range(sheet_name.nrows)]


def col_value(fp, sheet_name, col):
    """
    获取整列的值
    :param fp:
    :param sheet_name:
    :param col:
    :return:
    """
    test_data = xlrd.open_workbook(fp)
    sheet_name = test_data.sheet_by_name('%s' % sheet_name)
    return sheet_name.col_values(col - 1)


if __name__ == '__main__':
    PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
    excel_fp = PATH('../DrivingData/testDrivingData.xlsx')
    res = row_value(excel_fp, 'test_login')
    print(res)