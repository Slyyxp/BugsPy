import os
import re
import logging
from datetime import datetime
import platform
from sys import version
from modules import config

logger_utilities = logging.getLogger("Utilities")

def make_dir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)

def get_id(url):
	return re.match(
		r'https?://music\.bugs\.co\.kr/(?:(?:album|artist|track|playlist)/|[a-z]{2}-[a-z]{2}-?\w+(?:-\w+)*-?)(\w+)',
		url).group(1)

def contribution_check(artist_id_provided, artist_id_api):
	if int(artist_id_provided) == int(artist_id_api):
		return False
	else:
		return True

def sanitize(fn):
	"""
	:param fn: Filename
	:return: Sanitized string

	Removes invalid characters in the filename dependant on Operating System.
	"""
	if _is_win():
		return re.sub(r'[\/:*?"><|]', '_', fn)
	else:
		return re.sub('/', '_', fn)

def determine_quality(track):
	if track['svc_flac_yn'] == 'Y':
		return 'flac'
	else:
		return 'mp3'

def exist_check(abs):
	"""
	:param abs: Absolute path
	:return: If path exists.
	"""
	if os.path.isfile(abs):
		logger_utilities.debug("{} already exists locally.".format(os.path.basename(abs)))
		return True

def _is_win():
	if platform.system() == 'Windows':
		return True

def log_system_information():
	logger_utilities.debug("System Information: {}".format(platform.uname()))
	logger_utilities.debug("Python Version: {}".format(version))
	logger_utilities.debug("Preferences: {}".format(config.prefs))

def organize_meta(album, track, lyrics):
	meta = {
		"ALBUM": track['album_title'],
		"ALBUMARTIST": track['artist_disp_nm'],
		"ARTIST": track['artist_disp_nm'],
		"TITLE": track['track_title'],
		"DISCNUMBER": str(track['disc_id']),
		"TRACKNUMBER": str(track['track_no']),
		"COMMENT": str(track['track_id']),
		"DATE": get_date(track['release_ymd']),
		"GENRE": album['list'][0]['album_info']['result']['genre_str'].replace(",", "; "),
		"LABEL": '; '.join(str(label['label_nm']) for label in album['list'][0]['album_info']['result']['labels']),
		"LYRICS": lyrics
	}
	return meta

def get_date(date):
	# Bugs sometimes does not include the day on the release date for older albums released on the first day of the month.
	# We will append it manuallly before date transformation.
	if len(date) == 6:
		date = date + "01"
	date_patterns = ["%Y%m%d", "%Y%m", "%Y"]
	for pattern in date_patterns:
		try:
			return datetime.strptime(date, pattern).strftime('%Y.%m.%d')
		except ValueError:
			pass
