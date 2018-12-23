#coding:utf-8
import sys
sys.path.append('../')
from wnacg_comic import wnacg_comic

if __name__ == '__main__':
	url = sys.argv[1]
	name = sys.argv[2]
	start = int(sys.argv[3])
	factory = wnacg_comic(url, name, start)
	if sys.argv[4]:
		if int(sys.argv[4]) == 1:
			print('put img to txt')
			factory.main_txt()
	else:
		factory.main()
