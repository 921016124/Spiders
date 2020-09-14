# -*- coding: cp936 -*-

import os
import sys
from ctypes import *


class PJ:
	def Po_Jie(self):
		print('>>>正在初始化...')
		YDMApi = windll.LoadLibrary('yundamaAPI-x64')
		appId = 7931
		appKey = b'07e97c69ff9cd82a854d636ae1c1cb5e'
		print('软件ＩＤ：%d\r\n软件密钥：%s' % (appId, appKey))
		username = b'machengguang'
		password = b'zxcv_1234'
		if username == b'test':
			exit('\r\n>>>请先设置用户名密码')
		print('\r\n>>>正在一键识别...')
		codetype = 1004
		result = c_char_p(b"                              ")
		timeout = 60
		filename = b'Captcha.jpg'
		captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename, codetype, timeout, result)
		print("一键识别：验证码ID：%d，识别结果：%s" % (captchaId, result.value))
		return result.value
