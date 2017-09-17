import Qsys
import numpy as np
#import csv_to_tracklist

class QsysInterface():

    def __init__(self, tracklist, tf):
        """
        Takes tracklist as a parameter in constructor
        """
        self.measurements = tracklist
        self.tf = tf

    def setFirstMeasurement(self):
        for i in range(len(self.measurements)):
            if (len(self.measurements[i]) == 0):
                pass
            else:
                self.nextMeasurement = self.measurements[i]

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
