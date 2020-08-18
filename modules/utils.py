import os
import re
import logging
from datetime import datetime

logger_utilities = logging.getLogger("Utilities")


def make_dir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)


def get_id(url):
	return re.match(
		r'https?://music\.bugs\.co\.kr/(?:(?:album|artist|playlist)/|[a-z]{2}-[a-z]{2}-?\w+(?:-\w+)*-?)(\w+)',
		url).group(1)


def exist_check(abs):
	"""
	:param abs: Absolute path
	:return: If path exists.
	"""
	if os.path.isfile(abs):
		logger_utilities.debug("{} already exists locally.".format(os.path.basename(abs)))
		return True


def organize_meta(album, track, lyrics):
	meta = {
		"ALBUM": track['album_title'],
		"ALBUMARTIST": track['artist_disp_nm'],
		"ARTIST": track['artist_disp_nm'],
		"TITLE": track['track_title'],
		"DISCNUMBER": track['disc_id'],
		"TRACKNUMBER": track['track_no'],
		"COMMENT": track['track_id'],
		"DATE": datetime.strptime(track['release_ymd'], '%Y%m%d').strftime('%Y.%m.%d'),
		"GENRE": album['list'][0]['album_info']['result']['genre_str'].replace(",", "; "),
		"LABEL": '; '.join(str(label['label_nm']) for label in album['list'][0]['album_info']['result']['labels']),
		"LYRICS": lyrics
	}
	return meta
