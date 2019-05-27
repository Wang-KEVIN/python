import requests
import time
import io
import re
import re
import sys

def main(doornum):
	login_url = "http://202.116.25.12/Login.aspx"
	
	data = {
		"__LASTFOCUS":"", 
		"__VIEWSTATE": "/wEPDwULLTE5ODQ5MTY3NDlkZM4DISokA1JscbtlCdiUVQMwykIc",
		"__VIEWSTATEGENERATOR": "C2EE9ABB",
		"__EVENTTARGET":"" ,
		"__EVENTARGUMENT": "",
		"__EVENTVALIDATION": "/wEWBQLz+M6SBQK4tY3uAgLEhISACwKd+7q4BwKiwImNC7oxDnFDxrZR6l5WlUJDrpGZXrmN",
		"hidtime": "",
		"txtname": "",
		"txtpwd":"", 
		"ctl01":"" 
	}
	//请求
	data['hidtime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	data['txtname']=str(doornum)
	session = requests.session()
	resps = session.post(login_url,data)
	//模拟发送请求
	
	catch_url = "http://202.116.25.12/default.aspx"
	
	html = session.get(catch_url).text
	#print(html)
	if(re.search(r"用户名不能为空，请重新输入",html)!=None):
		print("-1")
		return
	viewstate = re.search(r"id=\"__VIEWSTATE\" value=\"(.+)\" />",html).group(1)
	eventvalidation = re.search(r"id=\"__EVENTVALIDATION\" value=\"(.+)\" />",html).group(1)
	l2_value = re.search(r"editable:false,value:\"(.+)\",hiddenName:\"__12_value\"",html).group(1)
	
	data = {
		"__EVENTTARGET":"btn", #
		"__VIEWSTATE":viewstate,#
		"__VIEWSTATEGENERATOR":"CA0B0334",#
		"__EVENTVALIDATION":eventvalidation,#
		"PandValue":"10", #
		"hidpageCurrentSize":"1", #
		"hidpageSum":"1", #
		"hidpageCurrentSize2":"1", #
		"hidpageSum2":"4", #
		"hidpageCurrentSize3":"1", #
		"hidpageSum3":"25", #
		"__12_value":l2_value, # 
		"__41_value":"00900200", #
		"RegionPanel1$Region1$GroupPanel2$Grid3$Toolbar2$pagesize3":"1",
		"RegionPanel1$Region1$GroupPanel2$Grid2$Toolbar3$pagesize2":"1",
		"RegionPanel1$Region1$GroupPanel2$Grid1$Toolbar1$pagesize":"1",
		"__box_page_state_changed":"false",
		"__12_last_value":l2_value,
		"__41_last_value":"00000000",
		"__box_ajax_mark":"true"
	}
	//新的请求
	result = session.post(catch_url,data)
	result = re.search(r"setValue\(\"当前剩余电量\"\);box.__27.setValue\(\"([0-9]*\.[0-9]*)\"\);",result.text).group(1)
	//正则匹配爬取目标内容
	print(result)


if __name__ == "__main__":
	main(sys.argv[1])

