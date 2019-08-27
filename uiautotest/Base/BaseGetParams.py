#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/6/18 20:23
@Desc  : The module of get parameters
"""

from Base.BaseReadExcel import row_value
import os

# Structure abspath by lambda method
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))


class GetParams(object):
    """
    package excel data
    """

    def __init__(self, file_path, sheet):

        self.fp = file_path
        self.sheet = sheet
        self.rows = row_value(self.fp, self.sheet)
        # zip函数依次将row[0]行与之后的每一行按照index相同条件重组为一个个元组，dict函数将其转为字典
        self.rows_dict = [dict(zip(self.rows[0], row_i)) for row_i in self.rows[1:]]

    def get_operate_params(self):
        """
        :return: return operate params
        """
        return [row_dict_i for row_dict_i in self.rows_dict if row_dict_i['step'] == 'operate' and row_dict_i['execution'] == 'Yes']

    def get_check_params(self):
        """
        :return: return check params
        """
        return [row_dict_i for row_dict_i in self.rows_dict if row_dict_i['step'] == 'check' and row_dict_i['execution'] == 'Yes']
