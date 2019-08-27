#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/5/19 23:59
@Desc  : Get apk package and activity
"""

import re
import os
import subprocess
from Base.BaseLog import Log

logger = Log('BaseApk.py').get_log()


class ApkInfo(object):

    """class of get apk's info"""

    def __init__(self, apk_path):
        """
        initial apk path
        :param apk_path:
        """
        self.apk_path = apk_path
        logger.info('apk path: %s' % self.apk_path)

    def get_appPackage(self):
        """
        get package name
        :return:
        """
        cmd = "aapt dump badging %s" % self.apk_path
        logger.info('get_appPackage command: %s' % cmd)
        res = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=True
        )
        (output, err) = res.communicate()
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        if not match:
            logger.info("can't get packageinfo")
            raise Exception("can't get packageinfo")
        package_name = match.group(1)
        version_code = match.group(2)
        version_name = match.group(3)
        logger.info('package name: %s, version code: %s, version name: %s'
                    % (package_name, version_code, version_name))
        return package_name, version_code, version_name

    def get_appActivity(self):
        """
        get app activity
        :return:
        """
        cmd = "aapt dump badging %s" % self.apk_path
        logger.info('get_appActivity command: %s' % cmd)
        res = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=True
        )
        (output, err) = res.communicate()
        match = re.compile(r"launchable[\s-]+activity[\s:]+name='(\S+)'").search(output.decode())
        if not match:
            logger.info("can't get packageinfo")
            raise Exception("can't get packageinfo")
        package_activity = match.group(1).split('label=')[0] if 'label=' in match.group(1) else match.group(1)
        logger.info('package activity: %s ' % package_activity)
        return package_activity


if __name__ == '__main__':

    PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
    path = PATH('../App/T_XXT_LN_35.apk')
    apk = ApkInfo(path).get_appPackage()
    print(apk, '\n', ApkInfo(path).get_appActivity())
    print(cmd)

