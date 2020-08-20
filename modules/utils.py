import os
import re
import logging
from datetime import datetime
from platform import uname
from sys import version
from modules import config

logger_utilities = logging.getLogger("Utilities")


def make_dir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)


def get_id(url):
	return re.match(
		r'https?://music\.bugs\.co\.kr/(?:(?:album|artist|playlist)/|[a-z]{2}-[a-z]{2}-?\w+(?:-\w+)*-?)(\w+)',
		url).group(1)

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

def log_system_information():
	logger_utilities.debug("System Information: {}".format(uname()))
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
		"DATE": datetime.strptime(track['release_ymd'], '%Y%m%d').strftime('%Y.%m.%d'),
		"GENRE": album['list'][0]['album_info']['result']['genre_str'].replace(",", "; "),
		"LABEL": '; '.join(str(label['label_nm']) for label in album['list'][0]['album_info']['result']['labels']),
		"LYRICS": lyrics
	}
	return meta
