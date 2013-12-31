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

classdef Winspec
    properties
        header
        frames
    end
    
    methods
        function X = x(obj)
            % Return the x axis from the calibration
            poly = fliplr( ...
                   obj.header.x_calibration.polynom_coeff( ...
                        1:(obj.header.x_calibration.polynom_order+1))');
            pixels = 1:obj.frame_width();

            X = polyval(poly, pixels);
        end
        
        function T = t(obj)
            % Return the t axis from a video            
            T = obj.header.exp_sec*(0:(obj.n_frames()-1));
        end
        
        function n = n_frames(obj)
            n = obj.header.NumFrames;
        end
        
        function width = frame_width(obj)
            width = obj.header.xdim;
        end
        
        function height = frame_height(obj)
            height = obj.header.ydim;
        end
    end
end
     
