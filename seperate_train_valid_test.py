import os
import random
import shutil
import argparse

def make_dir(path):
	if not os.path.isdir(path):
		os.mkdir(path)

def main(root_dir):
	valid_dir = root_dir + 'valid/'
	train_dir = root_dir + 'train/'
	test_dir = root_dir + 'test/'

	make_dir(valid_dir)
	make_dir(train_dir)
	make_dir(test_dir)

	train_ratio, valid_ratio, test_ratio = 0.6, 0.2, 0.2
	data_list = os.listdir(root_dir)
	random.shuffle(data_list)
	data_len = len(data_list)//2
	
	ind = 0
	for file_name in data_list:
		if file_name.endswith('jpg'):
			img = file_name
			txt = file_name.split('.')[0] + '.txt'
	
			if ind <= data_len*train_ratio:
				shutil.move(root_dir+img, train_dir+img)
				shutil.move(root_dir+txt, train_dir+txt)
			elif ind <= data_len * (train_ratio + valid_ratio):
				shutil.move(root_dir+img, valid_dir+img)
				shutil.move(root_dir+txt, valid_dir+txt)
			else:
				shutil.move(root_dir+img, test_dir+img)
				shutil.move(root_dir+txt, test_dir+txt)
	
			ind+=1

if __name__=='__main__':
	for week in range(28, 42):
		parser = argparse.ArgumentParser()
		parser.add_argument('--root_dir', default='/home/rtos/바탕화면/test/data_sep_week/' + str(week) +'/')
		opts = parser.parse_args()

		main(opts.root_dir)
