# -*- coding: cp936 -*-

import os
import sys
from ctypes import *


class PJ:
	def Po_Jie(self):
		print('>>>���ڳ�ʼ��...')
		YDMApi = windll.LoadLibrary('yundamaAPI-x64')
		appId = 7931
		appKey = b'07e97c69ff9cd82a854d636ae1c1cb5e'
		print('����ɣģ�%d\r\n�����Կ��%s' % (appId, appKey))
		username = b'machengguang'
		password = b'zxcv_1234'
		if username == b'test':
			exit('\r\n>>>���������û�������')
		print('\r\n>>>����һ��ʶ��...')
		codetype = 1004
		result = c_char_p(b"                              ")
		timeout = 60
		filename = b'Captcha.jpg'
		captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename, codetype, timeout, result)
		print("һ��ʶ����֤��ID��%d��ʶ������%s" % (captchaId, result.value))
		return result.value
