#!/usr/bin/env python

import re
import os
import Tkinter, tkFileDialog

import numpy
import libtiff

from winspec import Lightfield

def subtract_mean(filename, dst_dir=None, discard_frames=[0], print_every=10):
    root, name = os.path.split(filename)
    if dst_dir is None:
        dst_dir = root

    name_base = re.sub("\.spe", "", name)
    mean_filename = os.path.normpath(os.path.join(dst_dir,
                                 "{}_mean_background.tif".format(name_base)))
    max_filename = os.path.normpath(os.path.join(dst_dir,
                                "{}_max_mean_background.tif".format(name_base)))
    
    lf = Lightfield(filename)

    frames = list()
        
    for frame_index, frame in enumerate(lf.frames()):
        if frame_index % print_every == 0:
            print("Frame {} of {}".format(frame_index, lf.n_frames()))
        
        if frame_index in discard_frames:
            continue
            
        frames.append(numpy.array(list(frame.regions[0].data())))

    frames = numpy.array(frames)            
    mean_frame = frames.sum(0)/frames.shape[0]
    frames -= mean_frame[None,:,:]

    print("Writing to {}".format(mean_filename))
    mean_image = libtiff.TIFFimage(frames.astype("int16"))
    mean_image.write_file(mean_filename, verbose=False)

    print("Writing to {}".format(max_filename))
    max_image = libtiff.TIFFimage(numpy.amax(frames.astype("int16"), axis=0))
    max_image.write_file(max_filename, verbose=False)
    
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.withdraw()
    
    filenames = root.tk.splitlist(tkFileDialog.askopenfilenames(
        title="Choose files to process",
        filetypes=[("Winspec/Lightfield files", "*.spe")]))
##    filenames = ["blargh.spe"]

    dst_dir = tkFileDialog.askdirectory(title="Choose a destination directory")

    for filename in filenames:
        print("Processing {}".format(filename))
        subtract_mean(filename, dst_dir=dst_dir, print_every=40)   
        
        
