import numpy as np

class hamiltonian():

    def __init__(self):
        self.tau = 1.5 #Beats per SECOND
        self.period = 48. / self.tau
        self.omega = 5
        #Define the Ending thresholds in units of seconds
        self.I = np.array([i/self.tau for i in [15, 23, 31, 35, 37, 39, 43, 45, 47]])
        self.C7 = [10,0,5,4,8,2,0,9,0,1,8,0]
        self.F7 = [9,0,1,8,0,10,0,5,4,8,2,0]
        self.G7 = [2,0,9,0,1,8,0,10,0,5,4,8]
        self.A7 = [4,8,2,0,9,0,1,8,0,10,0,5]
        self.D7 = [0,8,10,0,2,0,8,3,0,9,0,1]
        self.d7 = [8,0,10,0,2,8,0,3,0,9,1,2]
        self.HC = self.omega * 0.5 * (np.outer(self.C7,self.G7) + np.outer(self.G7,self.C7))
        self.HF = self.omega * 0.5 * (np.outer(self.F7,self.C7) + np.outer(self.C7,self.F7))
        self.HG = self.omega * 0.5 * (np.outer(self.G7,self.D7) + np.outer(self.D7,self.G7))
        self.Hd = self.omega * 0.5 * (np.outer(self.d7,self.A7) + np.outer(self.A7,self.d7))

    def CJB(self,t):
        """
        Params:
        -------
            t: time IN UNITS OF SECONDS
        """
        red_t = t % self.period
        chord = self.I[self.I > red_t][0]
        I_temp = list(self.I)
        loc = I_temp.index(chord) 
        if loc == 0 or loc == 2 or loc == 5:
            return self.HC
        elif loc == 1 or loc == 4:
            return self.HF
        elif loc == 3 or loc == 7:
            return self.HG
        elif loc == 6:
            return self.Hd
        if t > self.period:
            t = 0 
        
if __name__ == "__main__":
    pass
