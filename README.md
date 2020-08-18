<p align="center">
  <img src="https://file.bugsm.co.kr/wbugs/common/header/logo_bugs.png?_t_s_=20200818-0850">
</p>  
<p align="center">
  <img src="https://img.shields.io/github/issues/Slyyxp/BugsPy?style=for-the-badge">  
  <img src="https://img.shields.io/github/languages/code-size/slyyxp/BugsPy?style=for-the-badge">  
  <img src="https://img.shields.io/maintenance/yes/2020?style=for-the-badge">  
</p>  

## Overview
**BugsPy** is a tool for downloading streamable tracks from **[Bugs.co.kr](https://music.bugs.co.kr/)**

Tested on **[Python 3.8.0](https://www.python.org/downloads/release/python-380/)**

Project structure based on **[GeniePy](https://github.com/Slyyxp/GeniePy)**

## Prerequisites

- Python 3.6+
- Bugs.co.kr Subscription 

## Features

- 16bit Lossless Support
- Artist Batching
- Bugs.co.kr Client
- Extensive Tagging
- Timed Lyrics

## Subscribing
### [Wiki](https://github.com/Slyyxp/BugsPy/wiki/Foreign-Subscriptions.-(iOS))

## Installation & Setup

```console
$ git clone https://github.com/Slyyxp/BugsPy.git
$ cd BugsPy
$ pip install -r requirements.txt
```

* Insert username and password into config.py.example  
* Optionally add the device id & user agent of your own android device
* Rename config.py.example to config.py

## Command Usage
```
python bugs.py -u {album_url}
```
Command  | Description  | Example
------------- | ------------- | -------------
-u | Bugs Url (Required) | `https://music.bugs.co.kr/album/20343816`, `https://music.bugs.co.kr/artist/80327433`

## config.py

**credentials:**

Config  | Description  | Example
------------- | ------------- | -------------
username | Bugs Email | `Slyyxp@domain.com`
password |Bugs Password | `ReallyBadPassword123`
device_id | Android Device ID | `eb9d53a3c424f961`
user_agent | User Agent | `Mobile/Bugs/4.11.30/Android/5.1.1/SM-G965N/samsung/market`

**prefs:**

Config  | Description  | Example
------------- | ------------- | -------------
download_directory | Directory to download files to | `Z:/BugsPy/downloads`
log_directory | Directory to save log files to  | `Z:/BugsPy/logs`
audio_quality | Default download format (flac, mp3) | `flac`, `mp3`
artist_folders | Whether or not to nest downloads into artist folders | `True/False`
cover_size | Size of cover art to download + embed | `original`, `200`, `140`, `1000`, `350`, `75`, `500`
cover_name | Name of cover art with jpg extension | `cover.jpg`, `folder.jpg`

## Disclaimer
- The usage of this script **may be** illegal in your country. It's your own responsibility to inform yourself of Copyright Law.