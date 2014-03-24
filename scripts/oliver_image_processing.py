#!/usr/bin/env python

import re
import os
import Tkinter, tkFileDialog

import numpy
import libtiff

from winspec import Lightfield

def subtract_mean(filename, dst_dir=None, discard_frames=[0]):
    dst_filename = re.sub("\.spe", "_mean_background.tif", filename,
                          re.IGNORECASE)

    if dst_dir is not None:
        dst_filename = os.path.join(dst_dir, dst_filename)
        
    lf = Lightfield(filename)

    frames = list()
        
    for frame_index, frame in enumerate(lf.frames()):
        if frame_index in discard_frames:
            continue
            
        frames.append(numpy.array(list(frame.regions[0].data())))

    frames = numpy.array(frames)            
    mean_frame = frames.sum(0)/frames.shape[0]
    frames -= mean_frame[None,:,:]

    dst_image = libtiff.TIFFimage(frames.astype("int16"))
    dst_image.write_file(dst_filename, verbose=False)    
    
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.withdraw()
    
    filenames = tkFileDialog.askopenfilenames(
        title="Choose files to process",
        filetypes=[("Winspec/Lightfield files", "*.spe")])

    dst_dir = tkFileDialog.askdirectory(title="Choose a destination directory")

    for filename in filenames:
        print("Processing {}".format(filename))
        subtract_mean(filename, dst_dir=dst_dir)   
        
        
