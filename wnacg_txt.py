#coding:utf-8
import sys
sys.path.append('../')
import requests
import os

class queue:
	def __init__(self,list_):
		self.list_ = list_

	def drop(self):
		drop = self.list_[0]
		self.list_ = self.list_[1:]
		return drop

	def add(self,arr):
		self.list_.append(arr)

	def is_empty(self):
		if len(self.list_) == 0:
			return True
		else:
			return False

class wnacg_txt:
	def __init__(self,txt_path,file_path):
		self.txt_path = txt_path
		self.file_path = file_path

	def get_list(self):
		file = open(self.txt_path,'r')
		lines = file.readlines()
		result = []
		for line in lines:
			temp = line.split(' ')
			result.append(temp)
		return result

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
		with open(os.path.join(self.file_path,name.replace('\n','')),'wb') as f:
			f.write(img.content)
		print('get picture successfully',name)

	def main(self):
		list_result = self.get_list()
		list_queue = queue(list_result)
		while not list_queue.is_empty():
			message = list_queue.drop()
			try:
				url = message[0]
				name = message[1]
				self.download_picture(url,name)
			except:
				print('error in: ',url)
				list_queue.add(message)
		if os.path.exists(self.txt_path):
			os.remove(self.txt_path)
			print('txt file delete')

if __name__ == '__main__':
	factory = wnacg_txt('/Users/ruicheng/Downloads/111/save_img.txt','/Users/ruicheng/Downloads/111')
	factory.main()
