# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import requests
import random
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import traceback
import urllib.request
import pymysql
import socket
#import win32api #pip install pypiwin32

#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True



#rasdial 宽带连接 19ab68----643534
def connect():
    cmd_str = "rasdial %s %s %s" % (g_adsl_account['name'], g_adsl_account['username'], g_adsl_account['password'])
    os.system(cmd_str)
    time.sleep(5)


#"rasdial 断开宽带连接 /disconnect"
def disconnect():
    cmd_str = "rasdial %s /disconnect" % g_adsl_account['name']
    os.system(cmd_str)
    time.sleep(5)
	
#获取ip地址	
def get_ip():
	#return ['ip','address']
	fp = urllib.request.urlopen("http://ip.chinaz.com/getip.aspx")
	mybytes = fp.read()
	# note that Python3 does not read the html code as string
	# but as html code bytearray, convert to string with
	mystr = mybytes.decode("utf8")
	fp.close()
	ip = mystr.find("ip")
	add = mystr.find("address")
	ip = mystr[ip+4:add-2]
	address = mystr[add+9:-2]
	return [ip,address]

#将ip地址插入数据库
def insert_db(ipdate):
	#try:
		#获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
		conn=pymysql.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
		cur=conn.cursor()                              #获取一个游标对象
		#cur.execute("CREATE DATABASE zongzong")          #执行对应的SQL语句
		#exit()
		cur.execute("USE zongzong")
		#exit()
		#cur.execute("CREATE TABLE `ip_log` (`id` int(11) NOT NULL AUTO_INCREMENT,`ip` varchar(32) DEFAULT NULL,`address` varchar(64) DEFAULT NULL,`keyword` varchar(64) DEFAULT '',`url` varchar(256) DEFAULT '',`error` varchar(64) DEFAULT '',`created_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;")
		
		#插入数据
		ISOTIMEFORMAT='%Y-%m-%d %X'
		ipdate.append( time.strftime( ISOTIMEFORMAT, time.localtime() ))
		cur.execute("INSERT INTO ip_log(ip,address,keyword,url,error,page,rank,created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",ipdate)
		
		#cur.execute("SELECT * FROM ip_log")
		#data=cur.fetchall()
		#print(data)
			
		cur.close()#关闭游标
		conn.commit()#向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
		conn.close()#关闭到数据库的连接，释放数据库资源
	#except:
	#	print("发生异常")	


#获取搜素出来的url
def get_search_url(driver):
	urls = []
	real = []
	real_url = []
	click_link = []
	content = driver.find_element_by_css_selector("div[id=\"content_left\"]")
	links = content.find_elements_by_tag_name("a")
	for link in links:
		if link.get_attribute('class') == "c-showurl":
			real.append(link.text)
			url = link.get_attribute('href')
			urls.append(url)
			
			#解密url
			header = requests.head(url).headers
			is_append = True
			for out_url in out_urls:
				if out_url in header['location']:
					is_append = False
					break
					
			if is_append == True:
				real_url.append(header['location'])
				#a标签对象
				click_link.append(link)
					
	#print(real)
	#print(urls)
	#return urls
	return [real_url,click_link]
	
	
#function：解析加密url，剔除竞争对手的url
# def get_real_url(urls):
	# real_url = []
	# for url in urls:
		# header = requests.head(url).headers
		# is_append = True
		# for out_url in out_urls:
			# if out_url in header['location']:
				# is_append = False
				# break
			
		# if is_append == True:
			# real_url.append(header['location'])
	# return real_url

#function 目标地址是否在某个list中
def get_urlIndex(tagurl,urls):
	i = 0
	has = -1
	for url in urls:
		if tagurl in url:
			has = True
			return i
		i = i+1
	return has 

	
#点击百度搜索内容下面的下一页
def click_nextBtn(driver):
	div = driver.find_element_by_css_selector("div[id=\"page\"]")
	a = div.find_elements_by_tag_name("a")
	for item in a:
		print(item.text)
		if item.text == "下一页>":
			item.click()
	
	return driver

			


#随机点击
def click_search_url(driver,items):
	urls = []
	real = []
	content = driver.find_element_by_css_selector("div[id=\"content_left\"]")
	links = content.find_elements_by_tag_name("a")
	i=0
	'''获取当前窗口'''
	nowhandle = driver.current_window_handle
	#allhandles=driver.window_handles
	#for handle in allhandles:
	#	print('....当前窗口....',handle.title)
	#exit()
	
	for link in links:
		if link.get_attribute('class') == "c-showurl":
			if i in items:
				print("随机点击item:",i)
				print(link.get_attribute('href'),link.text)
				#exit()
				link.click()
				#停留在点击页面
				time.sleep(random.randint(5,10))
			
				'''获取所有窗口'''
				allhandles=driver.window_handles
				#for handle in allhandles:
				#	print('....当前窗口....',handle.title)
				#exit()
				
				'''循环判断窗口是否为当前窗口'''
				for handle in allhandles:
					if handle != nowhandle:
						print("切换到当前窗口")
						driver.switch_to_window(handle)
						print("title:",driver.title)
						'''关闭当前窗口'''
						driver.close()
						'''回到原先的窗口'''
						print("切换到原来的窗口")
						driver.switch_to_window(nowhandle)
						print("title:",driver.title)
				print("本次随机点击完毕！")
						
			i=i+1

			
#获取随机点击的搜索页random.randint(0
def get_random_index(index,len):
	if index >= 8:
		random_index = [
			random.randint(0,4),random.randint(5,8)
		]
	elif index>=4:
		random_index = [
			random.randint(0,3),random.randint(3,index)
		]
	elif index>=0:
		random_index = [
			index
		]
	elif index == -1:
		if len <=5:
			random_index = [
				random.randint(0,5)
			]
		else:
			random_index = [
				#random.randint(0,4),random.randint(5,len)
				random.randint(5,len)
			]
	return random_index



def getUA():
	uaList = [
		#360
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
		#chrome
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
		#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
		
		#firefox
		#"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
		"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
		
		#ie11
		#"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
		#ie8 
		#"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; 4399Box.1357; 4399Box.1253; 4399Box.1357)",
		
		#2345王牌
		#"Chrome/39.0.2171.99 Safari/537.36 2345Explorer/6.5.0.11018",
		
		#搜狗
		#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
		#opera
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"
		
	]
	headers = random.choice(uaList)
	return headers

#屏幕浏览器窗口大小
def getWindowSize():
	wind_size = [
		[1920,1080],
		[1600,900],
		[1280,720]
	]
	headers = random.choice(wind_size)
	return headers
	
	
#屏幕分辨率设置
def setDisplay():
	display_size = [
		[1920,1080],
		[1680,1050],
		[1600,900],
		[1440,900],
		[1400,1050]
	]
	d_size = random.choice(display_size)
	
	dm = win32api.EnumDisplaySettings(None, 0)
	dm.PelsWidth = d_size[0]
	dm.PelsHeight = d_size[1]
	dm.BitsPerPel = 32
	dm.DisplayFixedOutput = 0
	win32api.ChangeDisplaySettings(dm, 0)

	
#拨号	19ab68----643534		
g_adsl_account = {
	"name":"宽带连接",
	"username":"19ab68",
	"password":"643534"
}


#屏蔽点击的地址（竞争对手）
out_urls = [
	'www.ef43.com.cn/zhuanti/2257/',
	'www.ef43.com.cn/brands/mdm/',
        'http://money.163.com/15/0416/11/ANANRECC00253B0H.html'
]


##内页词
targetURL = [
	#['www.beilaikang.com','产前65天'],
	#['www.beilaikang.com','孕产妇多用防风巾'],
	#['www.beilaikang.com','产妇专用弹力网眼内裤'],
	#['www.beilaikang.com','孕产妇保暖护腹内裤'],
	##['www.beilaikang.com','卡萨图儿童安全座椅'],
	##['www.beilaikang.com','卡萨图安全座椅'],
	#['www.hzalbl.com','杭州品牌折扣女装加盟'],
	#['www.hzalbl.com','杭州品牌女装折扣店'],
	#['www.hzalbl.com','杭州品牌折扣女装'],
	#['www.hzalbl.com','杭州品牌女装折扣加盟'],
	#['www.hzalbl.com','杭州时尚品牌女装加盟'],
	#['www.hzalbl.com','杭州时尚精品女装'],
	#['ssjj.qq.com','腾讯生死狙击'],
	#['ssjj.qq.com','生死狙击腾讯'],
	#['ssjj.qq.com','生死狙击OL'],
    
        ['http://www.hkuws.com','注册离岸公司'],
	['zs.efu.com.cn/mornfeeit/','梦菲雪'],
	['zs.efu.com.cn/chengshijiaren/','城市佳人'],
	['www.kidsnet.cn/exposition','童装展会'],
	#['top.kidsnet.cn/','童装加盟排行榜'],
	#['www.nynet.com.cn/','内衣网'],
	#['www.nzw.cn/','女装网'],
	['zs.efu.com.cn/ks/','卡索'],
	['zs.efu.com.cn/distin-kidny/','迪斯廷凯'],
	['zs.efu.com.cn/fuzhuang/luyidigao/','路易迪高童装代理'],
	['brand.efu.com.cn/brandshow-1221090.html','凯帝龙驰'],
	['zs.efu.com.cn/rabbitjero/','兔子杰罗'],
	['zs.efu.com.cn/wmprince/','西瓜王子'],
        ['zs.efu.com.cn/betu','百图'],
        ['zs.efu.com.cn/pepco/','小猪班纳'],


	#['http://news.ifeng.com/a/20160518/48795120_0.shtml','华夏信财'],
	['http://weibo.com/huaxiafinance','华夏信财'],
	['http://p2p.hexun.com/2016-04-26/183531215.html','华夏信财'],
	#['http://news.xinhuanet.com/fortune/2016-04/26/c_128932834.htm','华夏信财'],
	['http://www.xcf.cn/gdyw/201605/t20160526_772682.htm','华夏信财'],
	['http://www.huaxiaoxia.com/','华夏信财'],
        #['https://lc.huaxiafinance.com/','华夏信财'],



        ['so.tedu.cn','网络营销培训机构'],
        ['www.cosatto.net.cn','个性安全座椅'],
        ['www.kaihuata.com/','开化旅游'],
        #['www.kaihuata.com/','开化'],

        
        #['http://hotel.elong.com/beijing/chain53.html','7天连锁酒店'],
	#['http://hotel.elong.com/beijing/','北京宾馆住宿'],
	#['http://hotel.elong.com/beijing/60101567/','北京招待所'],
	#['http://hotel.elong.com/beijing/','北京住宿价格'],
	#['http://www.elong.com/','酒店预订'],
	#['http://hotel.elong.com/shanghai/','上海订宾馆'],
	#['http://hotel.elong.com/shanghai/','上海订房'],
	#['http://hotel.elong.com/shanghai/','上海订房网'],
	#['http://hotel.elong.com/shanghai/40201958/','上海商务酒店'],
	#['http://hotel.elong.com/shanghai/30201012/','上海市宾馆'],
	#['http://hotel.elong.com/wuxi/90933644/','书香府邸酒店'],
	#['http://hotel.elong.com/hongkong/53201178/','四季酒店'],
	#['http://hotel.elong.com/wuhan/01801320/','武汉枫尚酒店公寓'],
	#['http://hotel.elong.com/wuhan/01801473/','武汉友发商务酒店'],

]


for targetInfo in targetURL:
	try:
		#更换ip
		disconnect()
		connect()
		
		while(1):
                    try:
                        socket.gethostbyname("baidu.com")
                        break;
                    except:
                        disconnect()
                        connect()
		#更换分辨率
		#setDisplay()
		
		
		#启动浏览器
		#driver = webdriver.Ie()
		#driver = webdriver.Chrome()
		#driver = webdriver.Firefox()
		
		#设置PhantomJS的user_agent
		dcap = dict(DesiredCapabilities.PHANTOMJS)
		user_agent = getUA()
		print(user_agent)
		dcap["phantomjs.page.settings.userAgent"] = (
				user_agent
		)
		#dcap["phantomjs.page.settings.resourceTimeout"] = (15000)
		dcap["phantomjs.page.settings.loadImages"] = (False)
		driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--load-images=no'])
		
		
		# UA = getUA()
		# print(UA)
		# webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = UA
		# driver = webdriver.PhantomJS()
		
		driver.implicitly_wait(30)
		
		#清cookie
		driver.delete_all_cookies()

		#driver.maximize_window() # 浏览器全屏显示

		#打开百度
		driver.get("http://www.baidu.com/")
		#driver.get("http://mch.weiba01.com/2.php")
		
		#设置浏览器窗口大小
		window_size = getWindowSize()
		driver.set_window_size(window_size[0], window_size[1])
				
				
		#搜索某个关键词
		print('打开百度成功',driver.title)
		target = targetInfo[0]
		keyword = targetInfo[1]
		if len(targetInfo)>2:
				error_keyword = targetInfo[random.randint(2,len(targetInfo)-1)]       
		print(">>>>>>>>>>>>>>>点击的关键词：",keyword,"--->目标地址：",target,">>>>>>>>>>>>>>>>>>>>")
		
		
		if len(targetInfo)>2:
			#模拟错误关键词
			print("点击错误关键词：",error_keyword);
			driver.find_element_by_id("kw").send_keys(error_keyword)
			time.sleep(2)
			driver.find_element_by_id("su").click()
			time.sleep(5)
			driver.find_element_by_id("kw").clear()
			time.sleep(2)
			print("错误关键词点击完毕")
			
		driver.find_element_by_id("kw").send_keys(keyword)
		#time.sleep(2)

		#点击搜索按钮
		print("...开始点击搜索按钮..")
		driver.find_element_by_id("su").click()
		#exit()
		print("...点击完毕..")
		time.sleep(2)

		
		#获取搜索结果页 0:着陆页  1：对应的链接对象
		urls_res = get_search_url(driver)
		real_urls = urls_res[0]
		#get_search_url(driver)[1][2].click()
		
		
		#real_urls = get_real_url(urls)
		print("搜索出来的可点击着陆页个数：",len(real_urls))
		print(real_urls)
		index = get_urlIndex(target,real_urls)
		print("目标index:",index)

		page = 1
		while index == -1 and page <= 4:
			if page == 1:
				#点击前面的几个着陆页,模拟用户真实行为
				items = get_random_index(index,len(real_urls))
				#items = [4]
				print(items)
				click_search_url(driver,items)
			
			#下一页
			driver = click_nextBtn(driver)
			time.sleep(3)
			urls_res = get_search_url(driver)
			real_urls = urls_res[0]
			#real_urls = get_real_url(urls)
			print(real_urls)
			index = get_urlIndex(target,real_urls)
			
			page = page+1

			
			
		if index > 4 and page == 1:
			#第一页，随机点击两个或一个
			int = random.randint(1,2)
			if int == 2:
				items = get_random_index(index,len(real_urls))
			else:
				items = [1]
			print(items)
			click_search_url(driver,items)
			
		if page >=5:
			print("没有找到目标地址，放弃搜索...")
			print("关闭浏览器")
			driver.quit()
			
			time.sleep(5)
			data = get_ip()
			data.append(keyword)
			data.append(target)
			data.append("no_find")
			data.append(-1)
			data.append(-1)
			insert_db(data)
			continue
		
		print("目标在page",page,"当前排名：",index,real_urls[index])
		print("反问最后的目标页...")
		#driver.get(real_urls[index])
		urls_res[1][index].click()
		time.sleep(5)
		
		nowhandle = driver.current_window_handle
		allhandles = driver.window_handles
		#目标页和搜索栏目页切换下
		for handle in allhandles:
			if handle != nowhandle:
				print("切换到当前窗口")
				driver.switch_to_window(handle)
				stime = random.randint(15,25)
				#stime = 5;
				print("目标页title:",driver.title,"停留-->",stime)
				time.sleep(stime)
				'''关闭当前窗口'''
				driver.close()
				
				'''回到原先的窗口'''
				print("切换到原来的窗口")
				driver.switch_to_window(nowhandle)
				print("title:",driver.title)
		
		
		#time.sleep(random.randint(40,60))
		#time.sleep(5)

		#清除所有cookie
		print("打印cookie")
		cookie= driver.get_cookies()
		print(cookie)
		print("清除cookie")
		driver.delete_all_cookies()
		print("打印cookie:")
		cookie= driver.get_cookies()
		print(cookie)

		#关闭浏览器
		print("关闭浏览器")
		time.sleep(5)
		#driver.close()
		driver.quit()
		#time.sleep(5)
		
		#数据库记录运行信息
		data = get_ip()
		data.append(keyword)
		data.append(target)
		data.append("success")
		data.append(page)
		data.append(index)
		insert_db(data)
	
	except:
		data = get_ip()
		data.append(keyword)
		data.append(target)
		data.append("faild")
		data.append(-1)
		data.append(-1)
		insert_db(data)
	
