import argparse
import logging
import os
from datetime import datetime
import sys
import requests
from tqdm import tqdm
from modules import logger, client, utils, config
from mutagen.flac import FLAC, Picture
import mutagen.id3 as id3
from mutagen.id3 import ID3NoHeaderError


def getargs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', nargs="*", help="URL.", required=True)
	return parser.parse_args()


def download_track(pre_path, track_id, track_title, track_number):
	logger_bugs.info("Downloading {}. {}".format(track_number, track_title))
	params = {
		"ConnectionInfo": connection_info,
		"api_key": config.credentials['api_key'],
		"overwrite_session": "Y",
		"track_id": track_id
	}
	r = requests.get(
		"http://api.bugs.co.kr/3/tracks/{}/listen/android/{}".format(track_id, config.prefs['audio_quality']),
		params=params, stream=True)
	r.raise_for_status()
	size = int(r.headers.get('content-length', 0))
	with open(pre_path, 'wb') as f:
		with tqdm(total=size, unit='B',
		          unit_scale=True, unit_divisor=1024,
		          initial=0, miniters=1) as bar:
			for chunk in r.iter_content(32 * 1024):
				if chunk:
					f.write(chunk)
					bar.update(len(chunk))

def artist_rip(artist_id):
	meta = client.get_meta(type="artist", id=int(artist_id))
	for album in meta['list'][1]['artist_album']['list']:
		album_rip(album['album_id'])

def album_rip(album_id):
	"""
	:param id: String (Album ID)
	"""
	meta = client.get_meta(type="album", id=int(album_id))
	album_directory_name = "{} - {}".format(meta['list'][0]['album_info']['result']['artist_disp_nm'],
	                                        meta['list'][0]['album_info']['result']['title'])
	if config.prefs['artist_folders']:
		album_path = os.path.join(config.prefs['downloads_directory'],
		                          meta['list'][0]['album_info']['result']['artist_disp_nm'], album_directory_name, )
	else:
		album_path = os.path.join(config.prefs['downloads_directory'], album_directory_name)
	utils.make_dir(album_path)
	cover_path = os.path.join(album_path, config.prefs['cover_name'])
	download_cover(meta['list'][0]['album_info']['result']['img_urls'], cover_path)
	for track in meta['list'][0]['album_info']['result']['tracks']:
		pre_path = os.path.join(album_path, "{}. .BugsPy".format(track['track_no']))
		post_path = os.path.join(album_path, "{}. {}.{}".format(track['track_no'], track['track_title'],
		                                                        config.prefs['audio_quality']))
		if utils.exist_check(post_path):
			pass
		else:
			download_track(pre_path=pre_path, track_id=track['track_id'], track_title=track['track_title'],
			               track_number=track['track_no'])
			os.rename(pre_path, post_path)
			tag(album=meta, track=track, file_path=post_path, cover_path=cover_path)


def download_cover(imgs, cover_path):
	if utils.exist_check(cover_path):
		pass
	else:
		logger_bugs.info("Downloading cover artwork.")
		cover_url = imgs[config.prefs['cover_size']]
		r = requests.get(cover_url)
		r.raise_for_status()
		with open(cover_path, 'wb') as f:
			f.write(r.content)

def get_lyrics(lyrics_tp, track_id):
	if lyrics_tp == "T" and config.prefs['lyrics_type']:
		url = 'https://music.bugs.co.kr/player/lyrics/T/{}'.format(str(track_id))
		r = requests.get(url)
		lyrics = r.json()['lyrics'].replace("＃", "\n")
		line_split = (line.split('|') for line in lyrics.splitlines())
		lyrics = ("\n".join(
			f'[{datetime.fromtimestamp(round(float(a), 2)).strftime("%M:%S.%f")[0:-4]}]{b}' for a, b in
			line_split))
	if lyrics_tp == "N" or config.prefs['lyrics_type'] == "N":
		url = 'https://music.bugs.co.kr/player/lyrics/N/{}'.format(str(track_id))
		r = requests.get(url)
		lyrics = r.json()['lyrics']
	if lyrics_tp is None:
		lyrics = ""
	return lyrics


def tag(album, track, file_path, cover_path):
	lyrics = get_lyrics(track['lyrics_tp'], track['track_id'])
	meta = utils.organize_meta(album=album, track=track, lyrics=lyrics)
	if str(file_path).endswith('.flac'):
		if cover_path:
			f_file = FLAC(file_path)
			f_image = Picture()
			f_image.type = 3
			f_image.desc = 'Front Cover'
			with open(cover_path, 'rb') as f:
				f_image.data = f.read()
			f_file.add_picture(f_image)
			f_file.save()
		# Add tags to the flac file
		f = FLAC(file_path)
		logger_bugs.debug("Writing tags to {}".format(os.path.basename(file_path)))
		for k, v in meta.items():
			f[k] = str(v)
		f.save()
	if str(file_path).endswith('.mp3'):
		legend = {
			"ALBUM": id3.TALB,
			"ALBUMARTIST": id3.TPE2,
			"ARTIST": id3.TPE1,
			"COMMENT": id3.COMM,
			"COMPOSER": id3.TCOM,
			"COPYRIGHT": id3.TCOP,
			"DATE": id3.TDRC,
			"GENRE": id3.TCON,
			"ISRC": id3.TSRC,
			"LABEL": id3.TPUB,
			"PERFORMER": id3.TOPE,
			"TITLE": id3.TIT2,
			"LYRICS": id3.USLT
		}
		try:
			audio = id3.ID3(file_path)
		except ID3NoHeaderError:
			audio = id3.ID3()
		logger_bugs.info("Writing tags to {}".format(os.path.basename(file_path)))
		for k, v in meta.items():
			try:
				id3tag = legend[k]
				audio[id3tag.__name__] = id3tag(encoding=3, text=v)
			except KeyError:
				pass
		if cover_path:
			with open(cover_path, 'rb') as cov_obj:
				audio.add(id3.APIC(3, 'image/jpg', 3, '', cov_obj.read()))
			audio.save(file_path, 'v2_version=3')

def main():
	for url in args.u:
		id = utils.get_id(url)
		if "album" in url:
			album_rip(album_id=id)
		elif "artist" in url:
			artist_rip(artist_id=id)


if __name__ == "__main__":
	logger.log_setup()
	logger_bugs = logging.getLogger("Bugs")
	client = client.Client()
	connection_info = client.auth()
	args = getargs()
	main()
