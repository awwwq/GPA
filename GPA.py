
import requests
from bs4 import BeautifulSoup
import hashlib
import re

header = ''

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode('gb2312'))
    return m.hexdigest()


def parsesoup(soup):
	scorelist = []
	detailurl = 'http://202.202.1.176:8080/XSCJ/Stu_MyScore_detail.aspx?code='
	value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
	fenjidic = {'五级制': 1, '两档制': 0}
	fivedic = {'优秀': 95, '良好': 85, '中等': 75, '合格': 65, '不合格': 0}
	twodic = {'合格': 85, '不合格': 0}

	for t in soup.select('.B'):
		if not value.match(t.contents[6].text):
			if t.contents[6].text == '未录入':
				continue
			scorelist.append(t.contents[2].text)
			code = t.contents[9].a.get('onclick').strip('parent.openwin(\'').rstrip('\')')
			r = requests.post(detailurl+code, headers=header)
			detailsoup = BeautifulSoup(r.text, 'html.parser')
			if fenjidic[detailsoup.body.table.select('table')[0].contents[1].td.table.contents[1].select('td')[1].text]:
				scorelist.append(fivedic[t.contents[6].text])
			else:
				scorelist.append(twodic[t.contents[6].text])
		else:
			scorelist.append(t.contents[2].text)
			scorelist.append(t.contents[6].text)

	for t in soup.select('.H'):
		if not value.match(t.contents[6].text):
			if t.contents[6].text == '未录入':
				continue
			scorelist.append(t.contents[2].text)
			code = t.contents[9].a.get('onclick').strip('parent.openwin(\'').rstrip('\')')
			r = requests.post(detailurl+code, headers=header)
			detailsoup = BeautifulSoup(r.text, 'html.parser')
			if fenjidic[detailsoup.body.table.select('table')[0].contents[1].td.table.contents[1].select('td')[1].text]:
				scorelist.append(fivedic[t.contents[6].text])
			else:
				scorelist.append(twodic[t.contents[6].text])
		else:
			scorelist.append(t.contents[2].text)
			scorelist.append(t.contents[6].text)
	return scorelist

def chaxun(id,ps):
	id = id
	password = ps
	grade = 2014
	gpalist = []
	scorelist = []
	global header

	mdpw = md5(id+md5(password)[0:30].upper()+'10611')[0:30].upper()
	url = "http://202.202.1.176:8080/_data/index_login.aspx"
	params = {'Sel_Type':'STU','txt_dsdsdsdjkjkjc':id,'__VIEWSTATEGENERATOR':'CAA0A5A7','__VIEWSTATE':'dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1PjtpPDc+Oz47bDx0PHA8bDxUZXh0Oz47bDzph43luoblpKflraY7Pj47Oz47dDxwPGw8VGV4dDs+O2w8XDxzY3JpcHQgdHlwZT0idGV4dC9qYXZhc2NyaXB0Ilw+Clw8IS0tCmZ1bmN0aW9uIG9wZW5XaW5Mb2codGhlVVJMLHcsaCl7CnZhciBUZm9ybSxyZXRTdHJcOwpldmFsKCJUZm9ybT0nd2lkdGg9Iit3KyIsaGVpZ2h0PSIraCsiLHNjcm9sbGJhcnM9bm8scmVzaXphYmxlPW5vJyIpXDsKcG9wPXdpbmRvdy5vcGVuKHRoZVVSTCwnd2luS1BUJyxUZm9ybSlcOyAvL3BvcC5tb3ZlVG8oMCw3NSlcOwpldmFsKCJUZm9ybT0nZGlhbG9nV2lkdGg6Iit3KyJweFw7ZGlhbG9nSGVpZ2h0OiIraCsicHhcO3N0YXR1czpub1w7c2Nyb2xsYmFycz1ub1w7aGVscDpubyciKVw7CmlmKHR5cGVvZihyZXRTdHIpIT0ndW5kZWZpbmVkJykgYWxlcnQocmV0U3RyKVw7Cn0KZnVuY3Rpb24gc2hvd0xheShkaXZJZCl7CnZhciBvYmpEaXYgPSBldmFsKGRpdklkKVw7CmlmIChvYmpEaXYuc3R5bGUuZGlzcGxheT09Im5vbmUiKQp7b2JqRGl2LnN0eWxlLmRpc3BsYXk9IiJcO30KZWxzZXtvYmpEaXYuc3R5bGUuZGlzcGxheT0ibm9uZSJcO30KfQpmdW5jdGlvbiBzZWxUeWVOYW1lKCl7CiAgZG9jdW1lbnQuYWxsLnR5cGVOYW1lLnZhbHVlPWRvY3VtZW50LmFsbC5TZWxfVHlwZS5vcHRpb25zW2RvY3VtZW50LmFsbC5TZWxfVHlwZS5zZWxlY3RlZEluZGV4XS50ZXh0XDsKfQpmdW5jdGlvbiB3aW5kb3cub25sb2FkKCl7Cgl2YXIgc1BDPXdpbmRvdy5uYXZpZ2F0b3IudXNlckFnZW50K3dpbmRvdy5uYXZpZ2F0b3IuY3B1Q2xhc3Mrd2luZG93Lm5hdmlnYXRvci5hcHBNaW5vclZlcnNpb24rJyBTTjpOVUxMJ1w7CnRyeXtkb2N1bWVudC5hbGwucGNJbmZvLnZhbHVlPXNQQ1w7fWNhdGNoKGVycil7fQp0cnl7ZG9jdW1lbnQuYWxsLnR4dF9kc2RzZHNkamtqa2pjLmZvY3VzKClcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7fWNhdGNoKGVycil7fQp9CmZ1bmN0aW9uIG9wZW5XaW5EaWFsb2codXJsLHNjcix3LGgpCnsKdmFyIFRmb3JtXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6IitzY3IrIlw7c2Nyb2xsYmFycz1ub1w7aGVscDpubyciKVw7CndpbmRvdy5zaG93TW9kYWxEaWFsb2codXJsLDEsVGZvcm0pXDsKfQpmdW5jdGlvbiBvcGVuV2luKHRoZVVSTCl7CnZhciBUZm9ybSx3LGhcOwp0cnl7Cgl3PXdpbmRvdy5zY3JlZW4ud2lkdGgtMTBcOwp9Y2F0Y2goZSl7fQp0cnl7Cmg9d2luZG93LnNjcmVlbi5oZWlnaHQtMzBcOwp9Y2F0Y2goZSl7fQp0cnl7ZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHN0YXR1cz1ubyxyZXNpemFibGU9eWVzJyIpXDsKcG9wPXBhcmVudC53aW5kb3cub3Blbih0aGVVUkwsJycsVGZvcm0pXDsKcG9wLm1vdmVUbygwLDApXDsKcGFyZW50Lm9wZW5lcj1udWxsXDsKcGFyZW50LmNsb3NlKClcO31jYXRjaChlKXt9Cn0KZnVuY3Rpb24gY2hhbmdlVmFsaWRhdGVDb2RlKE9iail7CnZhciBkdCA9IG5ldyBEYXRlKClcOwpPYmouc3JjPSIuLi9zeXMvVmFsaWRhdGVDb2RlLmFzcHg/dD0iK2R0LmdldE1pbGxpc2Vjb25kcygpXDsKfQpcXC0tXD4KXDwvc2NyaXB0XD47Pj47Oz47dDw7bDxpPDE+Oz47bDx0PDtsPGk8MD47PjtsPHQ8cDxsPFRleHQ7PjtsPFw8b3B0aW9uIHZhbHVlPSdTVFUnIHVzcklEPSflrablj7cnXD7lrabnlJ9cPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nVEVBJyB1c3JJRD0n5biQ5Y+3J1w+5pWZ5biIXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1NZUycgdXNySUQ9J+W4kOWPtydcPueuoeeQhuS6uuWRmFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdBRE0nIHVzcklEPSfluJDlj7cnXD7pl6jmiLfnu7TmiqTlkZhcPC9vcHRpb25cPgo7Pj47Oz47Pj47Pj47dDxwPHA8bDxUZXh0Oz47bDzlj5HnlJ/mnKrnn6XplJnor6/vvIHnmbvlvZXlpLHotKXvvIE7Pj47Pjs7Pjs+Pjs+Tr8EDPbPuu5PdUoAduJtwsY/Ot0=',
			  'efdfdfuuyyuuckjg':mdpw}
	header = {'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
			  'Accept-Encoding':'gzip, deflate',
			  'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
			  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
			  'Host':'202.202.1.176:8080',
			  'Connection':'Keep-Alive'}
	searchurl = 'http://202.202.1.176:8080/xscj/Stu_MyScore_rpt.aspx'
	r = requests.post(url,data=params,headers = header)
	cookie = r.cookies['ASP.NET_SessionId']
	header = {'Cookie':'ASP.NET_SessionId='+cookie,'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
			  'Accept-Encoding':'gzip, deflate',
			  'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
			  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
			  'Host':'202.202.1.176:8080',
			  'Connection':'Keep-Alive'}
	for xn in range(grade,grade+4):
		for xq in range(0,2):
			searchparams = {'btn_search': '检索'.encode('gb2312'), 'sel_xn': xn, 'sel_xq': xq, 'SelXNXQ': '2', 'SJ': '0',
							'zxf': '0', 'zfx_flag': '0'}
			r = requests.post(searchurl,data=searchparams,headers=header)
			soup = BeautifulSoup(r.text,'html.parser')
			scorelist.append(parsesoup(soup))

	#GPA = jiaquan/xuefen
	for li in scorelist:
		if li:
			jiaquan = 0
			xuefen = 0
			for i in range(0,len(li),2):
				xuefen = xuefen + float(li[i])
				jiaquan = jiaquan + float(li[i])*float(li[i+1])
			gpalist.append((jiaquan/xuefen-50)/10)
	ji = ''
	i = 1
	for jidian in gpalist:
		ji = ji+'第%d学期:%.3f, '%(i,jidian)
		i=i+1
	return ji

if __name__ == '__main__':
	print(chaxun('20143893','Xx'))

