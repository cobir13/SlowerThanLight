# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:56:19 2018

@author: Cobi
"""
import numpy as np

from ViewingSensor import Sensor
from WorldlineClass import Worldline
from LocationClass import Location
from EventClass import Event


class Physical:
    """Physical objects that live in a Universe. They exist at a spacetime
    location with an orientation in space and velocity through space. Each
    Physical leaves behind a Worldline of events. Finally, each Physical has
    a Sensor which is the way it perceives other Physicals.
    
    Note: this class is meant to be extended to specific physical objects (for
    example, Ships or Asteroids). BE SURE TO OVERWRITE THE compress() AND
    decompress() METHODS!
    """
    
    def __init__(self,t,x,v,univ,isghost=False):
        """If isghost, the Physical is built as normal but without informing
        the Universe or building a Worldline for it."""
        self.univ = univ
        self.loc = Location(t,x)
        self.v = np.array(v,dtype=float)
        #Finished with descriptive fields. Now add to Universe
        self.linekey = None
        self.key = None
        if not isghost:
            firstevent = Event(type(self),self.compress(),self.loc.t,self.loc.space)
            worldline = Worldline(univ,firstevent) #build new Worldline (it adds itself to to univ.History)
            self.linekey = worldline.key
            self.sensor = Sensor(self.loc,univ,ownkey=self.linekey)
            self.key = univ.add_physical(self)

    def boost(self,dv):
        """Accelerate. Also create a new Event in the worldline, since you've maneuvered"""
        self.v += np.array(dv,dtype=float)
        #avoid exceeding the speed of light
        if np.sum(self.v**2) > self.univ.lightspeed**2:  #can't exceed lightspeed
            self.v = (self.v / np.sqrt(np.sum(self.v**2)))*(self.univ.lightspeed*0.999)
        #drifting parameters (velocity) has changed, so add a Worldline event
        self.worldline.add_event(self.GetStatusAsEvent())
    
    def drift(self, dt=1):
        #update location
        self.loc.t += dt
        self.loc.space += self.v*dt
        self.sensor.loc = self.loc #update sensor so it knows where its Physical is
        #just drifting, so interpolation is still valid. So don't need to add
        #NEW event, just update the latest so worldline has latest status info
        self.worldline.update_latest(self.GetStatusAsEvent())
        
    def destroy(self):
        self.worldline.add_event(self.GetStatusAsEvent())
        self.univ.del_physical(self.key)
    
    def GetStatusAsEvent(self):
        return Event(type(self),self.compress(),self.loc.t,self.loc.space)
    
    @property
    def worldline(self):
        return self.univ.get_worldline(self.linekey)
    
    # def find_collided(self,impactradius):
    #     """return a list of all Events that this Physical can see which are
    #     within impactradius of itself"""
    #     impactlist = []
    #     for ev in self.see_visible():
    #         if ev.length_to(self.loc) <= impactradius:
    #             impactlist.append(ev)
    #     return impactlist
                
    def get_visible(self):
        """return a list of all Events that this Physical can see"""
        return self.sensor.get_visible()
        
    def draw_to_screen(self,viewscreen,color):
        """draws self on a pygame viewscreen. Should be overridden for
        subclasses, to have their own individual displays"""
        viewscreen.draw_circle(color,self.loc.x,self.loc.y,radius=3)

    def compress(self):
        """give enough info to reconstruct the Physical as it was at this
        current point in spacetime, in as short a string as possible. No need
        to save spatial or temporal coordinates, though."""
        descrip = "V"
        descrip+= ",".join([("%0.2f" %component) for component in self.v])
        descrip += "END"
        return descrip
    
    def decompress(loc,cipherstring):
        """take in a Location and a compressed string following the compress
        method convention and returns a ghost Physical that matches the
        description.
        Note that this is a class method, NOT a instance method."""
        indxV = cipherstring.index("V")
        endex = cipherstring.index("END")
        v  = [float(x) for x in cipherstring[indxV+1:endex].split(",")]
        return Physical(loc.t,loc.space,v,None,isghost=True)
    
    def interpolate(cipher1,cipher2,percentage):
        return cipher1


###-------------------------------------------------------------------------###

class Orientable(Physical):
    """A line with a distinct "front" and "back", which stuff can bounce off of"""
    
    def __init__(self,t,x,v,theta,dtheta,univ,isghost=False):
        """If isghost, the Physical is built as normal but without informing
        the Universe or building a Worldline for it."""
        self.theta = theta #angle, in radians, clockwise from 3:00 (x-axis)
        self.dtheta = dtheta
        super().__init__(t,x,v,univ,isghost=isghost)

    def spin(self,ddtheta):
        """The equivalent to boost for angular velocity. Change the rate of
        change of theta by adding dtheta to the old rate."""
        self.dtheta = self.dtheta + ddtheta
        self.worldline.add_event(self.GetStatusAsEvent())
        
    ###update the drift, compress, and decompress functions to account for theta, dtheta
    def drift(self, dt=1):
        self.theta += self.dtheta
        super().drift(dt=dt)
    
    def draw_to_screen(self,viewscreen,color):
        """draws self on a pygame viewscreen. Should be overridden for
        subclasses, to have their own individual displays"""
        viewscreen.draw_triangle(color,self.loc.x,self.loc.y,self.theta)
    
    def compress(self):
        """give enough info to reconstruct the Orientable as it was at this
        current point in spacetime, in as short a string as possible. No need
        to save spatial or temporal coordinates, though."""
        descrip = "V"
        descrip+= ",".join([("%0.2f" %component) for component in self.v])
        descrip+="T%0.2f" % self.theta
        descrip+="O%0.2f" % self.dtheta
        descrip += "END"
        return descrip
    
    def decompress(loc,cipherstring):
        """take in a compressed string following the compress method convention
        and returns a ghost Physical that matches the description.
        Note that this is a class method, NOT a instance method."""
        indxV = cipherstring.index("V")
        indxT = cipherstring.index("T")
        indxO = cipherstring.index("O")
        endex = cipherstring.index("END")
        v  = [float(x) for x in cipherstring[indxV+1:indxT].split(",")]
        th = float( cipherstring[indxT+1:indxO] )
        om = float( cipherstring[indxO+1:endex] )
        return Orientable(loc.t,loc.space,v,th,om,None,isghost=True)
    
    def interpolate(cipher1,cipher2,percentage):
        indxT1 = cipher1.index("T")
        indxO1 = cipher1.index("O")
        th1 = float( cipher1[indxT1+1:indxO1] )
        indxT2 = cipher2.index("T")
        indxO2 = cipher2.index("O")
        th2 = float( cipher2[indxT2+1:indxO2] )
        th_new = percentage*(th2-th1)+th1
        # print(th1,th2,percentage,th_new)
        newcipher = cipher1[:indxT1]+("T%0.2f" %th_new)+cipher1[indxO1:]
        return newcipher
    
    
 