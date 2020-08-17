import argparse
import logging
import os
import sys
import requests
from tqdm import tqdm
from modules import logger, client, utils, config

def getargs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', nargs="*", help="URL.", required=True)
	return parser.parse_args()

def download_track(album_path, track_id, track_title, track_number):
	url = "https://api.bugs.co.kr/3/tracks/{}/listen/android/{}?api_key={}&track_id={}&overwrite_session=Y&{}".format(track_id, config.prefs['audio_quality'], config.credentials['api_key'], track_id, config.credentials['cookie'])
	print(url)
	r = requests.get(url, stream=True)
	r.raise_for_status()
	size = int(r.headers.get('content-length', 0))
	filename = "{}. {}.{}".format(track_number, track_title, config.prefs['audio_quality'])
	file_location = os.path.join(album_path, filename)
	with open(file_location, 'wb') as f:
		with tqdm(total=size, unit='B',
		          unit_scale=True, unit_divisor=1024,
		          initial=0, miniters=1) as bar:
			for chunk in r.iter_content(32 * 1024):
				if chunk:
					f.write(chunk)
					bar.update(len(chunk))

def album_rip(album_id):
	"""
	:param id: String (Album ID)
	"""
	meta = client.Client().get_meta(type="album", id=int(album_id))
	# Create album directory
	if config.prefs['artist_folders']:
		album_path = os.path.join(config.prefs['downloads_directory'])
		utils.make_dir(album_path)
	for track in meta['list'][0]['album_info']['result']['tracks']:
		download_track(album_path=album_path, track_id=track['track_id'], track_title=track['track_title'], track_number=track['track_no'])
		sys.exit()

def main():
	for url in args.u:
		album_id = utils.get_id(url)
		album_rip(album_id)


if __name__ == "__main__":
	args = getargs()
	logger.log_setup()
	logger_bugs = logging.getLogger("Bugs")
	main()
