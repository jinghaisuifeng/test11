#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/6/18 13:57
@Desc  : The module of encapsulating runner params
"""
from appium import webdriver
import configparser as cfgparser
from Base.BaseLog import Log
import unittest
import os

# Initial logger
logger = Log('BaseRunner.py').get_log()
# Structure abspath by lambda method
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))
# Initial cfgparser
cfg = cfgparser.ConfigParser()
cfg.read(PATH('../config.ini'), encoding='utf-8')


def appium_desired_caps(devices):

    desired_caps = {}
    desired_caps['platformName'] = devices['platformName']
    desired_caps['deviceName'] = devices['deviceName']
    desired_caps['platformVersion'] = devices['platformVersion']
    desired_caps["automationName"] = devices['automationName']
    desired_caps['appPackage'] = devices['appPackage']
    desired_caps['appActivity'] = devices['appActivity']
    desired_caps['app'] = devices["app"]
    desired_caps["unicodeKeyboard"] = True
    desired_caps["resetKeyboard"] = True
    # desired_caps['noSign'] = True
    desired_caps['noReset'] = devices['noReset']
    logger.info('desired_caps: %s' % desired_caps)
    remote = 'http://localhost:%s/wd/hub' % devices['port']
    logger.info('remote: %s' % remote)
    driver = webdriver.Remote(remote, desired_caps)
    logger.info('driver start-up successful, %s' % driver)
    return driver


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', params=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        global devices
        devices = params

    @classmethod
    def setUpClass(cls):
        cls.data_path = devices['data_path']
        cls.driver = appium_desired_caps(devices)
        logger.info('>>> A test_suite is starting <<<')

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_app()
        logger.info('>>> A test_suite is finished <<<')
        pass
