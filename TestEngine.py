# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:52:40 2017

@author: Cobi
"""
from UniverseClass import Universe        
from Graphics import ViewScreen
from PhysicalsClass import Orientable

import time


def ship_controls(myship,keyspressed):
    if 'a' in keyspressed:
        myship.boost((-.01,0))
    if 'd' in keyspressed:
        myship.boost((0.01,0))
    if 'w' in keyspressed:
        myship.boost((0,-.01))
    if 's' in keyspressed:
        myship.boost((0,0.01))
    if 'q' in keyspressed:
        myship.spin( 0.001)
    if 'e' in keyspressed:
        myship.spin(-0.001)   
    if "c" in keyspressed:
        myship.boost((-1*myship.v[0],-1*myship.v[1]))
        myship.spin(-1*myship.dtheta)

try:
    #####----TWO DIMENTIONAL OPERATION----####
    viewscreen = ViewScreen()
    keeplooping = True
    univ = Universe(lightspeed=1)
    myship    = Orientable(0,(20,20),(0,0),0,0,univ)
    othership = Orientable(0,(100,100),(0,0),1.57,0.003,univ)
    
    while keeplooping:
        startclock = time.perf_counter()
        univ.increment(dt=1)
        #draw the visible Physical objects
        viewscreen.draw_visible(myship,cheater=univ)
        letters = viewscreen.get_keys()
        ship_controls(myship,letters)
        if "Q" in letters:
            keeplooping = False
            
        if "r" in letters:
            print( [len(p.worldline.eventlist) for p in univ.Physicals.values()] )
            
        while time.perf_counter() - startclock < 0.01: #10 ms, or 100FPS
            time.sleep(0.001) #wait 1 ms
            
        #make the other ship dance around a bit
        shipclock = othership.loc.t%1000
        if 0<shipclock<30:
            othership.boost((.01,0))
        if 600<shipclock<630:
            othership.boost((-.01,0))
        if 500<shipclock<530:
            othership.boost((-.02,0))
        if 800<shipclock<830:
            othership.boost((.02,0))
        if 50<shipclock<60:
            othership.boost((0,.1))
        if 150<shipclock<160:
            othership.boost((0,-.1))
        if 300<shipclock<350:
            othership.boost((0,-.01))
        if 500<shipclock<550:
            othership.boost((0,.01))
        

        
    viewscreen.close()

except Exception as e:
    viewscreen.close()
    raise e
    

