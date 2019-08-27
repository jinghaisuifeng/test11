#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/6/23 20:24
@Desc  : Run all case
"""
from HTMLTestRunner import HTMLTestRunner
from Base.BaseRunner import ParametrizedTestCase
from Base.BaseAdb import AdbOperate
from Base.BaseApk import ApkInfo
from Base.BaseLog import Log
import configparser as cfgparser
import os
import unittest
import time
from Base.SendEmail import SendEmail

logger = Log('runAll.py').get_log()

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
cfg = cfgparser.ConfigParser()
cfg.read(PATH('./config.ini'), encoding='utf-8')
t_case_path = cfg.get('T_CASE_PATH', 'path')
p_case_path = cfg.get('P_CASE_PATH', 'path')
res_path = cfg.get('RESULT_PATH', 'path')
run_type = cfg.get('APP_TYPE', 'role_lst')
opt_method = cfg.get('OUTPUT', 'method')


def get_discover(_role):
    """
    get discover
    :param _role:
    :return:
    """
    if _role == 'teacher':
        return unittest.defaultTestLoader.discover(t_case_path, pattern='test*.py', top_level_dir=t_case_path)
    else:
        return unittest.defaultTestLoader.discover(p_case_path, pattern='test*.py', top_level_dir=p_case_path)


def output_method(method, _role, _discover):
    """
    The method of running result output
    :param method:
    :param _role:
    :param _discover:
    :return:
    """
    if method == 'to_html':
        # now = time.strftime('%Y-%m-%d %H_%M_%S')  # 获取当前时间
        # filename = now + _role + 'Report.html'
        filename = 'Report.html'
        fp = open(res_path + filename, 'wb')
        _runner = HTMLTestRunner(stream=fp, title='客户端Ui测试报告', description='用例执行情况：')
        _runner.run(_discover)
        fp.close()
        # SendEmail().sendEmail('./Result/Report.html')
    elif method == 'to_console':
        _runner = unittest.TextTestRunner()
        _runner.run(_discover)
    else:
        logger.info('output method error')
        pass
    SendEmail().sendEmail('./Result/Report.html')

def get_devices(_role):
    devices = {}
    if _role == 'teacher':
        apkInfo = ApkInfo(PATH(cfg.get('T_APK_PATH', 'path')))
        devices['appPackage'] = apkInfo.get_appPackage()[0]
        devices['appActivity'] = apkInfo.get_appActivity()
        devices["app"] = PATH(cfg.get('T_APK_PATH', 'path'))
        devices['data_path'] = PATH(cfg.get('T_DATA_PATH', 'path'))
    else:
        apkInfo = ApkInfo(PATH(cfg.get('P_APK_PATH', 'path')))
        devices['appPackage'] = apkInfo.get_appPackage()[0]
        devices['appActivity'] = apkInfo.get_appActivity()
        devices["app"] = PATH(cfg.get('P_APK_PATH', 'path'))
        devices['data_path'] = PATH(cfg.get('P_DATA_PATH', 'path'))
    devices['platformName'] = 'Android'
    devices['deviceName'] = AdbOperate().get_device_id()[0]
    devices['platformVersion'] = AdbOperate.get_android_ver(devices['deviceName'])
    devices['noReset'] = cfg.get('NORESET', 'noReset')
    devices['port'] = cfg.get('PORT', 'port')
    if int(devices['platformVersion'].split('.')[0]) >= 6:
        devices['automationName'] = 'uiautomator2'
    return devices


if __name__ == '__main__':
    # SendEmail().sendEmail('./Result/Report.html')
    run_type_lst = run_type.split(',')
    logger.info('run_type_lst: %s ' % run_type_lst)
    for role in run_type_lst:
        logger.info('%s client is currently running' % role)
        discover = get_discover(role)
        devices = get_devices(role)
        ParametrizedTestCase(params=devices)
        output_method(opt_method, role, discover)




