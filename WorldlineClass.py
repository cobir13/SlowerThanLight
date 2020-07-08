# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:57:26 2018

@author: Cobi
"""
import numpy as np
from EventClass import Event
from LocationClass import Location

        
# =============================================================================
# class Worldline:
#     """A list of Events in a single Universe describing a path through
#     space-time. The Events are presumably all caused by the same Physical so
#     that the Worldline describes how the Physical is acting through time, but
#     the Worldline itself does not care about this."""
#             
#     def __init__(self,univ):
#         self.eventlist = []  #ordered list of Events
#         self.timestamps = {} #key=timestamp, value=index of corresponding event
#         self.key = univ.add_worldline(self)
#         self.univ = univ   ###-------------------------------------------------might just want lightspeed?
#         self.timer = 0  #time since latest event added. See self.prune and univ.increment
#         
#     def add_event(self,loc,phystype,descrip):      
#         ev = Event(loc,phystype,descrip)
#         if len(self.eventlist)>0:
#             if ev.t > self.eventlist[-1].t:  #adding in chronological order
#                 self.timestamps[ev.t] = len(self.eventlist)  #index of the new Event being added
#                 self.eventlist.append(ev)
#             elif ev.t == self.eventlist[-1].t:  #same time, so replace
#                 self.eventlist[-1] = ev
#             else:
#                 raise AssertionError #trying to add backwards in time!
#         else:
#             self.timestamps[ev.t] = len(self.eventlist)  #index of the new Event being added
#             self.eventlist.append(ev)
#         self.timer = 0
#     
#     def prune(self):
#         """Gets rid of events so far in the past that they can't be seen again"""
#         crossingtime = 2*self.univ.radius / self.univ.lightspeed
#         if self.timer > crossingtime:
#             self.univ.del_worldline(self.key)
#         elif len(self.eventlist)>0:
#             index=0
#             while self.eventlist[-1].t - self.eventlist[index].t > crossingtime:
#                 del self.timestamps[self.eventlist[index].t]
#                 del self.eventlist[index]
#                 index += 1
#         for k in self.timestamps.keys():
#             self.timestamps[k] = self.timestamps[k] - index
# 
#     """Return the latest Event that a viewer at loc would see of the Events on
#     the Worldline. If the viewer could not see any Event, return None. prev is
#     the last Event that the viewer remembers seeing, of events on this
#     Worldline (not necessarily the immediate previous Event on the line), or
#     None if none is remembered.
#     THIS FUNCTION IS AT THE HEART OF THE WHOLE PROGRAM WORKING PROPERLY!!!
#     """
#     def find_latest_visible(self,loc,prev=None):
#         if len(self.eventlist) == 0:
#             return None #no events to see yet
#         #no hint where to start, so iterate through eventlist
#         if prev is None:
#             prev = self.eventlist[0] #oldest Event in Worldline
#         if not prev.is_visible(loc, self.univ.lightspeed):
#             return None #if can't see oldest, can't see any
#         index = self.timestamps[prev.t] #index to start searching Worldline
#         while index+1 < len(self.eventlist):
#             if not self.eventlist[index+1].is_visible(loc,self.univ.lightspeed):
#                 break #can see Event at index but not event at index+1
#             index += 1
#         else: #can see even latest in Worldline:
#             return None #entire Worldline is now in the past
#         return self.interpolate(index,loc)        
#     
#     def interpolate(self, index, viewloc):
#         """Find where the lightcone of viewloc intersects the worldline joining
#         the events prev and post.  Return an interpolated event at that
#         intersection point, which is what viewloc would see as it watches the
#         worldline.
#         Using convention prev=1, post=2, veiwloc=v:
#             parametrized worldline is x=(t-t1)*v_i+x1 for v_i=(x2-x1)/(t2-t1)
#             find t where distance b/w x, viewloc is delta-t*c
#         """
#         prev = self.eventlist[index]
#         post = self.eventlist[index+1]
#         v_i = (post.space() - prev.space())/(post.t - prev.t)
#         #quadratic formula components
#         a = np.sum(v_i**2)-self.univ.lightspeed**2
#         b = (2 * np.sum(v_i*(prev.space() - prev.t*v_i - viewloc.space())) +
#                 2 * viewloc.t * self.univ.lightspeed**2)
#         c = (np.sum((prev.space() - prev.t*v_i - viewloc.space())**2) -
#                   (viewloc.t * self.univ.lightspeed)**2)
#         pos = (-1*b + np.sqrt(b**2 - 4*a*c))/(2*a)
#         neg = (-1*b - np.sqrt(b**2 - 4*a*c))/(2*a)
#         #use correct component for time, then use time to find spatial location        
#         inter_t = (pos if prev.t<=pos<=post.t else neg)
#         inter_x = list((inter_t-prev.t)*v_i+prev.space())
#         while len(inter_x) < 3:
#             inter_x.append(None) #fixing dimentionality        
#         self.timestamps[inter_t] = index  #viewer might dictionary-lookup inter_t later
#         
#         return Event(Location(inter_t,inter_x[0],inter_x[1],inter_x[2]),prev.phystype,prev.descrip)  #should really interpolate description too....
#         
# =============================================================================
        
class Worldline:
    """A list of Events in a single Universe describing a path through
    space-time. The Events are presumably all caused by the same Physical so
    that the Worldline describes how the Physical is acting through time, but
    the Worldline itself does not care about this.
    It is automatically added to the Universe's History so other things can
    see it and interact with it."""
            
    def __init__(self,univ,startingEvent):
        self.eventlist = [startingEvent,startingEvent]  #list of Events. Acts as ring buffer
        self.future = 0 #index of the next place to add an event in the list. (Value of 2%2=0 --Cobi)
        self.oldest = 0 #index of oldest event in the list
        self.len = 2    #len(self.eventlist)
        
        self.key = univ.add_worldline(self)
        self.univ = univ
        
    def add_event(self,ev):      
        """add an event to the worldline. must occur at the same time or after
        the freshest event already present."""
        assert(ev.t >= self.eventlist[self.future-1].t) #should be newest thing!
        #check if we need to make the eventlist longer
        if self.future == self.oldest:
            self.eventlist.insert(self.future,ev)
            self.oldest += 1 #I've bumped the past up by one notch via inserting just before it
            self.len += 1
        else:
            self.eventlist[self.future] = ev
        #increment the future counter
        self.future = (self.future+1) % self.len
    
    def update_latest(self,ev):
        """Replace the previously-freshest event with the given event"""
        self.eventlist[self.future-1] = ev
    
    
    def prune(self):
        """Gets rid of events so far in the past that they can't be seen again"""
        crossingtime = 2*self.univ.radius / self.univ.lightspeed
        #if freshest event was added to worldline so long ago it's now out of
        #sight in the past, delete the whole worldline
        if self.univ.clock - self.eventlist[self.future-1].t  > crossingtime:
            self.univ.del_worldline(self.key)
            print("worldline with key", self.key,"lost in the past")
            return
        #if the event at self.oldest is stale, we will interpolate it to bring
        #it up to snuff, since it might be a valuable endcap for interpolation.
        #Unless the NEXT one is ALSO stale, in which case we should update THAT...
        while self.univ.clock - crossingtime > self.eventlist[self.oldest].t :
            plusone = (self.oldest+1)%self.len
            if self.univ.clock - crossingtime > self.eventlist[plusone].t:
                #next Event is ALSO stale, so move on to repairing THAT one
                self.oldest = plusone
            else:
                #next Event is fine, so interpolate this one to repair it (and don't move self.oldest)
                t = self.univ.clock - crossingtime
                e0 = self.eventlist[self.oldest]
                e1 = self.eventlist[plusone]
                percentage = (t-e0.t)/(e1.t-e0.t)
                newspace = percentage*(e1.space-e0.space) + e0.space
                newdescrip = e0.phystype.interpolate(e0.descrip,e1.descrip,percentage)
                self.eventlist[self.oldest] = Event(e0.phystype,newdescrip,t,newspace)
        

    """Return the latest Event that a viewer at loc would see of the Events on
    the Worldline, as well as the index of that event. If the viewer could not
    see any Event, return None,None.
    prev is the index of the last event that the viewer remembers seeing on
    this Worldline (using the indexing of the list underlying the Ring Bugger),
    or None if no memory of where it was last.
    THIS FUNCTION IS AT THE HEART OF THE WHOLE PROGRAM WORKING PROPERLY!!!
    """
    def find_latest_visible(self,loc,prev=None):
        # if prev is None or prev>self.len:
        #     index = self.oldest
        # elif self.newest < prev+self.len < self.oldest+self.len :
        #     #if prev is after the newest but before oldest in ring buffer, then
        #     #it's no good and we should start searching from oldest instead
        #     index = self.oldest
        # elif not self.eventlist[index].is_visible(loc,self.univ.lightspeed):
        #     #if can't see the Event in the index where you saw an event last time, you got lapped!
        #     index = self.oldest
        # else:
        #     index = prev
        index = self.oldest
        #if can't see oldest, can't see any
        if not self.eventlist[index].is_visible(loc,self.univ.lightspeed):
            return None,None
        #if program reached here, we know the viewer CAN see event at index. now find NEWEST visible
        plusone = (index+1)%self.len
        while plusone != self.future:
            if not self.eventlist[plusone].is_visible(loc,self.univ.lightspeed):
                break #can see Event at index but not event at index+1
            index = plusone
            plusone = (index+1)%self.len
        else: #can see even latest in Worldline:
            return None,None #entire Worldline is now in the past
        return self.interpolate(index,loc) , index
    
    
    def interpolate(self, index, viewloc):
        """Find where the lightcone of viewloc intersects the worldline joining
        the events prev and post.  Return an interpolated event at that
        intersection point, which is what viewloc would see as it watches the
        worldline.
        Using convention prev=1, post=2, veiwloc=v:
            parametrized worldline is x=(t-t1)*v_i+x1 for v_i=(x2-x1)/(t2-t1)
            find t where distance b/w x, viewloc is delta-t*c
        """
        prev = self.eventlist[index]
        post = self.eventlist[(index+1)%self.len]
        v_i = (post.space - prev.space)/(post.t - prev.t)
        #quadratic formula components
        a = np.sum(v_i**2)-self.univ.lightspeed**2
        b = (2 * np.sum(v_i*(prev.space - prev.t*v_i - viewloc.space)) +
                2 * viewloc.t * self.univ.lightspeed**2)
        c = (np.sum((prev.space - prev.t*v_i - viewloc.space)**2) -
                 (viewloc.t * self.univ.lightspeed)**2)
        pos = (-1*b + np.sqrt(b**2 - 4*a*c))/(2*a)
        neg = (-1*b - np.sqrt(b**2 - 4*a*c))/(2*a)
        #use correct component for time, then use time to find spatial location        
        inter_t = (pos if prev.t<=pos<=post.t else neg)
        inter_x = (inter_t-prev.t)*v_i+prev.space
        #interpolate the description of the event too, according to its own class methods
        percentage = (inter_t-prev.t)/(post.t-prev.t)
        inter_descrip = prev.phystype.interpolate(prev.descrip,post.descrip,percentage)
        return Event(prev.phystype,inter_descrip,inter_t,inter_x)
    