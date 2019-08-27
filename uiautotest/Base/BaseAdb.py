#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/5/19 22:02
@Desc  : Encapsulation of base adb command
"""

import os
import subprocess
from Base.BaseLog import Log

logger = Log('Baseadb.py').get_log()


class AdbOperate(object):

    """The class is aimed at encapsulating base adb command """

    @staticmethod
    def adb(cmd):
        """
        return the result of executing command
        :param cmd:
        :return:
        """
        return os.popen('adb %s' % cmd, 'r')

    @staticmethod
    def get_device_id():
        """
        get device ID
        :return:
        """
        cmd = 'devices'
        device_id = []
        res = AdbOperate.adb(cmd).readlines()
        for i in res:
            devices = i.split('\tdevice')
            if len(devices) >= 2:
                device_id.append(devices[0])
        logger.info('device id is: %s' % device_id)
        return device_id

    @staticmethod
    def get_android_ver(device_id):
        """
        get the device's android version
        :param device_id:
        :return:
        """
        cmd = '-s %s shell getprop ro.build.version.release' % device_id
        res = AdbOperate.adb(cmd).read()
        android_ver = res.split('\n')[0]
        logger.info('android version is: %s' % android_ver)
        return android_ver


if __name__ == '__main__':
    adb = AdbOperate()
    device = adb.get_device_id()[0]
    get_ver = adb.get_android_ver(device)
    print(device, get_ver)

