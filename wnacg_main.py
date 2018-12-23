#coding:utf-8
import sys
sys.path.append('../')
from wnacg_comic_new import wnacg_comic

if __name__ == '__main__':
	url = sys.argv[1]
	name = sys.argv[2]
	start = int(sys.argv[3])
	factory = wnacg_comic(url,name,start)
	factory.main()