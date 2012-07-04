import struct
import collections
import operator
import xml.dom.minidom

lightfield_v3_0_header_t = [
    (1992, "file_header_ver", "f"),
    (678, "xml_footer_offset", "Q"),
    (108, "datatype", "h"),
    (42, "xdim", "H"),
    (656, "ydim", "H"),
    (1446, "NumFrames", "i"),
    (6, "xDimDet", "H"),
    (18, "yDimDet", "H"),
    (34, "noscan", "h"),
    (664, "lnoscan", "i"),
    (658, "scramble", "h"),
    (2996, "WinView_id", "i"),
    (4098, "lastvalue", "h")]

ENDIANNESS = "<"

DATATYPES = {
    6: "B",
    3: "H",
    2: "h",
    8: "I",
    1: "i",
    0: "f",
    5: "d",
    "MonochromeFloating32": "f",
    "MonochromeUnsigned16": "H",
    "MonochromeUnsigned32": "i",
    "Int64": "q",
    "Double": "d"}

FRAME_ATTR = ("Frame",
              [("calibrations", str),
               ("count", int),
               ("size", int),
               ("stride", int),
               ("metaFormat", str),
               ("pixelFormat", str),
               ("type", str)])
REGION_ATTR = ("Region",
               [("count", int),
                ("width", int),
                ("height", int),
                ("calibrations", str),
                ("type", str),
                ("size", int),
                ("stride", int)])

METADATA_ATTR = {
    "TimeStamp": [("event", str),
                  ("type", str),
                  ("bitDepth", int),
                  ("resolution", int),
                  ("absoluteTime", str)],
    "FrameTrackingNumber": [("bitDepth", int),
                            ("type", str)],
    "GateTracking": [("component", str),
                     ("type", str),
                     ("bitDepth", int),
                     ("monotonic", str)],
    "ModulationTracking": [("component", str),
                           ("type", str),
                           ("bitDepth", int),
                           ("monotonic", str)]
    }

def read_attr(attr, source, name=None):
    if not name:
        name = attr[0]
        attributes = attr[1]
    else:
        attributes = attr

        
    result = collections.namedtuple(name,
                                    map(operator.itemgetter(0),
                                        attributes))

    for my_name, my_type in attributes:
        try:
            setattr(result,
                    my_name,
                    my_type(source.getAttribute(my_name)))
        except ValueError:
            setattr(result,
                    my_name,
                    source.getAttribute(my_name))

    return(result)

class Region(object):
    def __init__(self,
                 region_format,
                 data):
        self._calibration_x = None
        self._calibration_y = None
        self._data = data
        self.height = region_format.height
        self.width = region_format.width

    def x(self):
        if not self._calibration_x:
            return(None)

    def y(self):
        if not self._calibration_y:
            return(None)

    def data(self):
        for i in range(self.height):
            yield(self._data[i*self.width:(i+1)*self.width])

class Frame(object):
    def __init__(self,
                 frame_format,
                 region_formats,
                 metadata_formats,
                 data):
        self.regions = list()
        self._calibrations = list()
        self.metadata = list()
        
        pixel_format = DATATYPES[frame_format.pixelFormat]

        for region_format in region_formats:
            raw_data = data.read(region_format.size)

            region_data = struct.unpack(
                "{0}{1}{2}".format(
                    ENDIANNESS,
                    region_format.size // struct.calcsize(pixel_format),
                    pixel_format),
                raw_data)

            self.regions.append(Region(region_format,
                                        region_data))

        metadata_id = frame_format.metaFormat
        for metadata_format in filter(lambda x:
                                      x.getAttribute("id") == metadata_id,
                                      metadata_formats):
            for item in metadata_format.childNodes:
                metadata_type = read_attr(
                    METADATA_ATTR[item.tagName],
                    item,
                    name=item.tagName)

                fmt = "{0}{1}".format(
                    ENDIANNESS,
                    DATATYPES[metadata_type.type])

                self.metadata.append(
                    struct.unpack(
                        fmt,
                        data.read(struct.calcsize(fmt))))

class Lightfield(object):
    def __init__(self, filename):
        self.filename = filename
        self._header = None
        self._footer = None
        self._frames = None
        self._frame_formats = None

    def header(self):
        if not self._header:
            self._header = collections.namedtuple(
                "LightfieldHeader",
                map(operator.itemgetter(1),
                    lightfield_v3_0_header_t))
            
            with open(self.filename, "rb") as data_file:
                for offset, name, my_type in sorted(lightfield_v3_0_header_t):
                    my_type =  "{0}{1}".format(ENDIANNESS,
                                               my_type)

                    data_file.seek(offset)
                    setattr(self._header,
                            name,
                            struct.unpack(
                                my_type,
                                data_file.read(struct.calcsize(my_type))))

                    if len(getattr(self._header, name)) == 1:
                        setattr(self._header,
                                name,
                                getattr(self._header, name)[0])
            
        return(self._header)

    def footer(self):
        if not self._footer:
            with open(self.filename, "r") as data_file:
                data_file.seek(self.header().xml_footer_offset)
                
                self._footer = xml.dom.minidom.parseString(
                    data_file.read())

        return(self._footer)

    def frames(self):
        with open(self.filename, "rb") as data_file:
            data_file.seek(4100)

            # there are some number of data blocks, which contain
            # some number of frames, each of which contains some number
            # of regions and some amount of metadata. Read in each frame,
            # then parse the raw data to obtain the regions and metadata

            for data_block in self.frame_formats():
                for frame, regions, metadata in data_block:
                    for frame_number in range(frame.count):
                        yield(Frame(frame,
                                    regions,
                                    metadata,
                                    data_file))

    def frame_formats(self):
        if not self._frame_formats:
            self._frame_formats = list()

            for data_format in self.footer().getElementsByTagName("DataFormat"):
                self._frame_formats.append(list())
                for frame in filter(\
                    lambda x: x.getAttribute("type") == "Frame", \
                    data_format.getElementsByTagName("DataBlock")):

                    self._frame_formats[-1].append(
                        [read_attr(FRAME_ATTR, frame),
                         list(),
                         list()])

                    for region in filter( \
                        lambda x: \
                        x.getAttribute("type") == "Region",
                        frame.getElementsByTagName("DataBlock")):
                        
                        self._frame_formats[-1][-1][1].append(
                            read_attr(REGION_ATTR, region))

                    try:
                        # Get the metadata associated with the frame
                        for meta_format in \
                            frame.getAttribute("metaFormat").split(","):
                            metadata = list(
                                filter(lambda x:
                                       x.getAttribute("id") == meta_format,
                                       self.footer(
                                           ).getElementsByTagName(
                                               "MetaFormat")[
                                                   0].getElementsByTagName(
                                                   "MetaBlock")))[0]
                            
                            self._frame_formats[-1][-1][2].append(metadata)
                    except:
                        pass      

        return(self._frame_formats)

    def pixel_format(self):
        return(
            DATATYPES[
                self.footer().getElementsByTagName(
                    "DataFormat")[0].getElementsByTagName(
                        "DataBlock")[0].getAttribute("pixelFormat")])

if __name__ == "__main__":
    image = Lightfield("/home/tsbischof/Documents/"
                       "data/microscopy/20120523_InGaAs/"
                       "20120525/solution_emission 2012 "
                       "May 25 15_41_39 125.spe")

##    print(image.header())
##    print(image.footer())
##    print(image.pixel_format())
##    print(image.n_frames(), image.frame_height(), image.frame_width())
    for index, frame in zip(range(3), image.frames()):
        print(list(frame.regions[0].data())[0])

    a = image.frame_formats()
