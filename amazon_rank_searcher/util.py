import requests
from bs4 import BeautifulSoup
import time
import random
import xlrd
import sys
from configparser import SafeConfigParser

def getConfig():
	print("正在读取配置文件config.ini")
	parser = SafeConfigParser()
	parser.read("config.ini")
	return parser

def readWebSite():
	websites = []
	websites_path = "./网址.xlsx"
	data = xlrd.open_workbook(websites_path)
	table = data.sheets()[0]
	row_num = table.nrows
	for i in (0, row_num -1):
		website = table.cell(i, 0).value
		websites.append(website)
	return websites

def germanyRankData():
	rank_data = []
	data = xlrd.open_workbook("德国排名.xlsx")
	table = data.sheets()[0]
	row_num = table.nrows
	for i in range(0, row_num):
		product = table.cell(i, 0).value
		merchant = table.cell(i, 1).value
		format_info = {'product': product, 'merchant': merchant}
		rank_data.append(format_info)
	return rank_data

def UKRankData():
	rank_data = []
	data = xlrd.open_workbook("英国排名.xlsx")
	table = data.sheets()[0]
	row_num = table.nrows
	for i in (0, row_num -1):
		product = table.cell(i, 0).value
		merchant = table.cell(i, 1).value
		format_info = {'product': product, 'merchant': merchant}
		rank_data.append(format_info)
	return rank_data

def getProxies(page_start, page_end):
	proxy_list = []
	proxy_api = "http://www.xicidaili.com/wt/"
	user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12"
	headers = {'User-Agent': user_agent}
	for page_num in range(page_start,page_end):
    		if page_num != 1:
    			actual_api = proxy_api + str(page_num)
    		else:
    			actual_api = proxy_api
    		api_result = requests.get(actual_api, headers=headers)
    		soup = BeautifulSoup(api_result.text, "html.parser")
    		trs = soup.find_all('tr')
    		for tr in trs:
    			tds = tr.find_all('td')
    			try:
    				proxy = {'ip': tds[1].string, "port": tds[2].string}
    				proxy_list.append(proxy)
    			except IndexError:	
    				print("")
    		print("正在获取代理ip...", page_num)
    		time.sleep(2)
	print("获得代理ip数:", len(proxy_list))
	return proxy_list

def getUserAgent():
	agent_list = [
	"Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
	"Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
	"Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
	"Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
	"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)",
	"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)"
	]
	return agent_list

def getRandProxy(proxy_list):
	ran_proxy = random.choice(proxy_list)
	proxy_list.remove(ran_proxy)
	format_addr = ran_proxy['ip'] + ":" + ran_proxy['port']
	format_proxy = {'http': format_addr}
	return format_proxy

def parsePageMers(pageText):
	soup = BeautifulSoup(pageText, "html.parser")
	items = soup.findAll('div', {"class": "a-row a-spacing-small"})
	item_result = []
	for item in items:
		mer = item.findAll('span', {"class": "a-size-small a-color-secondary"})
		if len(mer) == 2:
			item_result.append(mer[1].string)
	return item_result