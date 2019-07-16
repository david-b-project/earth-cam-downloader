earth-cam-downloader
===================

This repository contains code for downloading archives of livestreams from [earthcam.com](https://www.earthcam.com/). 


## Installation

```
pipenv install 
pip3 install --editable .
```

## Usage 

You can see an example of a download script [here](script/times-square.py).

In order to find the camera id's, open up a network tab in chrome and monitor the `playlist.m3u8` url that gets fetched when requesting an archive of a camera. This url should look something like this:
```
https://video2archives.earthcam.com/archives/_definst_/MP4:network/9974/2019/07/16/0500.mp4/playlist.m3u8 to output/street-cam-2019-07-16-0500.mp4
```

The format of this url is:
```
https://video2archives.earthcam.com/archives/_definst_/MP4:network/{camera_id}/{year}/{month}/{day}/{hour}.mp4/playlist.m3u8
```

You should be able to use this method to download footage for every camera.

**NOTE**: Archives only go back 2-3 days.

