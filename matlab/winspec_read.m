% 
% Copyright (c) 2011-2014, Thomas Bischof
% All rights reserved.
% 
% Redistribution and use in source and binary forms, with or without 
% modification, are permitted provided that the following conditions are met:
% 
% 1. Redistributions of source code must retain the above copyright notice, 
%    this list of conditions and the following disclaimer.
% 
% 2. Redistributions in binary form must reproduce the above copyright notice, 
%    this list of conditions and the following disclaimer in the documentation 
%    and/or other materials provided with the distribution.
% 
% 3. Neither the name of the Massachusetts Institute of Technology nor the 
%    names of its contributors may be used to endorse or promote products 
%    derived from this software without specific prior written permission.
% 
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
% ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
% LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
% CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
% SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
% INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
% CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
% ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
% POSSIBILITY OF SUCH DAMAGE.
%

function winspec = winspec_read(filename)

file = fopen(filename, 'rb');

winspec = Winspec();

% Start reading through things. 
winspec.header.ControllerVersion = fread(file, 1, 'int16');
winspec.header.LogicOutput = fread(file, 1, 'int16');
winspec.header.AmpHiCapLowNoise = fread(file, 1, 'uint16');
winspec.header.xDimDet = fread(file, 1, 'uint16');
winspec.header.mode = fread(file, 1, 'int16');
winspec.header.exp_sec = fread(file, 1, 'float32');
winspec.header.VChipXdim = fread(file, 1, 'int16');
winspec.header.VChipYdim = fread(file, 1, 'int16');
winspec.header.yDimDet = fread(file, 1, 'uint16');
winspec.header.date = fread(file, 10, 'char');
winspec.header.VirtualChipFlag = fread(file, 1, 'int16');
winspec.header.Spare_1 = fread(file, 2, 'char');
winspec.header.noscan = fread(file, 1, 'int16');
winspec.header.DetTemperature = fread(file, 1, 'float32');
winspec.header.DetType = fread(file, 1, 'int16');
winspec.header.xdim = fread(file, 1, 'uint16');
winspec.header.stdiode = fread(file, 1, 'int16');
winspec.header.DelayTime = fread(file, 1, 'float32');
winspec.header.ShutterControl = fread(file, 1, 'uint16');
winspec.header.AbsorbLive = fread(file, 1, 'int16');
winspec.header.AbsorbMode = fread(file, 1, 'uint16');
winspec.header.CanDoVirtualChipFlag = fread(file, 1, 'int16');
winspec.header.ThresholdMinLive = fread(file, 1, 'int16');
winspec.header.ThresholdMinVal = fread(file, 1, 'float32');
winspec.header.ThresholdMaxLive = fread(file, 1, 'int16');
winspec.header.ThresholdMaxVal = fread(file, 1, 'float32');
winspec.header.SpecAutoSpectroMode = fread(file, 1, 'int16');
winspec.header.SpecCenterWlNm = fread(file, 1, 'float32');
winspec.header.SpecGlueFlag = fread(file, 1, 'int16');
winspec.header.SpecGlueStartWlNm = fread(file, 1, 'float32');
winspec.header.SpecGlueEndWlNm = fread(file, 1, 'float32');
winspec.header.SpecGlueMinOvrlpNm = fread(file, 1, 'float32');
winspec.header.SpecGlueFinalResNm = fread(file, 1, 'float32');
winspec.header.PulserType = fread(file, 1, 'int16');
winspec.header.CustomChipFlag = fread(file, 1, 'int16');
winspec.header.XPrePixels = fread(file, 1, 'int16');
winspec.header.XPostPixels = fread(file, 1, 'int16');
winspec.header.YPrePixels = fread(file, 1, 'int16');
winspec.header.YPostPixels = fread(file, 1, 'int16');
winspec.header.asynen = fread(file, 1, 'int16');
winspec.header.datatype = fread(file, 1, 'int16');
winspec.header.PulserMode = fread(file, 1, 'int16');
winspec.header.PulserOnChipAccums = fread(file, 1, 'uint16');
winspec.header.PulserRepeatExp = fread(file, 1, 'uint32');
winspec.header.PulseRepWidth = fread(file, 1, 'float32');
winspec.header.PulseRepDelay = fread(file, 1, 'float32');
winspec.header.PulseSeqStartWidth = fread(file, 1, 'float32');
winspec.header.PulseSeqEndWidth = fread(file, 1, 'float32');
winspec.header.PulseSeqStartDelay = fread(file, 1, 'float32');
winspec.header.PulseSeqEndDelay = fread(file, 1, 'float32');
winspec.header.PulseSeqIncMode = fread(file, 1, 'int16');
winspec.header.PImaxUsed = fread(file, 1, 'int16');
winspec.header.PImaxMode = fread(file, 1, 'int16');
winspec.header.PImaxGain = fread(file, 1, 'int16');
winspec.header.BackGrndApplied = fread(file, 1, 'int16');
winspec.header.PImax2nsBrdUsed = fread(file, 1, 'int16');
winspec.header.minblk = fread(file, 1, 'uint16');
winspec.header.numminblk = fread(file, 1, 'uint16');
winspec.header.SpecMirrorLocation = fread(file, 2, 'int16');
winspec.header.SpecSlitLocation = fread(file, 4, 'int16');
winspec.header.CustomTimingFlag = fread(file, 1, 'int16');
winspec.header.ExperimentTimeLocal = fread(file, 7, 'char');
winspec.header.ExperimentTimeUTC = fread(file, 7, 'char');
winspec.header.ExposUnits = fread(file, 1, 'int16');
winspec.header.ADCoffset = fread(file, 1, 'uint16');
winspec.header.ADCrate = fread(file, 1, 'uint16');
winspec.header.ADCtype = fread(file, 1, 'uint16');
winspec.header.ADCresolution = fread(file, 1, 'uint16');
winspec.header.ADCbitAdjust = fread(file, 1, 'uint16');
winspec.header.gain = fread(file, 1, 'uint16');
winspec.header.Comments = fread(file, [5, 80], 'char');
winspec.header.geometric = fread(file, 1, 'uint16');
winspec.header.xlabel = fread(file, 16, 'char');
winspec.header.cleans = fread(file, 1, 'uint16');
winspec.header.NumSkpPerCln = fread(file, 1, 'uint16');
winspec.header.SpecMirrorPos = fread(file, 2, 'int16');
winspec.header.SpecSlitPos = fread(file, 4, 'float32');
winspec.header.AutoCleansActive = fread(file, 1, 'int16');
winspec.header.UseContCleansInst = fread(file, 1, 'int16');
winspec.header.AbsorbStripNum = fread(file, 1, 'int16');
winspec.header.SpecSlitPosUnits = fread(file, 1, 'int16');
winspec.header.SpecGrooves = fread(file, 1, 'float32');
winspec.header.srccmp = fread(file, 1, 'int16');
winspec.header.ydim = fread(file, 1, 'uint16');
winspec.header.scramble = fread(file, 1, 'int16');
winspec.header.ContinuousCleansFlag = fread(file, 1, 'int16');
winspec.header.ExternalTriggerFlag = fread(file, 1, 'int16');
winspec.header.lnoscan = fread(file, 1, 'int32');
winspec.header.lavgexp = fread(file, 1, 'int32');
winspec.header.ReadoutTime = fread(file, 1, 'float32');
winspec.header.TriggeredModeFlag = fread(file, 1, 'int16');
winspec.header.Spare_2 = fread(file, 10, 'char');
winspec.header.sw_version = fread(file, 16, 'char');
winspec.header.type = fread(file, 1, 'int16');
winspec.header.flatFieldApplied = fread(file, 1, 'int16');
winspec.header.Spare_3 = fread(file, 16, 'char');
winspec.header.kin_trig_mode = fread(file, 1, 'int16');
winspec.header.dlabel = fread(file, 16, 'char');
winspec.header.Spare_4 = fread(file, 436, 'char');
winspec.header.PulseFileName = fread(file, 120, 'char');
winspec.header.AbsorbFileName = fread(file, 120, 'char');
winspec.header.NumExpRepeats = fread(file, 1, 'uint32');
winspec.header.NumExpAccums = fread(file, 1, 'uint32');
winspec.header.YT_Flag = fread(file, 1, 'int16');
winspec.header.clkspd_us = fread(file, 1, 'float32');
winspec.header.HWaccumFlag = fread(file, 1, 'int16');
winspec.header.StoreSync = fread(file, 1, 'int16');
winspec.header.BlemishApplied = fread(file, 1, 'int16');
winspec.header.CosmicApplied = fread(file, 1, 'int16');
winspec.header.CosmicType = fread(file, 1, 'int16');
winspec.header.CosmicThreshold = fread(file, 1, 'float32');
winspec.header.NumFrames = fread(file, 1, 'int32');
winspec.header.MaxIntensity = fread(file, 1, 'float32');
winspec.header.MinIntensity = fread(file, 1, 'float32');
winspec.header.ylabel = fread(file, 16, 'char');
winspec.header.ShutterType = fread(file, 1, 'uint16');
winspec.header.shutterComp = fread(file, 1, 'float32');
winspec.header.readoutMode = fread(file, 1, 'uint16');
winspec.header.WindowSize = fread(file, 1, 'uint16');
winspec.header.clkspd = fread(file, 1, 'uint16');
winspec.header.interface_type = fread(file, 1, 'uint16');
winspec.header.NumROIsInExperiment = fread(file, 1, 'int16');
winspec.header.Spare_5 = fread(file, 16, 'char');
winspec.header.controllerNum = fread(file, 1, 'uint16');
winspec.header.SWmade = fread(file, 1, 'uint16');
winspec.header.NumROI = fread(file, 1, 'int16');

% ROI
winspec.header.ROI = struct([]);
for i=1:10
    winspec.header.ROI(i).startx = fread(file, 1, 'uint16');
    winspec.header.ROI(i).endx = fread(file, 1, 'uint16');
    winspec.header.ROI(i).groupx = fread(file, 1, 'uint16');
    winspec.header.ROI(i).starty = fread(file, 1, 'uint16');
    winspec.header.ROI(i).endy = fread(file, 1, 'uint16');
    winspec.header.ROI(i).groupy = fread(file, 1, 'uint16');
end

winspec.header.FlatField = fread(file, 120, 'char');
winspec.header.background = fread(file, 120, 'char');
winspec.header.blemish = fread(file, 120, 'char');
winspec.header.file_header_ver = fread(file, 1, 'float32');
winspec.header.YT_INFO = fread(file, 1000, 'char');
winspec.header.WinView_id = fread(file, 1, 'int32');

% x calibration.
winspec.header.x_calibration = struct();
winspec.header.x_calibration.offset = fread(file, 1, 'float64');
winspec.header.x_calibration.factor = fread(file, 1, 'float64');
winspec.header.x_calibration.current_unit = fread(file, 1, 'char');
winspec.header.x_calibration.reserved1 = fread(file, 1, 'char');
winspec.header.x_calibration.string = fread(file, 40, 'char');
winspec.header.x_calibration.reserved2 = fread(file, 40, 'char');
winspec.header.x_calibration.calib_valid = fread(file, 1, 'char');
winspec.header.x_calibration.input_unit = fread(file, 1, 'char');
winspec.header.x_calibration.polynom_unit = fread(file, 1, 'char');
winspec.header.x_calibration.polynom_order = fread(file, 1, 'char');
winspec.header.x_calibration.calib_count = fread(file, 1, 'char');
winspec.header.x_calibration.pixel_position = fread(file, 10, 'float64');
winspec.header.x_calibration.calib_value = fread(file, 10, 'float64');
winspec.header.x_calibration.polynom_coeff = fread(file, 6, 'float64');
winspec.header.x_calibration.laser_position = fread(file, 1, 'float64');
winspec.header.x_calibration.reserved3 = fread(file, 1, 'char');
winspec.header.x_calibration.new_calib_flag = fread(file, 1, 'uint8');
winspec.header.x_calibration.calib_label = fread(file, 81, 'char');
winspec.header.x_calibration.expansion = fread(file, 87, 'char');

%y calibration
winspec.header.y_calibration = struct();
winspec.header.y_calibration.offset = fread(file, 1, 'float64');
winspec.header.y_calibration.factor = fread(file, 1, 'float64');
winspec.header.y_calibration.current_unit = fread(file, 1, 'char');
winspec.header.y_calibration.reserved1 = fread(file, 1, 'char');
winspec.header.y_calibration.string = fread(file, 40, 'char');
winspec.header.y_calibration.reserved2 = fread(file, 40, 'char');
winspec.header.y_calibration.calib_valid = fread(file, 1, 'char');
winspec.header.y_calibration.input_unit = fread(file, 1, 'char');
winspec.header.y_calibration.polynom_unit = fread(file, 1, 'char');
winspec.header.y_calibration.polynom_order = fread(file, 1, 'char');
winspec.header.y_calibration.calib_count = fread(file, 1, 'char');
winspec.header.y_calibration.pixel_position = fread(file, 10, 'float64');
winspec.header.y_calibration.calib_value = fread(file, 10, 'float64');
winspec.header.y_calibration.polynom_coeff = fread(file, 6, 'float64');
winspec.header.y_calibration.laser_position = fread(file, 1, 'float64');
winspec.header.y_calibration.reserved3 = fread(file, 1, 'char');
winspec.header.y_calibration.new_calib_flag = fread(file, 1, 'uint8');
winspec.header.y_calibration.calib_label = fread(file, 81, 'char');
winspec.header.y_calibration.expansion = fread(file, 87, 'char');

winspec.header.Istring = fread(file, 40, 'char');
winspec.header.Spare_6 = fread(file, 25, 'char');
winspec.header.SpecType = fread(file, 1, 'uint8');
winspec.header.SpecModel = fread(file, 1, 'uint8');
winspec.header.PulseBurstUsed = fread(file, 1, 'uint8');
winspec.header.PulseBurstCount = fread(file, 1, 'uint32');
winspec.header.ulseBurstPeriod = fread(file, 1, 'float64');
winspec.header.PulseBracketUsed = fread(file, 1, 'uint8');
winspec.header.PulseBracketType = fread(file, 1, 'uint8');
winspec.header.PulseTimeConstFast = fread(file, 1, 'float64');
winspec.header.PulseAmplitudeFast = fread(file, 1, 'float64');
winspec.header.PulseTimeConstSlow = fread(file, 1, 'float64');
winspec.header.PulseAmplitudeSlow = fread(file, 1, 'float64');
winspec.header.AnalogGain = fread(file, 1, 'int16');
winspec.header.AvGainUsed = fread(file, 1, 'int16');
winspec.header.AvGain = fread(file, 1, 'int16');
winspec.header.lastvalue = fread(file, 1, 'int16');

% % Now, read the data
data_types = {'float32' 'int32' 'int16' 'uint16'};
winspec.frames = fread(file, ...
    [winspec.frame_width()*winspec.frame_height()*winspec.n_frames()], ...
    char(data_types(winspec.header.datatype+1)));
% add 1 to the datatype to account for the difference between C (Winspec)
% and Matlab indexing

winspec.frames = reshape(winspec.frames, ...
    [winspec.frame_width() winspec.frame_height() winspec.n_frames()]);

fclose(file);

end

         
      
