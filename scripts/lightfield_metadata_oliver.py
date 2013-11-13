"""
This script is designed to gather and report on the metadata contained within
spe files, particularly for specifications set by Oliver Bruns. It is
designed to:
1. Find all spe files.
2. For each spe file, find the associated exported tiff files.
3. For each spe file, update a central database of metadata.
4. For each tiff file, add the metadata from the corresponding spe file.
"""

import os
import csv
import re
import getpass
import logging
from xml.parsers.expat import ExpatError

import winspec

def get_files(search_root, suffix):
    logging.info("Searching for {} files.".format(suffix))
    parser = re.compile("{}$".format(suffix),
                        re.IGNORECASE)
    
    for root, dirs, filenames in os.walk(search_root):
        for filename in filenames:
            if parser.search(filename):
                name = os.path.join(root, filename)
                logging.debug("Found {0}".format(name))
                yield(name)

def match_spe_tiff_files(spe_files, tiff_files):
    """
    For each spe file, find any associated tiff file by checking that they
    share the same filename.
    """
    logging.info("Matching spe and tiff files.")
    spe = dict()

    my_spe_files = list(spe_files)
    my_tiff_files = list(tiff_files)

    for spe_filename in my_spe_files:
        spe[spe_filename] = list()
        spe_name = re.sub("\.spe$", "", os.path.split(spe_filename)[1],
                          re.IGNORECASE)

        for tiff_filename in my_tiff_files:
            if re.search(spe_name, tiff_filename):
                spe[spe_filename].append(tiff_filename)
                my_tiff_files.remove(tiff_filename)

    return(spe)

def write_metadata_database(spe, database_filename):
    """
    For each spe file, write an entry to a csv file which includes the pertinent
    metadata.
    """
    logging.info("Writing database of metadata of {} files.".format(len(
        spe.keys())))
    keys = [("Exposure start", "exposure_start"),
            ("Exposure stop", "exposure_stop"),
            ("Exposure time", "exposure_time"),
            ("Gain", "gain"),
            ("AD rate", "ad_rate"),
            ("Frame rate", "frame_rate"),
            ("Readout Time", "readout_time"),
            ("Temperature set", "temperature_set"),
            ("Temperature read", "temperature_read"),
            ("Background file", "background_file"),
            ("Number of frames", "n_frames"),
            ("Frames per readout", "frames_per_readout")]
    
    with open(database_filename, "wb") as stream_out:
        writer = csv.writer(stream_out)

        fields = ["Filename"] + list(map(lambda x: x[0], keys))
        writer.writerow(fields)
        
        for filename in sorted(spe.keys()):
            try:
                w = winspec.Lightfield(filename)

                my_row = [filename]
                
                for name, key in keys:
                    my_row.append(getattr(w, key)())

                writer.writerow(my_row)
            except ExpatError:
                print("Failed to parse xml for {}".format(filename))
                continue

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if getpass.getuser() == "tsbischof":
        spe_directory = "/home/tsbischof/src/winspec"
        tiff_directory = spe_directory
        report_filename = "/home/tsbischof/src/winspec/scripts/oliver.csv"
    else:
        spe_directory = r"E:\raw_data"
        tiff_directory = spe_directory
        report_filename = r"C:\Users\Oliver\Desktop\data_processing\thomas_script_results\oliver.csv"

    spe_files = get_files(spe_directory, "spe")
    tiff_files = get_files(spe_directory, "tiff")

    spe_database = match_spe_tiff_files(spe_files, tiff_files)

    write_metadata_database(spe_database, report_filename)
##    write_metadata_to_tiff(spe_database)
    
