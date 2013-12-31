# 
# Copyright (c) 2011-2014, Thomas Bischof
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the Massachusetts Institute of Technology nor the 
#    names of its contributors may be used to endorse or promote products 
#    derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
# 

import struct
import logging
import pprint

class CStruct(object):
    def __init__(self, definition):
        self.__definition = definition

    def __str__(self):
        result = list()
        # Change this to give a lisp-like output:
        # (name, value)
        # and so forth
        
        return(pprint.pformat(self.to_list()))
        
    def from_stream(self, data):
        stream_to_tuple(data, self.__definition, self)

    def to_list(self):
        result = list()
        for name, form in self.__definition:
            try:
                value = getattr(self, name)

                if isinstance(value, tuple):
                    for index, f in enumerate(value):
                        result.append(("{0}[{1}]".format(name, index),
                                      f.to_list()))
                elif isinstance(value, CStruct):
                    result.append((name, value.to_list()))
                else:
                    result.append((name, value))
            except AttributeError:
                logging.debug("Attribute not found: {0}".format(name))
                result.append((name, None))

        return(result)

    def definition(self):
        return(self.__definition)

def add_tab(string, tabs=1):
    result = str()
    for line in string.split("\n"):
        result += "\t{0}\n".format(line)

    return(result)

def strip_null(string):
    return(string.rstrip("\x000").lstrip("\x000"))

def stream_to_tuple(data, structure_definition, target):
    """Given the structure of interest, populates the named tuple with the
appropriate data. Ideally, this could be done with tuple._make(struct.unpack())),
but strings do not seem to work properly in this case."""
    for index, definition in enumerate(structure_definition):
        logging.debug(definition)
        name, form = definition
        number, formtype = form
        logging.debug("{0}: {1}".format(name, form))

        if type(formtype) == type(str()):
            # We have a string format, so no recursion
            formstr = "{0}{1}".format(number, formtype)
            logging.debug("Reading {0} ({1}) from stream at offset {2}.".format(
                name, formstr, data.tell()))

            size = struct.calcsize(formstr)
            my_data = data.read(size)
            value = struct.unpack_from(formstr, my_data)

            logging.debug("Found: {0}".format(value))

            # Now that we have the data, we need to consider whether it is an
            # array or a single value. If a character array, create a string.
            # If a numerical array, make a list. If a single value, make a
            # single value
            if form[-1] in "?bBhHiIlLqQfdP":
                logging.debug("Numerical value.")
                # Numerical value
                if form[0] == 1:
                    # Single value
                    value = value[0]
                else:
                    value = list(value)
            else:
                # Character value
                # Kludge to get rid of "\x00". This should be possible using nicer
                # methods.
                logging.debug("Character value.")
                value = strip_null(bytes("".encode()).join(value).decode())

            logging.debug("{0}: {1}".format(name, value))
                
            setattr(target, name, value)
        else:
            # Recursion!
            logging.debug("Recursing!")
            if number == 1:
                setattr(target, name, CStruct(formtype))
                stream_to_tuple(data, formtype, getattr(target, name))
            else:
                setattr(target, name, tuple([CStruct(formtype)
                                             for i in range(number)]))
                for i in range(number):
                    stream_to_tuple(data, formtype, getattr(target, name)[i])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    blargh_t = [
        ("blargh", (20, "i")),
        ("cool", (10, "c"))]

    nyargh_t = [
        ("nyargh", (2, "c")),
        ("fjord", (10, blargh_t))]


    a = CStruct(nyargh_t)

    with open("WINHEAD.TXT", "rb") as data:
        a.from_stream(data)

    print(a)
