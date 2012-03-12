classdef Winspec
    properties
        header
        frames
    end
    
    methods
        function X = x(obj)
            % Return the x axis from the calibration
            X = polyval(fliplr(obj.header.x_calibration.polynom_coeff'), ...
                1:obj.frame_width());
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
     
