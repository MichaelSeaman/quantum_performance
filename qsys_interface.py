import Qsys
import numpy as np
#import csv_to_tracklist

class QsysInterface():
   
    def __init__(self, tracklist): 
        """
        Takes tracklist as a parameter in constructor
        """
        self.measurements = [[], [], [[3, 0, 0.186951, 0, 3266, 3269], [3, 4, 0.186951, 0, 3267, 3268], [3, 0, 0.373902, 0, 3270, 3273], [3, 4, 0.373902, 0, 3271, 3272], [3, 0, 0.5596605, 0, 3274, 3277], [3, 4, 0.5596605, 0, 3275, 3276]], [[2, 0, 0.0, 0, 11774, 11775], [2, 7, 0.186951, 0, 11776, 11779], [2, 0, 0.186951, 0, 11777, 11778], [2, 7, 0.373902, 0, 11780, 11783], [2, 0, 0.373902, 0, 11781, 11782]], [], [], [], []]  #[i,j] => i -> pitch (0 - 11), j -> time (in seconds)

    def setFirstMeasurement(self):
        for i in range(len(self.measurements)):
            if (len(self.measurements[i]) == 0):
                pass
            else:
                self.nextMeasurement = self.measurements[i]

    def setFinalTime(self):
        for i in range(len(self.measurements)):
            if (len(self.measurements[-i]) == 0):
                pass
            else:
                self.tf = self.measurements[4][-i][2] + 3

    def setQsys(self):
        """
        Setup quantum system, needs to be called for each track
        """
        self.sys = Qsys.Qsys(12, [1,0,0,0,0,0,0,0,0,0,0,0], 0.01, 6, [10,0,3,0,9,2,0,8,0,2,1,6], None, None, 0, 7, argHamiltonian=None)
    
    def setCurrentTrack(self):
        self.current_track = None

    def doMeasurement(self):
        """
        Called whenever measurement condition is reached (ie: sys.time > next_measurement.time) 
        """
        print("Measuring")
        self.next_measurement[3] = self.sys.measure(self.next_measurement[1])[1]
        self.i += 1
        if self.i < len(self.current_track):
            self.next_measurement = self.current_track[i]
            print("Moving to next measurement")
        else:
            self.next_measurement = [0,0,tf + 5,0]

    def run(self):
        """
        Measurements Format:
        [octave, pitch, time, output, etc...]
        """
        j = 0
        self.setFirstMeasurement()
        self.setFinalTime()
        for track in self.measurements: #Separate each track into a single list of measurements
            print("Working on Track " + str(j))
            self.next_mesaurement = self.current_track[0]
            self.setQsys()
            self.i = 0
            while self.sys.time < self.tf: #Loop over all time steps
                print(self.sys.time)
                if (self.sys.time > self.next_measurement[2]): #check if system time is close to measurement time 
                    self.doMeasurement()
                self.sys.run()
            j += 1
            if j < len(self.measurements):
                self.next_measurement = self.measurements[j][0]
        print(self.measurements)
            
if __name__ == "__main__":
    pass
