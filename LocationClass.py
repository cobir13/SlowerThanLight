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
        if isinstance(x,list) or isinstance(x,tuple) or isinstance(x,np.ndarray):
            self.space = np.array(x,dtype=float)
        else:
            self.space = np.array([v for v in [x,y,z] if v is not None],dtype=float)
    
    def length_to(self,loc2):
        """spatial separation between self and another Location"""
        return np.sqrt(np.sum((self.space - loc2.space)**2))
    
    def is_visible(self,loc2,c=10):
        """given a viewing space-time location, return the boolean 'light has had
            time to travel from self to the viewer'"""
        return ((loc2.t - self.t)*c >= self.length_to(loc2))
    
    def duplicopy(self):
        return Location(self.t,self.space)
    
    def dim(self):
        return len(self.space)
    
    @property
    def x(self):
        return self.space[0]
    @property
    def y(self):
        return self.space[1]
    @property
    def z(self):
        return self.space[2]