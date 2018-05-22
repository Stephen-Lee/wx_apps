import requests
from bs4 import BeautifulSoup
import time
import random
import util
from threading import Thread

class RankSpirder:
	def initDe(self):
		self.base_url = "https://www.amazon.de/s/ref=nb_sb_noss_"
		self.threads = [] 
		self.parser = util.getConfig()
		self.actual_result = []
		self.max_search_count = int(self.parser.get("settings", "max_search_count"))

		self.rank_data = util.germanyRankData()
		self.proxy_list = util.getProxies(1,3)
		self.agents = util.getUserAgent()
		self.base_headers = {
			"authority": self.parser.get("base_headers", "authority"),
			"method": self.parser.get("base_headers", "method"),
			# "path": "/mn/search/ajax/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=gaming+headset+ps4&rh=i%3Aaps%2Ck%3Agaming+headset+ps4&fromHash=%2Fref%3Dsr_pg_3%3Frh%3Di%253Aaps%252Ck%253Agaming%2Bheadset%2Bps4%26page%3D3%26keywords%3Dgaming%2Bheadset%2Bps4%26ie%3DUTF8%26qid%3D1526454787&section=ATF,BTF&fromApp=gp%2Fsearch&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1526457074&atfLayout=list",
			"scheme": self.parser.get("base_headers", "scheme"),
			"accept": self.parser.get("base_headers", "accept"),
			"accept-encoding": self.parser.get("base_headers", "accept-encoding"),
			"accept-language": self.parser.get("base_headers", "accept-language"),
			"cookie": self.parser.get("base_headers", "cookie")
			# "referer": "https://www.amazon.de/s/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=gaming+headset+ps4&rh=i%3Aaps%2Ck%3Agaming+headset+ps4",
			# 'user-agent': rand_agent
		}

		self.base_query_str = {
			"__mk_de_DE": self.parser.get("base_query", "__mk_de_DE"),
			"url": self.parser.get("base_query", "url")
		}

	def getRank(self, data, proxy, agent, page_no=1):
		query_str = self.base_query_str
		header = self.base_headers
		header["user-agent"] = agent 
		url = self.base_url + str(page_no)
		query_str['page'] = page_no
		query_str["field-keywords"] = data["product"]
		print(data["product"] ,"开始获取第",page_no, "页")
		r = requests.get(url, headers=header, params=query_str, proxies=proxy)
		if r.status_code == 200:
			print("获取页面成功")
			# filename = "./pages/" + data["product"] + str(page_no) + ".html"
			# fo = open(filename, "w")
			# fo.write(r.text)
		else:
			print("获取页面失败")
		mers = util.parsePageMers(r.text)
		if data['merchant'] in mers:
			print(data["product"]," 在第", page_no, "页")
			success_result = {"product": data["product"], "mer": data["merchant"], "page": page_no}
			self.actual_result.append(success_result)
			return
		else:
			print("商家不在该页")
			page_no += 1
			if page_no > self.max_search_count:
				print("找了", self.max_search_count, "页都找不到，放弃了!")
				return
			wait_time = random.randint(4,6)
			print("随机等待", wait_time, "秒")
			time.sleep(wait_time)
			self.getRank(data, proxy, agent, page_no)

	def getRankInstance(self,data):
		rand_proxy = util.getRandProxy(self.proxy_list)
		rand_agent = random.choice(self.agents)
		print("使用代理", rand_proxy, "处理:", data["product"], "商家:", data["merchant"])
		self.getRank(data, rand_proxy, rand_agent)

	def run(self):
		for data in self.rank_data:
			t = Thread(target=self.getRankInstance, args=[data])
			self.threads.append(t)
			t.start()

		for t in self.threads:
			t.join()

		result_file = open("德站排名结果.txt", "w")
		print("结果:")
		for res in self.actual_result:
			print("商品:", res["product"],  "商家:", res["mer"], "页数:", res["page"])
			# result_text = "商品:  %s,   商家:  %s,   页数: %i  \n" % (res["product"], res["mer"], res["page"])
			# result_file.write(result_text)

	def printResult(self):
		result_text = "结果:\n"
		for r in self.actual_result:
			text = "商品: %s  商家: %s  页数: %i \n" %(r["product"], r["mer"], r["page"])
			result_text += text
		return result_text	