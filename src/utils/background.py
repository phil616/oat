"""
    filename: utils/background.py
    ~~~~~~~~~~~~~~~~~~~~
    Some background tasks and threads.

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""

import os
import glob
import time


def monitor_directory(directory: os.PathLike):
    while True:
        files = glob.glob(os.path.join(directory, '*'))
        if len(files) > 12:
            # sort files by creation time
            files.sort(key=os.path.getctime)
            # delete oldest file
            os.remove(files[0])
            print(f"Removed: {files[0]}")
        time.sleep(1)  # check every second
