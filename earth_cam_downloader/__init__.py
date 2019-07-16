import time
from datetime import timedelta

from earth_cam_downloader.m3u8_downloader import M3U8Downloader


class EarthCamDownloader(object):

    M3U8_URL = "https://video2archives.earthcam.com/archives/_definst_/MP4:network/%s/%s.mp4/playlist.m3u8"
    M3U8_FILEPATH = "%s/%s-%s.%s"

    def __init__(self, cam_id, cam_name, start, end, file_format, output_dir):
        self.cam_id = str(cam_id)
        self.cam_name = cam_name
        self.file_format = file_format
        self.start = start
        self.end = end
        self.output_dir = output_dir

    def download(self):
        for url, filepath in zip(self.urls, self.filepaths):
            started_at = time.time()
            print(f"INFO: Downloading {url} to {filepath}")
            m3u8 = M3U8Downloader(uri=url, select_first_playlist=True)
            m3u8.download(filepath)
            ended_at = time.time()
            print(f"INFO: Downloaded {filepath} in {round((ended_at -  started_at) / 60, 2)} minutes.")

    @property
    def urls(self):
        return map(self._gen_m3u8_url_for_datetime, self.date_range)

    @property
    def filepaths(self):
        return map(self._gen_filepath_for_datetime, self.date_range)

    @property
    def date_range(self):
        return list(
            set(
                [
                    (self.start + timedelta(hours=n)).replace(
                        minute=0, second=0, microsecond=0
                    )
                    for n in range(int((self.end - self.start).seconds / 3600) + 1)
                ]
            )
        )

    def _gen_m3u8_url_for_datetime(self, dt):
        return self.M3U8_URL % (self.cam_id, dt.strftime("%Y/%m/%d/%H00"))

    def _gen_filepath_for_datetime(self, dt):
        return self.M3U8_FILEPATH % (
            self.output_dir,
            self.cam_name,
            dt.strftime("%Y-%m-%d-%H00"),
            self.file_format,
        )
