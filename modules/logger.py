import os
import logging
from datetime import datetime
from modules.utils import make_dir
from modules.config import prefs

def log_setup():
	# TODO: Fix logging, requests are logging to console when they shouldn't.
	filename = '{:%H.%M.%S}.log'.format(datetime.now())
	folder_name = os.path.join(prefs['log_directory'], '{:%Y-%m-%d}'.format(datetime.now()))
	make_dir(folder_name)
	log_path = os.path.join(folder_name, filename)
	logging.basicConfig(level=logging.DEBUG,
	                    handlers=[logging.FileHandler(log_path, 'w', 'utf-8')],
	                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
	                    datefmt='%Y-%m-%d %H:%M:%S')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)
	logging.getLogger("requests").setLevel(logging.WARNING)
