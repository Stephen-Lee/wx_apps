import requests
from bs4 import BeautifulSoup
import time
import random
import util

actual_result = []

proxy_list = util.getProxies(1,2)
agents = util.getUserAgent()

rank_data = util.UKRankData()
rand_proxy = util.getRandProxy(proxy_list)
print("使用随机代理:", rand_proxy)
rand_agent = random.choice(agents)

base_headers = {
	"authority": "www.amazon.co.uk",
	"method": "GET",
	# "path": "/mn/search/ajax/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=gaming+headset+ps4&rh=i%3Aaps%2Ck%3Agaming+headset+ps4&fromHash=%2Fref%3Dsr_pg_3%3Frh%3Di%253Aaps%252Ck%253Agaming%2Bheadset%2Bps4%26page%3D3%26keywords%3Dgaming%2Bheadset%2Bps4%26ie%3DUTF8%26qid%3D1526454787&section=ATF,BTF&fromApp=gp%2Fsearch&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1526457074&atfLayout=list",
	"scheme": "https",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9",
	"cookie": 'session-id=261-9544120-5738321; ubid-acbde=258-7852165-8152244; x-wl-uid=1zOWBl/FwBc8It99rDUJf/F9XSsVHvc4liiBM56Y/Aya1jx3RdmOyfbedW/cxDUfz2sPNM3UZziQ=; session-token="QgTIx2cHwdN9Vf3M/SXw5DjLn5qWA3iNhiHrVWfVOGGpK+Wv/DRLBRwDVp/XfecmORV5abBY8DMzi+YyiuR3udZw3+qitmx0+sX9HuWkAK8FOsjuKN6urd3ZARySQ2waMHD9o+zwkPvpe02X/0hDS8X17XnPVAya4nijN73Uf/lhezcxYIkdrqFmU7JAvALN7xvLQkQT0aoo8C18gJHwxiY2zvgk1nuBXpmdaXat05zHan8mSPTMdhW2qtyZj2QzhvTUsou9zQI="; csm-hit=tb:NTNJQGC7SYK5FR2FWSE9+s-KA61XGBVSJGZW5907CRS|1526606666333&adb:adblk_no; session-id-time=2082787201l',
	# "referer": "https://www.amazon.de/s/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=gaming+headset+ps4&rh=i%3Aaps%2Ck%3Agaming+headset+ps4",
	'user-agent': rand_agent
}

base_query_str = {
	"url": "search-alias=aps"
}
def getRank(data, page_no=1):
	query_str = base_query_str
	url = "https://www.amazon.co.uk/s/ref=nb_sb_noss_" + str(page_no)
	query_str['page'] = page_no
	query_str["field-keywords"] = data["product"]
	print("商品名: ", data["product"], " 要查找的商家:", data["merchant"])
	print("开始获取第",page_no, "页")
	r = requests.get(url, headers=base_headers, params=query_str, proxies=rand_proxy)
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
		actual_result.append(success_result)
		return
	else:
		print("商家不在该页")
		page_no += 1
		time.sleep(2)
		getRank(data, page_no)


for data in rank_data:
	# print(data)
	getRank(data)

print("结果:")
for res in actual_result:
	print("商品:", res["product"],  "商家:", res["mer"], "页数:", res["page"])