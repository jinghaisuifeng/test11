# UiAutoTest

#### 介绍
基于数据驱动的Ui自动化框架

#### 环境要求
1. 框架基于Python3 + unittest + appium
2. 运行电脑需配置adb、aapt的环境变量
2. 配置appium环境，并确保appium版本1.9及以上
3. 目前只支持安卓手机，建议使用安卓7.0及以上设备
4. 运行时候，电脑只能同时连接一台测试机

#### 框架结构

1. App - 存放待测apk
2. Base - 存放基础工具类
3. DrivingData - 存放测试驱动数据（excel格式）
4. Log - 存放日志
5. PageObject - 封装页面的操作逻辑和校验逻辑
6. Result - 存放测试结果
7. TestCase - 存放测试用例
8. config.ini - 配置文件
9. runAll.py - 主脚本

#### 使用说明

1. excel字段详细说明（*表示重要字段）
    1. *step：执行步骤，可选operate和check，operate表示操作，check表示断言
    2. step_desc：执行步骤描述，打印日志使用
    3. page_object：操作步骤所处的页面描述，打印日志使用
    4. *location_type：常用定位方式， 可选方式为：id,xpath,name,class_name,css_selector,ids,xpaths,names,class_names,css_selectors，结尾为`s`的表示定位一组元素
    5. index：索引，如果location_type用定位一组元素，用index索引确定具体的元素，索引的下表从0开始，即要取组元素中的第一个元素，index为0
    6. *location_value：定位值，注意定位值里面均为英文字符，如有中文会导致无法正确定位
    7. *operate_method：常用操作方法，可选方法为：click,input,wait,imp_wait,close_allow_box,swipe_by_ratio,text,screenshot,quit
    8. *operate_value：操作值，**如有多个，中间以空格隔开**
2. operate_method字段详细说明
    1. click - 点击事件，location_type、location_value为必填字段，operate_value为空
    2. input - 清除输入框文本并输入事件，location_type、location_value、operate_value为必填字段，其中operate_value填写输入内容
    3. wait - 强制等待事件，location_type、location_value为空，operate_value（非必填项）填数字，如不填默认等待时间为1s，否则按照填写时间执行
    4. imp_wait - 隐式等待，location_type、location_value为空，operate_value（非必填项）填数字，如不填默认等待时间为5s，否则按照填写时间执行
    5. close_allow_box - 关闭权限弹框事件，location_type、location_value为空，operate_value（非必填项）填写格式为：权限button内容 关闭次数，如不填默认匹配`允许`字符，关闭次数为1次
    6. swipe_by_ratio - 滑动事件，location_type、location_value为空，operate_value（非必填项）填写格式：开始坐标 方向 滑动比例 持续时间（毫秒），如不填默认`start_x=500, start_y=800, direction='up', ratio=0.1, duration=200`执行
    7. text - 获取元素文本，location_type、location_value为空，operate_value（非必填项），通常用于check方法下，获得的元素文本与operate_value内容作对比
    8. screenshot - 截图事件，location_type、location_value为空，operate_value（非必填项）填写内容为截图文件名，如不填默认为screenshot+当前时间戳
    9. quit - 退出时间，一般用于运行结束，关闭app
    10. is_login - 判断是否登录，如果是则退出，回到登录页，如果不是则直接进入登录页，location_type、location_value为空，operate_value（非必填项），填写内容为：登录标志字段 设置按钮的定位方式 设置按钮的定位值，如：`登录 id com.aspirecn.xiaoxuntongParent.ln:id/me_setting`
    
    ***is_login*方法源码 - *BaseOperate.py***
    ```python
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

    ```
    
    ***swipe_by_ratio*方法源码 - *BaseOperate.py***
    ```python
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

    ```
    
 3. 测试用例集命名格式为：test_n_xxx.py，其中n为阿拉伯数字，可用数字大小控制用例集执行的先后顺序，xxx为脚本名，如：`test_2_notice.py`
 4. 测试用例编写格式
    2. 测试用例命名格式与测试用例集命名格式类似，可用数字大小控制用例集执行的先后顺序
    1. 每一个case需要传入不同的sheet
    3. 如果该条case无check，则不用写`self.assertEqual(page.check()[0], True, msg=page.check()[1])`
    4. 另外，在最后的`setUpClass`和`tearDownClass`方法下的`super`类中写当前测试用例集的类名，如：`super(SendNotice, cls).setUpClass()`，`SendNotice`为该用例集的类名
    4. 其余内容复制粘贴即可
    ```python
    from PageObject.Pages import PageObjects
    from Base.BaseRunner import ParametrizedTestCase
    
    class SendNotice(ParametrizedTestCase):
        """
        发通知测试
        """
    
        def test_1_send_text(self):
    
            """发文本通知"""
    
            app = {
                'driver': self.driver,
                'data_path': self.data_path,
                'sheet': 'text_notice'
            }
            page = PageObjects(app)
            page.operate()
            self.assertEqual(page.check()[0], True, msg=page.check()[1])
    
        def test_2_send_rich_text(self):
    
            """发图文音频通知"""
    
            app = {
                'driver': self.driver,
                'data_path': self.data_path,
                'sheet': 'rich_text_notice'
            }
            page = PageObjects(app)
            page.operate()
            self.assertEqual(page.check()[0], True, msg=page.check()[1])
    
        @classmethod
        def setUpClass(cls):
            super(SendNotice, cls).setUpClass()
    
        @classmethod
        def tearDownClass(cls):
            super(SendNotice, cls).tearDownClass()
    ```
 5. 配置文件说明
     ```python
    # --- PATH CONFIG --- #
    # 注意：以下均以使用该路径的py文件为当前路径的相对路径表达式
    [LOG_PATH]
    path = ../Log
    [RESULT_PATH]
    path = ./Result/
    # teacher
    [T_DATA_PATH]
    path = ./DrivingData/teacher.xlsx
    [T_APK_PATH]
    path = ./App/T_XXT_LN_35.apk
    [T_CASE_PATH]
    path = ./TestCase/teacher
    # parent
    [P_DATA_PATH]
    path = ./DrivingData/parent.xlsx
    [P_APK_PATH]
    path = ./App/P_XXT_LN_37.apk
    [P_CASE_PATH]
    path = ./TestCase/parent
    
    
    # --- OTHER FUNC CONFIG --- #
    [WAIT]
    # 显示等待时间
    time = 6
    
    [NORESET]
    # 重置应用（清除session信息），True为不需要重置，False为需要重置
    noReset = True
    
    [PORT]
    # appium服务的端口号，默认为4723，启动时请确认appium的端口号与之一致
    port = 4723
    
    [APP_TYPE]
    # 启动的客户端类型，若启动启动两个客户端`teacher`和`parent`中间用英文','隔开即可
    role_lst = teacher,parent
    # role_lst = teacher
    # role_lst = parent
    
    [OUTPUT]
    # 运行结果输出的方式，to_html为生成HTML测试报告，to_console为结果输出在控制器
    # method = to_html
    method = to_console
    ```
    
    
 #### 参考
 
 1. https://github.com/Louis-me/appium
 2. https://github.com/Lemonzhulixin/python-appium
    
    
    
    
    
    