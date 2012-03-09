import struct
import re

import cstruct

def parse_header(header):
    types = {'ExperimentTimeUTC':
             'HDRNAMEMAX':
             'CALIBRATION':
             'float': "f",
             'char': "c",
             'DWORD': "",
             'PulseFileName':
             'USERINFOMAX':
             'ROI':
             'DATEMAX':
             'WORD':
             'ydim':
             'unsigned':
             'long':
             'under', 'Date', '8', 'TIMEMA', 'AbsorbFileName', 'COMMENTMAX', '10', '6', 'xdim', 'LABELMAX', 'FlatField', 'blemish', 'background', 'date', 'BYTE', 'with', 'ROIMAX', 'FILEVERMAX', '11', 'sw_version', 'short', 'reverse', 'header', 'datatype', 'of', 'NumFrames', 'ExperimentTimeLocal', 'xlabel', 'double', 'ylabel'}
    
    parser = re.compile("\W*(?P<type>[^\W]+)\W*"
                        "(?P<name>[^\W]+)\W*"
                        "(?P<offset>[0-9]+)\W*"
                        "(?P<description>[^\W]+)")
    
    for line in header:
        parsed = parser.search(line)
        if parsed:
            types.add(parsed.group("type"))
##            print(parsed.group("type"), parsed.group("name"))
        else:
            pass
##            print("Could not parse: {0}".format(line))


if __name__ == "__main__":
    with open("WINHEAD.TXT") as header:
        print(parse_header(header))

        
