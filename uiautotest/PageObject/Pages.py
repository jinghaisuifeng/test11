#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/6/18 20:23
@Desc  : The module of page base operating
"""
from Base.BaseOperate import BaseOperate
from Base.BaseGetParams import GetParams
from Base.BaseLog import Log
import re

logger = Log('Pages.py').get_log()


class PageObjects(object):
    """
    The class of base page operate
    """
    def __init__(self, kwargs):
        self.driver = kwargs["driver"]
        self.fp = kwargs['data_path']
        self.sheet = kwargs['sheet']
        self._operate = BaseOperate(self.driver)
        self.cases = GetParams(self.fp, self.sheet)

    def operate(self):
        """
        execute operated cases
        :return:
        """
        ope_case = self.cases.get_operate_params()
        if ope_case:
            for ope_case_i in ope_case:
                logger.info('%s -> %s -> %s' % (ope_case_i['step'], ope_case_i['page_object'], ope_case_i['step_desc']))
                if ope_case_i['location_type']:
                    if ope_case_i['location_type'][-1] != 's':
                        el = self._operate.find_element(ope_case_i['location_type'], ope_case_i['location_value'], ope_case_i['step_desc'])
                        if el[0]:
                            if ope_case_i['operate_method'] == 'click':
                                self._operate.to_click(el[1])
                            elif ope_case_i['operate_method'] == 'clear':
                                self._operate.to_clear(el[1])
                            elif ope_case_i['operate_method'] == 'input':
                                self._operate.input(el[1], ope_case_i['operate_value'])
                            continue
                    elif ope_case_i['location_type'][-1] == 's':
                        els = self._operate.find_elements(ope_case_i['location_type'], ope_case_i['location_value'], ope_case_i['step_desc'])
                        if els[0]:
                            if ope_case_i['operate_method'] == 'click':
                                self._operate.to_click(els[1][int(ope_case_i['index'])])
                            elif ope_case_i['operate_method'] == 'clear':
                                self._operate.to_clear(els[1][int(ope_case_i['index'])])
                            elif ope_case_i['operate_method'] == 'input':
                                self._operate.input(els[1][int(ope_case_i['index'])], ope_case_i['operate_value'])
                            continue
                    else:
                        logger.info('location_type is illegal, the legal format in (id,xpath,name,class_name,'
                                    'css_selector,ids,xpaths,names,class_names,css_selectors), please confirm!')
                else:
                    if ope_case_i['operate_method'] == 'wait':
                        if ope_case_i['operate_value']:
                            self._operate.force_wait(float(ope_case_i['operate_value']))
                        else:
                            self._operate.force_wait()
                    elif ope_case_i['operate_method'] == 'imp_wait':
                        if ope_case_i['operate_value']:
                            self._operate.imp_wait(float(ope_case_i['operate_value']))
                        else:
                            self._operate.imp_wait()
                    elif ope_case_i['operate_method'] == 'close_allow_box':
                        if ope_case_i['operate_value']:
                            value = re.split(r'[\s,，]+', ope_case_i['operate_value'])
                            logger.info("ope_case_i['operate_value']: %s" % value)
                            self._operate.close_allow_box(location=value[0], num=int(value[1]))
                        else:
                            self._operate.close_allow_box()
                    elif ope_case_i['operate_method'] == 'swipe_by_ratio':
                        if ope_case_i['operate_value']:
                            value = re.split(r'[\s,，]+', ope_case_i['operate_value'])
                            logger.info("ope_case_i['operate_value']: %s" % value)
                            start_x = int(value[0])
                            start_y = int(value[1])
                            direction = value[2]
                            ratio = float(value[3])
                            duration = int(value[4])
                            self._operate.swipe_by_ratio(start_x, start_y, direction, ratio, duration)
                        else:
                            self._operate.swipe_by_ratio()
                    elif ope_case_i['operate_method'] == 'screenshot':
                        if ope_case_i['operate_value']:
                            self._operate.get_screenshot(ope_case_i['operate_value'])
                        else:
                            self._operate.get_screenshot()
                    elif ope_case_i['operate_method'] == 'exit':
                        self._operate.to_exit()

                    # ----------------Add operate method condition----------------------#
                    # add is_login condition
                    elif ope_case_i['operate_method'] == 'is_login':
                        if ope_case_i['operate_value']:
                            value = re.split(r'[\s,，]+', ope_case_i['operate_value'])
                            logger.info("ope_case_i['operate_value']: %s" % value)
                            login_text = value[0]
                            set_loc_type = value[1]
                            set_loc = value[2]
                            self._operate.is_login(login_text, set_loc_type, set_loc)
                        else:
                            self._operate.is_login()

                    # operate_method is not exist
                    else:
                        logger.info('operate_method is not exist')
                        pass

        else:
            logger.info('operate case list is empty')

    def check(self):
        """
        execute check cases
        :return:
        """
        che_case = self.cases.get_check_params()
        if che_case:
            for che_case_i in che_case:
                logger.info('%s -> %s -> %s' % (che_case_i['step'], che_case_i['page_object'], che_case_i['step_desc']))
                if che_case_i['location_type']:
                    if che_case_i['location_type'][-1] != 's':
                        el = self._operate.find_element(che_case_i['location_type'], che_case_i['location_value'], che_case_i['step_desc'])
                        if el[0]:
                            # 避免重复打印get text日志，提前定义get_text，后面重复调用即可
                            get_txt = self._operate.get_text(el[1])
                            if get_txt in che_case_i['operate_value'] or che_case_i['operate_value'] in get_txt:
                                logger.info('%s, is success' % che_case_i['step_desc'])
                                return True, 'check ok'
                            else:
                                logger.info('%s, is failure, %s != %s' % (che_case_i['step_desc'], get_txt, che_case_i['operate_value']))
                                return False, '%s != %s' % (get_txt, che_case_i['operate_value'])
                    elif che_case_i['location_type'][-1] == 's':
                        els = self._operate.find_elements(che_case_i['location_type'], che_case_i['location_value'], che_case_i['step_desc'])
                        if els[0]:
                            get_txt = self._operate.get_text(els[1][int(che_case_i['index'])])
                            if get_txt in che_case_i['operate_value'] or che_case_i['operate_value'] in get_txt:
                                logger.info('%s, is success' % che_case_i['step_desc'])
                                return True, 'check ok'
                            else:
                                logger.info('%s, is failure, %s != %s' % (che_case_i['step_desc'], get_txt, che_case_i['operate_value']))
                                return False, '%s != %s' % (get_txt, che_case_i['operate_value'])
                    else:
                        logger.info('location_type is illegal, the legal format in (id,xpath,name,class_name,'
                                    'css_selector,ids,xpaths,names,class_names,css_selectors), please confirm!')
        else:
            logger.info('check case list is empty')






