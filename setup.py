#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

package_name = "earth-cam-downloader"
package_version = "0.0.1"

setup(
    name=package_name,
    version=package_version,
    description="A downloader for m3u8 files from EarthCam",
    author="Brian Abelson",
    author_email="brianabelson@gmail.com",
    url="https://github.com/abelsonlive/earthcam-downloader",
    packages=find_packages()
)
