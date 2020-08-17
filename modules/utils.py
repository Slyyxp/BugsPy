import os
import re
import logging

logger_utilities = logging.getLogger("Utilities")

def make_dir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)

def get_id(url):
    return re.match(r'https?://music\.bugs\.co\.kr/(?:(?:album|artist|playlist)/|[a-z]{2}-[a-z]{2}-?\w+(?:-\w+)*-?)(\w+)', url).group(1)

def exist_check(abs):
	"""
	:param abs: Absolute path
	:return: If path exists.
	"""
	if os.path.isfile(abs):
		logger_utilities.info("{} already exists locally.".format(os.path.basename(abs)))
		return True
