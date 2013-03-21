#!/usr/bin/python

from sympy import *

# Class used to pass various data around so that it is available to all Pis when computing (x,y)
class PiData:

    def __init__(self, sig_str_to_ap):
        
        # Data from Pi defining y-axis
        self.y_PiDistToMe=None
        self.y_PiDistToAp=None
        self.y_PiSigStrenToAp=None
        
        # Data from Pi defining x-axis
        self.x_PiDistToMe=None
        self.x_PiDistToAp=None
        self.x_PiSigStrenToAp=None
        
        # Hash keyed by mac to return the coordinates of all Pis
        self.piPositions = {}
        
        self.my_SigStrenToAp = sig_str_to_ap
        self.my_DistToAp=None
        self.my_XY=None

    def computeXY(self):
        # Using trilateration QUESTION: what happens if no solution is found due to error?
        x_PiPt = 0,1
        radius1 = 1
        
        y_PiPt = 1,0
        radius2 = 1
        
        # compute my radius to origin using signal strengths
        radius3 = 2
        
        equations = [
            Eq(S('(x-(%d))**2+(y-(%d))**2' % (x_PiPt[0], x_PiPt[1]) ) , S('%d' % radius1)),
            Eq(S('(x-(%d))**2+(y-(%d))**2' % (y_PiPt[0], y_PiPt[1]) ), S('%d' % radius2)),
            Eq(S('x**2+y**2'), S('%d' % radius3))
        ]
        
        return solve(equations)
        
        # TODO Add methods for acessing dBm to metres conversion table plus interpolation logic
        # Replace hardcoded positions and radii with computed ones!
        
