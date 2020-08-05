import os

def make_dir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
