#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/5/19 22:01
@Desc  : The module of Encapsulating Ui element operation
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, WebDriverException, StaleElementReferenceException
from Base.BaseLog import Log
import configparser as cfgparser
import os
import time


logger = Log('BaseOperate.py').get_log()
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
screenshot_path = PATH('../Result/screenshot/')
if not os.path.exists(screenshot_path):
    os.mkdir(screenshot_path)

NOW = lambda: time.strftime('%Y%m%d%H%M%S')


class BaseOperate(object):

    """"""
    def __init__(self, driver):
        self.driver = driver
        self.cfg_path = PATH('../config.ini')
        self.cfg = cfgparser.ConfigParser()
        self.cfg.read(self.cfg_path, encoding='utf-8')

    def hightlight(self, el):
        """
        The function of hightlight element
        :param el:
        :return:
        """
        js = "arguments[0].style.border='2px solid red'"
        self.driver.execute_script(js, el)
        logger.info('hightlight element: %s' % el)

    def get_screen_size(self):
        """
        The function of get screen size
        :return:
        """
        size = self.driver.get_window_size()
        logger.info('get screen size: width is {width}, height is {height}'.format(**size))
        return size['width'], size['height']

    def get_screenshot(self, pic_name='screenshot' + NOW()):
        """
        Get screenshot
        :param pic_name:
        :return:
        """
        self.driver.get_screenshot_as_file(os.path.join(screenshot_path, pic_name + '.png'))
        logger.info('screenshot %s.png' % pic_name)

    def find_element(self, _type, location, step_desc=NOW()):
        """
        The function of find element
        :param step_desc
        :param _type:
        :param location:
        :return:
        """
        try:
            if _type == 'id':
                loc = (By.ID, location)
            elif _type == 'xpath':
                loc = (By.XPATH, location)
            elif _type == 'name':
                loc = (By.NAME, location)
            elif _type == 'class_name':
                loc = (By.CLASS_NAME, location)
            elif _type == 'css_selector':
                loc = (By.CSS_SELECTOR, location)
            else:
                loc = (By.ID, location)
            wait_time = int(self.cfg.get('WAIT', 'time'))
            el = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(loc))
            logger.info("element: '%s' locate success, method: '%s'" % (location, _type))
            # the function of hightlight in appium is unavailable
            # self.hightlight(el)
            return True, el
        except NoSuchElementException as e:
            logger.info("element: '%s' locate failure, method: '%s', error: %s" % (location, _type, e))
            self.get_screenshot('Fail_' + step_desc)
            return False,
        except TimeoutException as e:
            logger.info("element: '%s' locate failure, method: '%s', error: %s" % (location, _type, e))
            self.get_screenshot('Fail_' + step_desc)
            return False,
        except Exception as e:
            logger.info("element: '%s' locate failure, method: '%s', error: %s" % (location, _type, e))
            self.get_screenshot('Fail_' + step_desc)
            return False,

    def find_elements(self, _type, location, step_desc=NOW()):
        """
        The function of find elements
        :param step_desc
        :param _type:
        :param location:
        :return:
        """
        try:
            if _type == 'ids':
                loc = (By.ID, location)
            elif _type == 'xpaths':
                loc = (By.XPATH, location)
            elif _type == 'names':
                loc = (By.NAME, location)
            elif _type == 'class_names':
                loc = (By.CLASS_NAME, location)
            elif _type == 'css_selectors':
                loc = (By.CSS_SELECTOR, location)
            else:
                loc = (By.ID, location)
            wait_time = int(self.cfg.get('WAIT', 'time'))
            el = WebDriverWait(self.driver, wait_time).until(EC.presence_of_all_elements_located(loc))
            logger.info("element: '%s' locate success, method: '%s'" % (location, _type))
            # the function of hightlight in appium is unavailable
            # self.hightlight(el)
            return True, el
        except NoSuchElementException as e:
            logger.info("element: '%s' locate failure, method: '%s', error: %s" % (location, _type, e))
            self.get_screenshot('Fail_' + step_desc)
            return False,
        except TimeoutException as e:
            logger.info("element: '%s' locate failure, method: '%s', error: %s" % (location, _type, e))
            self.get_screenshot('Fail_' + step_desc)
            return False,
        except Exception as e:
            logger.info("element: '%s' locate failure, method: '%s', error: %s" % (location, _type, e))
            self.get_screenshot('Fail_' + step_desc)
            return False,

    @staticmethod
    def to_click(el):
        """
        The function of click
        :return:
        """
        try:
            el.click()
            logger.info('element object: %s click success' % el)
        except Exception as e:
            logger.info('element object: %s click failure: %s' % (el, e))

    @staticmethod
    def to_clear(el):
        """
        The function of clear
        :return:
        """
        try:
            el.clear()
            logger.info('element object: %s clear success' % el)
        except Exception as e:
            logger.info('element object: %s clear failure: %s' % (el, e))

    def input(self, el, content):
        """
        The function of send_keys
        :param el:
        :param content:
        :return:
        """
        try:
            self.to_clear(el)
            el.send_keys(content)
            logger.info('element object: %s send_keys success, value: %s' % (el, content))
        except Exception as e:
            logger.info('element object: %s send_keys failure: %s' % (el, e))

    @staticmethod
    def force_wait(_time=1):
        """
        The function of forced wait
        :param _time:
        :return:
        """
        time.sleep(_time)
        logger.info('forced wait %ss' % _time)

    def imp_wait(self, _time=5):
        """
        The function of implicitly_wait
        :param _time:
        :return:
        """
        self.driver.implicitly_wait(_time)
        logger.info('implicitly wait %ss' % _time)

    def close_allow_box(self, location='允许', num=1):
        """
        The function of close limited allow box
        :param location: The name of allow box
        :param num: The times of close box
        :return:
        """
        for i in range(num):
            loc = "//*/android.widget.Button[contains(@text, '%s')]" % location
            el = self.find_element('xpath', loc)
            if el[0]:
                self.to_click(el[1])
        logger.info('close limited allow box, location: %s, num: %s ' % (location, num))

    def swipe_by_ratio(self, start_x=500, start_y=800, direction='up', ratio=0.1, duration=200):
        """
        The function of swipe by ratio(按比例滑动屏幕)
        :param start_x: start abscissa
        :param start_y: start ordinate
        :param direction: The direction of swipe, support 'up', 'down', 'left', 'right'
        :param ratio: The screen ration's distance of swiping
        :param duration: continue time, unit ms
        :return:
        """
        self.force_wait(3)
        direction_tuple = ('up', 'down', 'left', 'right')
        if direction not in direction_tuple:
            logger.info('This swiping direction is not support')
        width, height = self.get_screen_size()

        def swipe_up():
            """
            swipe to up
            :return:
            """
            end_y = start_y - height * ratio
            if end_y < 0:
                logger.info('the distance of swiping too much')
            else:
                self.driver.swipe(start_x, start_y, start_x, end_y, duration)
                logger.info('from (%s, %s) swiping up to (%s, %s), during %sms' % (start_x, start_y, start_x, end_y, duration))

        def swipe_down():
            """
            swipe to down
            :return:
            """
            end_y = start_y + height * ratio
            if end_y > height:
                logger.info('the distance of swiping too much')
            else:
                self.driver.swipe(start_x, start_y, start_x, end_y, duration)
                logger.info('from (%s, %s) swiping down to (%s, %s), during %sms' % (start_x, start_y, start_x, end_y, duration))

        def swipe_left():
            """
            swipe to left
            :return:
            """
            end_x = start_x - width * ratio
            if end_x < 0:
                logger.info('the distance of swiping too much')
            else:
                self.driver.swipe(start_x, start_y, end_x, start_y, duration)
                logger.info('from (%s, %s) swiping left to (%s, %s), during %sms' % (start_x, start_y, end_x, start_y, duration))

        def swipe_right():
            """
            swipe to right
            :return:
            """
            end_x = start_x + width * ratio
            if end_x > width:
                logger.info('the distance of swiping too much')
            else:
                self.driver.swipe(start_x, start_y, end_x, start_y, duration)
                logger.info('from (%s, %s) swiping right to (%s, %s), during %sms' % (start_x, start_y, end_x, start_y, duration))
        swipe_dict = {
            'up': swipe_up,
            'down': swipe_down,
            'left': swipe_left,
            'right': swipe_right
        }
        # 【错误】，以下写法逻辑有问题，即在初始化字典时候就已经执行了所有滑动方法，最后还要返回的是swipe_dict[direction]函数
        # swipe_dict = {'up': swipe_up(),'down': swipe_down(),...}
        # return swipe_dict[direction]
        # 【正确】，字典中只初始化方向对应的函数，return返回具体的滑动函数调用
        return swipe_dict[direction]()

    @staticmethod
    def get_text(el):
        """
        The function of get text
        :return:
        """
        try:
            text = el.text
            logger.info('get text %s success' % text)
            return text
        except Exception as e:
            logger.info('get text %s failure: %s' % (el.text, e))

    def to_exit(self):
        """
        The function of quit
        :return:
        """
        self.driver.quit()
        logger.info('driver %s quit' % self.driver)

    # ----------Add operate method---------------#
    # add is_login method
    def is_login(self, login_text='登录', set_loc_type='id', set_loc='com.aspirecn.xiaoxuntongTeacher.ln:id/me_setting'):
        """
        判断是否为登录状态，是退出，否进入登录页
        :param login_text: 判断是否登录的标志字段
        :param set_loc_type: 设置元素定位方式
        :param set_loc: 设置元素定位
        :return:
        """
        wo_loc = "//*[@text='我']"
        login_text_loc = "//*[contains(@text, '%s')]" % login_text
        wo_el = self.find_element('xpath', wo_loc)
        self.to_click(wo_el[1]) if wo_el[0] else logger.info("切换'我'定位失败，请检查xpath是否正确：%s" % wo_loc)
        if self.find_element('xpath', login_text_loc)[0]:
            logger.info('the app is logout status')
            self.to_click(self.find_element('xpath', login_text_loc)[1])
        else:
            set_el = self.find_element(set_loc_type, set_loc)
            self.to_click(set_el[1]) if set_el[0] else logger.info("'设置'定位失败，请检查%s是否正确：%s" % (set_loc_type, wo_loc))
            logout_el = self.find_element('xpath', "//*[contains(@text, '退出')]")
            self.to_click(logout_el[1]) if logout_el[0] else logger.info("'退出'定位失败，请检查xpath是否正确：%s" % "//*[contains(@text, '退出')]")





