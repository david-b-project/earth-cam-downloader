"""
M3U8 Downloader
Download the ts files according to the given m3u8 file.
"""
import argparse
import os

import ffmpy
import m3u8


class M3U8Downloader:
    """M3U8 Downloader Class"""

    def __init__(
        self,
        uri,
        timeout=None,
        headers=None,
        select_first_playlist=False,
        ffmpeg_path="ffmpeg",
        ffmpeg_loglevel="quiet",
    ):
        """Initialize a M3U8 Downloader.
        Args:
            uri (:obj:`str`): The URI of the m3u8 file.
            timeout (:obj:`int`, optional): The timeout used when loading
                from uri. Defaults to ``None``.
            headers (:obj:`list` of :obj:`str`, optional): The headers used
                when loading from uri. Defaults to ``None``.
            ffmpeg_path (:obj:`str`, optional): The path to ffmpeg executable.
                Defaults to ``ffmpeg``.
            ffmpeg_loglevel (:obj:`str`, optional): The logging level of
                ffmpeg. Defaults to ``quiet``.
            select_first_playlist(:obj:`boolean`, optional): Whether or not to simply select
                the first playlist for a variant m3u8 file.
        """
        if not headers:
            headers = {}

        self.uri = uri
        self.ffmpeg_path = ffmpeg_path
        self.ffmpeg_loglevel = ffmpeg_loglevel
        self.select_first_playlist = select_first_playlist
        self.m3u8 = m3u8.load(uri=uri, timeout=timeout, headers=headers)

    def download(self, output="output.ts"):
        """Start downloading and merging with the given m3u8 file.
        Args:
            output (:obj:`str`): The path to output. Defaults to ``output.ts``
        """
        if self.m3u8.is_variant:
            print("INFO: There are multiple m3u8 files listed in this file.")
            try:
                if self.select_first_playlist:
                    print("INFO: Simply selecting the first playlist to download...")
                    fetch_index = 0
                else:
                    print()
                    for index, playlist in enumerate(self.m3u8.playlists):
                        self._print_stream_info(playlist, index)
                    fetch_index = int(input("Index> "))

                downloader = M3U8Downloader(
                    self.m3u8.playlists[fetch_index].absolute_uri,
                    ffmpeg_path=self.ffmpeg_path,
                    ffmpeg_loglevel=self.ffmpeg_loglevel,
                )
                downloader.download(output)
            except (ValueError, IndexError):
                print("ERROR: Invalid index.")

        else:
            dirname = os.path.dirname(output)
            if dirname:
                os.makedirs(os.path.dirname(output), exist_ok=True)

            ffmpeg_cmd = ffmpy.FFmpeg(
                self.ffmpeg_path,
                "-y -loglevel {}".format(self.ffmpeg_loglevel),
                inputs={self.uri: None},
                outputs={output: "-c copy"},
            )
            print("INFO: Start downloading and merging with ffmpeg...")
            print(ffmpeg_cmd.cmd)

            ffmpeg_cmd.run()

    @staticmethod
    def _print_stream_info(playlist, index=0):
        print("INDEX: " + str(index))

        stream_info = playlist.stream_info
        if stream_info.bandwidth:
            print("Bandwidth: {}".format(stream_info.bandwidth))
        if stream_info.average_bandwidth:
            print("Average bandwidth: {}".format(stream_info.average_bandwidth))
        if stream_info.program_id:
            print("Program ID: {}".format(stream_info.program_id))
        if stream_info.resolution:
            print("Resolution: {}".format(stream_info.resolution))
        if stream_info.codecs:
            print("Codecs: {}".format(stream_info.codecs))
        print()
