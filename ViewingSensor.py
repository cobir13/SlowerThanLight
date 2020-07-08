# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 18:04:53 2018

@author: Cobi
"""
#from WorldlineClass import Worldline

class Sensor:
    """An eye floating at a location in space-time in a given Universe.  It
    watches all worldlines not corresponding to its exception-key (representing
    the Physical object the sensor is attached to), and keeps track of the
    latest event in each worldline visible from its location.
    """
    
    def __init__(self, loc, univ, ownkey=None):
        self.univ = univ
        # #dict of worldlines that have already been spotted. key is Worldline id,
        # #value is index of latest visible Event
        # self.watchedlines = {}
        self.loc = loc
        self.ownkey = ownkey #the key of the Physical this sensor belongs to, if any

        
    # def get_visible(self):
    #     """returns a list of the latest visible events in all worldlines"""
    #     eventlist = []
    #     for wline in self.univ.History:
    #         linekey = wline.key
    #         if wline.key == self.ownkey:
    #             continue #no need to observe itself
    #         #get the latest index this sensor has seen, if it's seen this worldline before
    #         prev = self.watchedlines[linekey] if linekey in self.watchedlines else None
    #         #find the freshest visible event, and its index
    #         ev,index = wline.find_latest_visible(self.loc,prev)
    #         if ev is None: #nothing visible
    #            if linekey in self.watchedlines: #remove from list because no longer visible
    #                del self.watchedlines[linekey]
    #         else: #something visible!
    #             self.watchedlines[linekey] = index
    #             eventlist.append(ev)
    #     #while we're here, do some housekeeping
    #     #get rid of any worldlines we're watching which no longer exist
    #     for linekey in [k for k in self.watchedlines.keys() if k not in self.univ.History]:
    #         del self.watchedlines[linekey]
    #     #return all visible events
    #     return eventlist
        
    def get_visible(self):
        """returns a list of the latest visible events in all worldlines"""
        eventlist = []
        for wline in self.univ.History:
            if wline.key == self.ownkey:
                continue #no need to observe itself
            #find the freshest visible event (and its index, for no good reason)
            ev,index = wline.find_latest_visible(self.loc,None)
            if ev is not None: #nothing visible
                eventlist.append(ev)
        return eventlist
        
        
