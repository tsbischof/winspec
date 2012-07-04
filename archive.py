#!/usr/bin/env python

import subprocess
import os

if __name__ == "__main__":
    src_dir = "winspec"
    suffixes = [".c", ".py", ".m", ".txt"]
    archive_base = "winspec"
    zip_archive = "{0}.zip".format(archive_base)
    tar_archive = "{0}.tar.bz2".format(archive_base)

    to_archive = list()

    try:
        os.remove(zip_archive)
    except:
        pass

    try:
        os.remove(tar_archive)
    except:
        pass

    for root, dirs, filenames in os.walk(src_dir):
        for filename in filenames:
            if any(map(lambda suffix: filename.lower().endswith(suffix),\
                                       suffixes)):
                to_archive.append(os.path.join(root, filename))

    subprocess.Popen(["zip", zip_archive] + to_archive).wait()
    subprocess.Popen(["tar", "-vjcf", tar_archive] + to_archive).wait()
