# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:54:39 2019

@author: Cobi
"""
from LocationClass import Location

class Event(Location):
    """A location in space-time and the type and parameters of the Physical object
    which was there at that time.  The parameters are not themselves a Physical,
    just some sort of compressed description that can be later expanded and
    used to see what had happened at this Event.
    """
    
    def __init__(self,phystype,descrip,t,x,y=None,z=None):
        super().__init__(t,x,y=y,z=z)
        self.descrip = descrip
        self.phystype = phystype
    
    def get_ghostimage(self):
        """Return an instance of the correct subtype of Physical which matches
        the description of this event. That Physical is a 'ghost': not
        registered with the Universe and has no Worldline"""
        return self.phystype.decompress(self,self.descrip)
    