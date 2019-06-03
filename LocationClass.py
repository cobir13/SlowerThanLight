# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:53:57 2019

@author: Cobi
"""
import numpy as np

class Location:
    """a location in spacetime, with one time dimension and between 1 and 3
        space dimensions.
        Arguments are:
            x as spatial position as an array of length between 1 and 3
        or:
            x,y,z are spatial coords (for dim<3, leave z and/or y as Nones)
        t is always the time dimension.
        """
    def __init__(self,t,x,y=None,z=None):
        self.t=t
        self.x=None
        self.y=None
        self.z=None
        try:
            d = len(x)  # if x is a single real number this raises TypeError
            self.x = x[0]
            if d>=2:
                self.y = x[1]
                self.z = None
            if d>=3:
                self.z = x[2]

        except TypeError:
            self.x=x
            self.y=y
            self.z=z

    def space(self):
        return np.array([v for v in [self.x,self.y,self.z] if v is not None])
    
    def dim(self):
        """number of spatial dimentions"""
        return len(self.space())
    
    def length_to(self,loc2):
        """spatial separation between self and another Location"""
        assert(self.dim() == loc2.dim())
        return np.sqrt(np.sum((self.space() - loc2.space())**2))
    
    def duplicopy(self):
        return Location(self.t,self.x,self.y,self.z)