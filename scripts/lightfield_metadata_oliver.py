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

import winspec

def get_files(search_root, suffix):
    parser = re.compile("{}$".format(suffix),
                        re.IGNORECASE)
    
    for root, dirs, filenames in os.walk(search_root):
        for filename in filenames:
            if parser.search(filename):
                yield(os.path.join(root, filename))

def match_spe_tiff_files(spe_files, tiff_files):
    """
    For each spe file, find any associated tiff file by checking that they
    share the same filename.
    """
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
    keys = [("Exposure start", "exposure_start"),
            ("Exposure stop", "exposure_stop"),
            ("Exposure time", "exposure_time"),
            ("Gain", "gain"),
            ("AD rate", "ad_rate"),
            ("Frame rate", "frame_rate"), 
            ("Temperature set", "temperature_set"),
            ("Temperature read", "temperature_read"),
            ("Background file", "background_file")]
    
    with open(database_filename, "w") as stream_out:
        writer = csv.writer(stream_out)

        fields = ["Filename"] + list(map(lambda x: x[0], keys))
        writer.writerow(fields)
        
        for filename in spe.keys():
            w = winspec.Lightfield(filename)

            my_row = [filename]
            
            for name, key in keys:
                my_row.append(getattr(w, key)())

            writer.writerow(my_row)        

if __name__ == "__main__":
    spe_directory = "/home/tsbischof/src/winspec"
    tiff_directory = "/home/tsbischof/Documents/src/winspec"

    spe_files = get_files(spe_directory, "spe")
    tiff_files = get_files(spe_directory, "tiff")

    spe_database = match_spe_tiff_files(spe_files, tiff_files)

    write_metadata_database(spe_database,
                            "/home/tsbischof/src/winspec/scripts/oliver.csv")
##    write_metadata_to_tiff(spe_database)
    