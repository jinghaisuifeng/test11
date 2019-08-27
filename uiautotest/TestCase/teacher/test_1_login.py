#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/6/23 19:27
@Desc  : login test case
"""

from PageObject.Pages import PageObjects
from Base.BaseRunner import ParametrizedTestCase


class LoginTest(ParametrizedTestCase):
    """
    登录测试
    """

    def test_1_username_err(self):

        """用户名错误"""

        app = {
            'driver': self.driver,
            'data_path': self.data_path,
            'sheet': 'username_err'
        }
        page = PageObjects(app)
        page.operate()
        self.assertEqual(page.check()[0], True, msg=page.check()[1])

    # def test_2_passwd_err(self):
    #
    #     """密码错误"""
    #
    #     app = {
    #         'driver': self.driver,
    #         'data_path': self.data_path,
    #         'sheet': 'passwd_err'
    #     }
    #     page = PageObjects(app)
    #     page.operate()
    #     self.assertEqual(page.check()[0], True, msg=page.check()[1])
    #
    # def test_3_login_success(self):
    #
    #     """正常登录"""
    #
    #     app = {
    #         'driver': self.driver,
    #         'data_path': self.data_path,
    #         'sheet': 'login_success'
    #     }
    #     page = PageObjects(app)
    #     page.operate()
    #     self.assertEqual(page.check()[0], True, msg=page.check()[1])

    @classmethod
    def setUpClass(cls):
        super(LoginTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LoginTest, cls).tearDownClass()


