try:	
	import time
	import sys
	import os
	if getattr(sys, 'frozen', False):
		os.chdir('../..')	
	sys.path.append("./amazon_rank_searcher")
	from bs4 import BeautifulSoup
	import xlrd
	from configparser import SafeConfigParser
	from rank_spider import RankSpirder
	

	print("你要干啥？")
	print("1: 我要查找商品排名 ")
	print("2: 开启微信个人服务")
	app_index = input()
	if app_index == "1":
		os.chdir('./amazon_rank_searcher')
		rank_app = RankSpirder()
		rank_app.initDe()
		rank_app.run()
		print("输入回车键结束")
		key = input()
	elif app_index == "2":
		import wechat_service
except Exception as e:
	print(e)
	print("程序将在6秒后关闭")
	time.sleep(6)


