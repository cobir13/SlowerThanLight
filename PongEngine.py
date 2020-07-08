# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:52:40 2017

@author: Cobi
"""
from UniverseClass import Universe        
from Graphics import ViewScreen
from PhysicalsClass import Physical,Orientable

import time
import numpy as np



class Ball(Physical):
    def __init__(self,t,x,v,univ,isghost=False):
        super().__init__(t,x,v,univ,isghost=isghost)
        
        
class Mirror(Orientable):
    
    def __init__(self,t,x,v,theta,dtheta,univ,isghost=False):
        self.theta = theta #angle, in radians, counterclockwise from 3:00 (x-axis)
        self.dtheta = dtheta
        super().__init__(t,x,v,theta,dtheta,univ,isghost=isghost)
    
    
    def draw_to_screen(self,viewscreen,color):
        """draws self on a pygame viewscreen. Should be overridden for
        subclasses, to have their own individual displays"""
        x = self.loc.x
        y = self.loc.y
        cos = np.cos(self.theta)
        sin = np.sin(self.theta)
        viewscreen.draw_line(color,x-10*sin,y+10*cos,x+10*sin,y-10*cos)
        viewscreen.draw_triangle(color,x,y,self.theta)

    def decompress(loc,cipherstring):
        """take in a compressed string following the compress method convention
        and returns a ghost Mirror that matches the description.
        Note that this is a class method, NOT a instance method."""
        orien = Orientable.decompress(loc,cipherstring)
        return Mirror(orien.loc.t,orien.loc.space,orien.v,orien.theta,orien.dtheta,None,isghost=True)



def ship_controls(myship,keyspressed):
    if 'a' in keyspressed:
        myship.boost((-.05,0))
    if 'd' in keyspressed:
        myship.boost(( .05,0))
    if 's' in keyspressed:
        myship.boost((0,-.05))
    if 'w' in keyspressed:
        myship.boost((0, .05))
    if 'q' in keyspressed:
        myship.spin(-0.001)
    if 'e' in keyspressed:
        myship.spin(+0.001)   
    #emergency brakes, for testing purposes. Just zero everything out.
    if "c" in keyspressed:
        myship.boost((-1*myship.v[0],-1*myship.v[1]))
        myship.spin(-1*myship.dtheta)


#main game loop. the try-except is to exit gracefully in case something goes wrong

try:
    viewscreen = ViewScreen()
    keeplooping = True
    #set up the universe
    w,h = viewscreen.screen.get_size()
    univ = Universe(lightspeed=5,radius=np.hypot(w,h))
    
    
    
    paddle = Mirror(0,(20,20),(0,0),0,0,univ)
    
    for k in range(10):
        pos = np.random.randint(100,300,2)
        vel = 6*(np.random.rand(2)-0.5)   #max speed 2*sqrt(3) = 2.8
        Ball(univ.clock,pos,vel,univ)
    
    for k in range(5):
        pos = np.random.randint(100,300,2)
        vel = 4*(np.random.rand(2)-0.5)   #max speed 3*sqrt(2) = 4.24
        omega = np.random.rand()*0.03
        Mirror(univ.clock,pos,vel,1,omega,univ)
    
    
    

    while keeplooping:
        startclock = time.perf_counter()
        univ.increment(dt=1)
        
        #draw the visible Physical objects
        viewscreen.draw_visible(paddle,cheater=None) #univ)
        
        #make everything bounce off of the walls (in reality, not just what the paddle can see)
        for thing in univ.Physicals.values():
            x = thing.loc.x
            y = thing.loc.y
            if (x<0 and thing.v[0]<0) or (x>viewscreen.screen.get_size()[0] and thing.v[0]>0): #horizontal bounce
                thing.boost( (-2*thing.v[0],0) )
            if (y<0 and thing.v[1]<0) or (y>viewscreen.screen.get_size()[1] and thing.v[1]>0): #vertical bounce
                thing.boost( (0, -2*thing.v[1]) )

        
        # #make the balls reflect off the paddle
        # for b in [ball,ball2]:
        #     if np.sqrt(np.sum((paddle.loc.space-b.loc.space)**2))<20:
        #         dot = np.sum(b.v*paddle.v)
        #         ball.boost( (-2*dot*np.cos(paddle.theta),-2*dot*np.sin(paddle.theta)) )
            
        
        #handle keyboard inputs as control signals
        letters = viewscreen.get_keys()
        ship_controls(paddle,letters)
        if "Q" in letters:
            keeplooping = False #quit if we get capital Q (also happens inside <viewscreen>, I think --Cobi)
        if "r" in letters:
            print( [len(p.worldline.eventlist) for p in univ.Physicals.values()] )
        if "b" in letters:
            print( [(p.worldline.future-p.worldline.oldest)%p.worldline.len for p in univ.Physicals.values()] )
            
        while time.perf_counter() - startclock < 0.01: #10 ms, or 100FPS
            time.sleep(0.001) #wait 1 ms
        
    viewscreen.close()

except Exception as e:
    viewscreen.close()
    raise e
    


# keeplooping = True
# #set up the universe
# univ = Universe(lightspeed=10,radius=900)

# ball     = Ball(0,(100,100),(0.2,0.25),univ)
# ball2    = Ball(0,(200,300),(0.1,0.15),univ)
# paddle = Mirror(0,(20,20),(0,0),0,0,univ)



# # univ.increment(dt=1)


        