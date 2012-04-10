import struct
import re
import logging
import os

import matplotlib.pyplot as plt

import cstruct

winspec_ROI_t = [
    ("startx", (1, "H")),
    ("endx", (1, "H")),
    ("groupx", (1, "H")),
    ("starty", (1, "H")),
    ("endy", (1, "H")),
    ("groupy", (1, "H"))]

winspec_calibration_t = [
    ("offset", (1, "d")),
    ("factor", (1, "d")),
    ("current_unit", (1, "c")),
    ("reserved1", (1, "c")),
    ("string", (40, "c")),
    ("reserved2", (40, "c")),
    ("calib_valid", (1, "c")),
    ("input_unit", (1, "c")),
    ("polynom_unit", (1, "c")),
    ("polynom_order", (1, "c")),
    ("calib_count", (1, "c")),
    ("pixel_position", (10, "d")),
    ("calib_value", (10, "d")),
    ("polynom_coeff", (6, "d")),
    ("laser_position", (1, "d")),
    ("reserved3", (1, "c")),
    ("new_calib_flag", (1, "B")),
    ("calib_label", (81, "c")),
    ("expansion", (87, "c"))]

winspec_header_t = [
    ("ControllerVersion", (1, "h")),
    ("LogicOutput", (1, "h")),
    ("AmpHiCapLowNoise", (1, "H")),
    ("xDimDet", (1, "H")),
    ("mode", (1, "h")),
    ("exp_sec", (1, "f")),
    ("VChipXdim", (1, "h")),
    ("VChipYdim", (1, "h")),
    ("yDimDet", (1, "H")),
    ("date", (10, "c")),
    ("VirtualChipFlag", (1, "h")),
    ("Spare_1", (2, "c")),
    ("noscan", (1, "h")),
    ("DetTemperature", (1, "f")),
    ("DetType", (1, "h")),
    ("xdim", (1, "H")),
    ("stdiode", (1, "h")),
    ("DelayTime", (1, "f")),
    ("ShutterControl", (1, "H")),
    ("AbsorbLive", (1, "h")),
    ("AbsorbMode", (1, "H")),
    ("CanDoVirtualChipFlag", (1, "h")),
    ("ThresholdMinLive", (1, "h")),
    ("ThresholdMinVal", (1, "f")),
    ("ThresholdMaxLive", (1, "h")),
    ("ThresholdMaxVal", (1, "f")),
    ("SpecAutoSpectroMode", (1, "h")),
    ("SpecCenterWlNm", (1, "f")),
    ("SpecGlueFlag", (1, "h")),
    ("SpecGlueStartWlNm", (1, "f")),
    ("SpecGlueEndWlNm", (1, "f")),
    ("SpecGlueMinOvrlpNm", (1, "f")),
    ("SpecGlueFinalResNm", (1, "f")),
    ("PulserType", (1, "h")),
    ("CustomChipFlag", (1, "h")),
    ("XPrePixels", (1, "h")),
    ("XPostPixels", (1, "h")),
    ("YPrePixels", (1, "h")),
    ("YPostPixels", (1, "h")),
    ("asynen", (1, "h")),
    ("datatype", (1, "h")),
    ("PulserMode", (1, "h")),
    ("PulserOnChipAccums", (1, "H")),
    ("PulserRepeatExp", (1, "I")),
    ("PulseRepWidth", (1, "f")),
    ("PulseRepDelay", (1, "f")),
    ("PulseSeqStartWidth", (1, "f")),
    ("PulseSeqEndWidth", (1, "f")),
    ("PulseSeqStartDelay", (1, "f")),
    ("PulseSeqEndDelay", (1, "f")),
    ("PulseSeqIncMode", (1, "h")),
    ("PImaxUsed", (1, "h")),
    ("PImaxMode", (1, "h")),
    ("PImaxGain", (1, "h")),
    ("BackGrndApplied", (1, "h")),
    ("PImax2nsBrdUsed", (1, "h")),
    ("minblk", (1, "H")),
    ("numminblk", (1, "H")),
    ("SpecMirrorLocation", (2, "h")),
    ("SpecSlitLocation", (4, "h")),
    ("CustomTimingFlag", (1, "h")),
    ("ExperimentTimeLocal", (7, "c")),
    ("ExperimentTimeUTC", (7, "c")),
    ("ExposUnits", (1, "h")),
    ("ADCoffset", (1, "H")),
    ("ADCrate", (1, "H")),
    ("ADCtype", (1, "H")),
    ("ADCresolution", (1, "H")),
    ("ADCbitAdjust", (1, "H")),
    ("gain", (1, "H")),
    ("Comments", (5, [("comment", (80, "c"))])),
    ("geometric", (1, "H")),
    ("xlabel", (16, "c")),
    ("cleans", (1, "H")),
    ("NumSkpPerCln", (1, "H")),
    ("SpecMirrorPos", (2, "h")),
    ("SpecSlitPos", (4, "f")),
    ("AutoCleansActive", (1, "h")),
    ("UseContCleansInst", (1, "h")),
    ("AbsorbStripNum", (1, "h")),
    ("SpecSlitPosUnits", (1, "h")),
    ("SpecGrooves", (1, "f")),
    ("srccmp", (1, "h")),
    ("ydim", (1, "H")),
    ("scramble", (1, "h")),
    ("ContinuousCleansFlag", (1, "h")),
    ("ExternalTriggerFlag", (1, "h")),
    ("lnoscan", (1, "i")),
    ("lavgexp", (1, "i")),
    ("ReadoutTime", (1, "f")),
    ("TriggeredModeFlag", (1, "h")),
    ("Spare_2", (10, "c")),
    ("sw_version", (16, "c")),
    ("type", (1, "h")),
    ("flatFieldApplied", (1, "h")),
    ("Spare_3", (16, "c")),
    ("kin_trig_mode", (1, "h")),
    ("dlabel", (16, "c")),
    ("Spare_4", (436, "c")),
    ("PulseFileName", (120, "c")),
    ("AbsorbFileName", (120, "c")),
    ("NumExpRepeats", (1, "I")),
    ("NumExpAccums", (1, "I")),
    ("YT_Flag", (1, "h")),
    ("clkspd_us", (1, "f")),
    ("HWaccumFlag", (1, "h")),
    ("StoreSync", (1, "h")),
    ("BlemishApplied", (1, "h")),
    ("CosmicApplied", (1, "h")),
    ("CosmicType", (1, "h")),
    ("CosmicThreshold", (1, "f")),
    ("NumFrames", (1, "i")),
    ("MaxIntensity", (1, "f")),
    ("MinIntensity", (1, "f")),
    ("ylabel", (16, "c")),
    ("ShutterType", (1, "H")),
    ("shutterComp", (1, "f")),
    ("readoutMode", (1, "H")),
    ("WindowSize", (1, "H")),
    ("clkspd", (1, "H")),
    ("interface_type", (1, "H")),
    ("NumROIsInExperiment", (1, "h")),
    ("Spare_5", (16, "c")),
    ("controllerNum", (1, "H")),
    ("SWmade", (1, "H")),
    ("NumROI", (1, "h")),
    ("ROI", (10, winspec_ROI_t)),
    ("FlatField", (120, "c")),
    ("background", (120, "c")),
    ("blemish", (120, "c")),
    ("file_header_ver", (1, "f")),
    ("YT_INFO", (1000, "c")),
    ("WinView_id", (1, "i")),
    ("x_calibration", (1, winspec_calibration_t)),
    ("y_calibration", (1, winspec_calibration_t)),
    ("Istring", (40, "c")),
    ("Spare_6", (25, "c")),
    ("SpecType", (1, "B")),
    ("SpecModel", (1, "B")),
    ("PulseBurstUsed", (1, "B")),
    ("PulseBurstCount", (1, "I")),
    ("PulseBurstPeriod", (1, "d")),
    ("PulseBracketUsed", (1, "B")),
    ("PulseBracketType", (1, "B")),
    ("PulseTimeConstFast", (1, "d")),
    ("PulseAmplitudeFast", (1, "d")),
    ("PulseTimeConstSlow", (1, "d")),
    ("PulseAmplitudeSlow", (1, "d")),
    ("AnalogGain", (1, "h")),
    ("AvGainUsed", (1, "h")),
    ("AvGain", (1, "h")),
    ("lastvalue", (1, "h"))]

types = {"float": "f",
         "char": "c",
         "BYTE": "B",
         "DWORD": "i",
         "WORD": "H",
         "long": "i",
         "short": "h",
         "double": "d"}

constants = {"HDRNAMEMAX": 120,
             "USERINFOMAX": 1000,
             "COMMENTMAX": 80,
             "LABELMAX": 16,
             "FILEVERMAX": 16,
             "DATEMAX": 10,
             "ROIMAX": 10,
             "TIMEMAX": 7}

data_types = ["", "f", "i", "h", "H"]
camera_types = ["", "new120", "old120", "ST130", "ST121", "ST138", "DC131",
                "ST133", "ST135", "VICCD", "ST117", "OMA3", "OMA4"]

winspec_header = cstruct.CStruct(winspec_header_t)

def parse_header(header):   
    parser = re.compile("\W*(?P<type>[A-Za-z^_^\[]+)\W+"
                        "(?P<name>[A-Za-z0-9\[\]]+)\W+"
                        "(?P<offset>[0-9]+)\W+"
                        "(?P<description>[^\W]+)")

    name_parser = re.compile("(?P<name>[^\[]+)\[(?P<number>[^\]]+)\]")
    
    for line in header:
        try:
            my_type, my_name = line.split()[0:2]

            name_parsed = name_parser.search(my_name)

            if name_parsed:
                name = name_parsed.group("name")
                number = name_parsed.group("number")
                print((name, (constants[number], types[my_type])), ",")
            else:
                print((my_name, (1, types[my_type])), ",")
        except:
            continue

class Winspec:
    def __init__(self, filename):
        self.__header = None
        self.__filename = filename
        self.__data_file = open(filename, "rb")
        self.__x = None
        self.__y = None

        self.header()

    def header(self):
        if self.__header == None:
            self.__header = cstruct.CStruct(winspec_header_t)
            self.__header.from_stream(self.__data_file)

            if self.__data_file.tell() != 4100:
                logging.error("Only read to {0}. "
                              "The header should stop at {1}.".format(
                                  self.__data_file.tell(), 4100))

        return(self.__header)

    def frames(self):
        data_type = data_types[self.header().datatype]

        n_frames = self.n_frames()
        frame_width = self.frame_width()
        frame_height = self.frame_height()

        line_format = "{0}{1}".format(frame_width, data_type)
        logging.info("Reading {0} frames, at {1}x{2}.".format(
            n_frames, frame_width, frame_height))
        logging.info("Format for a line: {0}.".format(line_format))

        for frame_number in range(n_frames):
            logging.info("Reading frame {0}.".format(frame_number))
            frame_data = list()
            for line_number in range(frame_height):
                logging.debug("Reading line {0}.".format(line_number))
                raw_data = self.__data_file.read(struct.calcsize(line_format))
                line_data = struct.unpack(line_format, raw_data)

                frame_data.append(line_data)

            if len(frame_data) == 1:
                yield(frame_data[0])
            else:
                yield(frame_data)

    def x(self):
        # Get the calibration out and print the axis values.
        if self.__x:
            return(self.__x)
        
        line = list()
        for pixel_index in range(self.header().xdim):
            result = 0
            for power, coefficient in enumerate(
                       self.header().x_calibration.polynom_coeff):
                result += coefficient*(pixel_index**power)
            line.append(result)

        self.__x = line
        return(line)
                
    def y(self):
        if self.__y:
            return(self.__y)
        
        line = list()
        for pixel_index in range(self.header().xdim):
            result = 0
            for power, coefficient in enumerate(
                       self.header().y_calibration.polynom_coeff):
                result += coefficient*(pixel_index**power)
            line.append(result)

        self.__y = line
        return(line)

    def x_label(self):
        return(self.header().x_calibration.string)

    def n_frames(self):
        return(self.header().NumFrames)

    def frame_width(self):
        return(self.header().xdim)

    def frame_height(self):
        return(self.header().ydim)

    def t(self):
        return(map(lambda x: x*self.header().exp_sec, range(self.n_frames())))

    def exposure_time(self):
        return(self.header().exp_sec)

    def to_file(self, filename):
        # Write the binary structure to file.
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
##    logging.basicConfig(level=logging.DEBUG)
    data = Winspec("../sample_data/TSB-01-152_photodarkening_000.SPE")

##    data_dir = "../sample_data"

##    for filename in filter(lambda x: x.lower().endswith(".spe"),
##                           os.listdir(data_dir)):
##        print(filename)
##        name_base = filename[:-4]
##        try:
##            os.mkdir(os.path.join(data_dir, name_base))
##        except:
##            pass
##
##        data = Winspec(os.path.join(data_dir, filename))
##
##        if data.frame_height() == 1:
##            for frame_number, frame in enumerate(data.data()):
##                plt.clf()
##                plt.plot(data.x(), frame)
##                plt.savefig(os.path.join(data_dir, name_base,
##                            "frame_{0:08d}.png".format(frame_number)))
##                
                
    print(data.header())

##    background = next(data.data())
##    
##    for frame_number, frame in enumerate(data.data()):
##        print("{0:8d}/{1}".format(frame_number, data.n_frames()-1))
##        plt.clf()
##        plt.plot(data.x(), map(lambda x,y: x-y, frame, background))
##        plt.xlim((min(data.x()), max(data.x())))
##        plt.ylim((0, 150))
##        plt.xlabel(data.x_label())
##        plt.savefig("images/frame_{0:08d}.png".format(frame_number))
    
##    frames = list()
##    for frame_number, frame in enumerate(data.data()):
##        print("{0:8d}/{1}".format(frame_number, data.n_frames()-1))
##        frames.append(frame)
##
##    plt.clf()
##    wavelengths = data.x()
##    times = data.t()
##    
##    plt.imshow(frames, extent=(min(wavelengths), max(wavelengths),
##                               max(times), min(times)),
##               vmin=500, vmax=800)
##    plt.xlabel(data.x_label())
##    plt.ylabel("Time/s")
##    plt.show()
##    
##
##        
##
