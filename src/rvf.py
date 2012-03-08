#!/usr/bin/env python

import os
import struct
import collections
import csv
import re
import ctypes

import PIL.Image
import numpy

rvf_file_header_v0_t = \
               [("magic_identifier", "4c"),
                ("magic_number", "H"),
                ("version_major", "B"),
                ("version_minor", "B"),
                ("file_header_bytes", "I"),
                ("frame_header_bytes", "I"),
                ("frame_header_version", "I"),
                ("image_size", "I"),
                ("image_width", "I"),
                ("image_height", "I"),
                ("image_bpp", "B"),
                ("image_type", "B"),
                ("image_rotate", "B"),
                ("image_flip", "B"),
                ("image_fps", "f"),
                ("image_testpixels_preimage", "I"),
                ("image_testpixels_postimage", "I"),
                ("reserved", "{0}c".format(1024-256-48)),
                ("file_creator", "256c"),
                ("camera_description", "1024c"),
                ("camera_settings", "2048c"),
                ("owner_description", "2048c"),
                ("comment_description", "2048c"),
                ("padding", "{0}c".format(65536-8192))]

rvf_frame_header_v0_t = \
               [("identifier", "16c"),
                ("version", "I"),
                ("number", "I"),
                ("ticks", "Q"),
                ("ts_tz", "h"),
                ("ts_year", "H"),
                ("ts_month", "H"),
                ("ts_day", "H"),
                ("ts_hour", "H"),
                ("ts_minute", "H"),
                ("ts_second", "H"),
                ("ts_millisecond", "H"),
                ("padding", "{0}c".format(4096-48))]

class RVF:
    def __init__(self, filename, src_pixel_format="H",
                 dst_pixel_type="int16", dst_dir=None,
                 dst_image_type="tiff", dst_name_format=None):
        self.src_pixel_format = src_pixel_format
        
        self.filename = filename
        if dst_dir == None:
            dst_dir = re.sub("\.rvf$", "", filename)
        self.dst_dir = dst_dir
        self.name = os.path.split(self.dst_dir)[1]

        if dst_name_format == None:
            dst_name_format = "frame_{0:010d}"
        self.dst_name_format = dst_name_format

        self.file_header = definition_to_tuple("rvf_file_header_v0_t",
                                            rvf_file_header_v0_t)
        self.frame_header = definition_to_tuple("rvf_frame_header_v0_t",
                                            rvf_frame_header_v0_t)
        self.frame_data = None
        
        self.rvf_file = None
        self.metadata_file = None

        self.dst_pixel_type = dst_pixel_type
        self.dst_image_type = dst_image_type

    def __str__(self):
        return(self.name)

    def read_file_header(self):
        stream_to_tuple(self.rvf_file, rvf_file_header_v0_t, self.file_header)

    def read_frame_header(self):
        stream_to_tuple(self.rvf_file, rvf_frame_header_v0_t, self.frame_header)

    def read_frame_data(self):
        form = "{0}{1}".format(self.file_header.image_size, self.src_pixel_format)
        raw = struct.unpack_from(form,
                                self.rvf_file.read(struct.calcsize(form)))
        self.frame_data = numpy.array(raw).reshape(
                                (self.file_header.image_height,
                                 self.file_header.image_width)
                                ).astype(self.dst_pixel_type)

    def frames(self):
        while True:
            try:
                self.read_frame_header()
                self.read_frame_data()
                yield(self.frame_header, self.frame_data)              
            except:
                break
        
    def frame_to_file(self, frame_data, frame_name, image_format):
##        pass
        dst = "{0}.{1}".format(frame_name, image_format)
        image = PIL.Image.fromarray(frame_data)
        image.save(dst)

    def metadata_to_file(self, key, metadata):
##        pass
        if self.do_write:
            writer = csv.writer(self.metadata_file)
            for attribute in sorted(metadata._fields):
                writer.writerow([key, attribute, getattr(metadata, attribute)])

    def to_frames(self):             
        try:
            os.makedirs(self.dst_dir)
        except:
            if not os.path.isdir:
                raise(OSError(
                    "Could not create {0} for output from {1}.".format(
                    self.dst_dir, self.filename)))
            else:
                pass

        metadata_filename = os.path.join(self.dst_dir,
                                          "{0}.metadata".format(self.name))

        with open(self.filename, "rb") as self.rvf_file:
            with open(metadata_filename, "w") as self.metadata_file:
                # Read the file header and write its content to a text file.
                self.read_file_header()
                self.metadata_to_file("file_header", self.file_header)

                # Read frames, write metadata to file, and write frames to
                # individual files. 
                for frame_number, frame in enumerate(self.frames()):
                    print("{0}: {1:010d}".format(self.name, frame_number))
                    header, data = frame
                    
                    name = self.dst_name_format.format(frame_number)
                    self.metadata_to_file(name, header)

                    self.frame_to_file(data, os.path.join(self.dst_dir,
                                                          name),
                                       self.dst_image_type)

def definition_to_tuple(tuple_name, definition):
    names = list(map(lambda x: x[0], definition))
    return(collections.namedtuple(tuple_name, names))

def stream_to_tuple(data, structure_definition, target_tuple):
    """Given the structure of interest, populates the named tuple with the
appropriate data. Ideally, this could be done with tuple._make(struct.unpack())),
but strings do not seem to work properly in this case."""
    for name, form in structure_definition:
        value = struct.unpack(form, data.read(struct.calcsize(form)))

        # Now that we have the data, we need to consider whether it is an array
        # or a single value. If a character array, create a string. If a
        # numerical array, make a list. If a single value, make a single value
        if form[-1] in "?hHiIlLqQfdP":
            # Numerical value
            if len(form) == 1:
                # Single value
                value = value[0]
            else:
                value = list(value[:-1])
        else:
            # Character value
            # Kludge to get rid of "\x00". This should be possible using nicer
            # methods.
            value = bytes('').join(value[:-1]).encode().rstrip("\x00")
            
        setattr(target_tuple, name, value)

if __name__ == "__main__":
    data_root = "/home/tsbischof/Documents/data/raytheon"
    rvf_files = list()

    for root, dirs, files in os.walk(data_root):
        for filename in files:
            if filename.endswith(".rvf"):
                rvf_files.append(os.path.join(root, filename))

    for rvf_filename in rvf_files:
        rvf = RVF(rvf_filename)
        rvf.to_frames()
