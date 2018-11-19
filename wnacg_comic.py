#coding:utf-8
import sys
sys.path.append('../')
import os
import random
import requests
from config import wnacg_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class wnacg_comic:
	def __init__(self,url,title=None,start=1):
		'''
		初始化
		:param url:
		:param title:
		'''
		self.EC = EC
		self.By = By
		self.config = wnacg_config()
		self.start=start
		self.browser = webdriver.Chrome(self.config.webdriver_path)
		self.wait = WebDriverWait(self.browser,10)
		if title:
			self.save_path = os.path.join(self.config.save_path,title)
		else:
			self.save_path = os.path.join(self.config.save_path, random.randint(1,10))
		self.url = url

	def os_save_path(self):
		'''
		新建文件夹
		:return:
		'''
		if os.path.exists(self.save_path):
			print('file already exists')
			return
		os.mkdir(self.save_path)
		print('file ok')

	def get_url(self,url):
		'''
		驱动浏览器浏览网页
		:param url:
		:return:
		'''
		self.browser.get(url)

	def get_max_page(self):
		'''
		获取最大页数用于循环
		:return:
		'''
		text = self.browser.find_element_by_css_selector('span.newpagelabel').text
		max_page = int(text.split('/')[-1])
		return max_page

	def get_next_page(self):
		'''
		获取新页面
		此网站较为奇葩，下一页按钮并不是按钮，只是包含了下一页的地址
		:return:
		'''
		buttons = self.browser.find_elements_by_css_selector('a.btntuzao')
		for button in buttons:
			if button.text == '下一頁':
				next_button = button
		next_url = next_button.get_attribute('href')
		# print(next_url)
		return next_url

	def get_picture_url(self):
		'''
		获取当前页面的图片地址
		:return:
		'''
		try:
			url_base = self.wait.until(self.EC.presence_of_element_located((self.By.CSS_SELECTOR,'span#imgarea img#picarea.photo')))
			url = url_base.get_attribute('src')
			return url
		except:
			print('error in url:',url)
			return None

	def download_picture(self,url,name):
		'''
		下载图片到本地
		:param url:
		:param name:
		:return:
		'''
		img = requests.get(url)
		if img.status_code != 200:
			print('get picture fale')
			return
		with open(os.path.join(self.save_path,name+'.jpg'),'wb') as f:
			f.write(img.content)
		print('get picture successfully')

	def get_name(self,page,max_page):
		l = len(str(max_page))
		name = str(page)
		if len(name) < l :
			name = '0' * (l - len(name)) + name
		return name

	def close(self):
		'''
		关闭驱动
		:return:
		'''
		self.browser.close()

	def main(self):
		'''
		主函数
		:return:
		'''
		self.os_save_path()
		self.get_url(self.url)
		max_page = self.get_max_page()
		for page in range(self.start,max_page+1):
			print('start to get page:',page)
			img_url = self.get_picture_url()
			if not img_url:
				break
			self.download_picture(img_url,self.get_name(page,max_page))
			new_url = self.get_next_page()
			self.get_url(new_url)
		self.close()





if __name__ == '__main__':
	factory = wnacg_comic('https://www.wnacg.com/photos-view-id-5064365.html','[奥森ボウイ]俺得修学旅行～男は女装した俺だけ!!第01~25話',121)
	factory.main()



