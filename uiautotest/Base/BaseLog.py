#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/5/13 18:48
@Desc  : The class of log function
"""

import os
import time
import logging
import configparser as cfgparser

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# create the log_path
now = time.strftime('%Y%m%d%H%M%S')
cfg = cfgparser.ConfigParser()
cfg.read(PATH('../config.ini'), encoding='utf-8')
log_path = PATH(cfg.get('LOG_PATH', 'path'))
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log(object):

    """定义日志类"""

    def __init__(self, _name):
        """
        初始化logger
        :param _name: 写每条log的名字
        """
        # structure a logger
        self.logger = logging.getLogger(_name)
        self.logger.setLevel(logging.INFO)

        # create a log file handler
        fh = logging.FileHandler(os.path.join(log_path, now + '.log'), encoding='utf-8')
        fh.setLevel(logging.INFO)

        # create a log terminal handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # define logger output format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # logger add handler function
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        """
        return logger
        :return:
        """
        return self.logger


if __name__ == '__main__':

    logger = Log('lidi').get_log()
    logger.info('lidi test logger')



