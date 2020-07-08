# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:21:32 2017

@author: Cobi
"""

import numpy as np
import pygame
# from PhysicalsClass import Physical, Orientable


class ViewScreen:
    def __init__(self):
        pygame.display.init()
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.key.set_repeat(5,5)  #5 ms delay, 5 ms interval b/w KEYDOWN events
        self.screen = pygame.display.set_mode((640, 640))  #type(screen) = pygame.Surface
        self.screen.fill((0,0,0))  #black

    def close(self):
        self.screen = None
        pygame.display.quit()
        pygame.quit()

    def draw_visible(self,viewingPhysical,cheater=None):
        """Takes in a Physical object and displays onscreen what its sensor
        would see.  Right now everything it sees displays as blue, and it
        displays itself as green.
        If <cheater> is a Universe instead of None, also display everything in
        that universe like a cheating cheater who cheats. In red. Cheatingly."""
        viewer = viewingPhysical.sensor
        assert(viewer.loc.dim()==2)
        self.screen.fill((0,0,0))
    
        if cheater is not None:
            for thing in cheater.Physicals.values():
                thing.draw_to_screen(self, (255,0,0) ) #red is for cheaters

        viewingPhysical.draw_to_screen(self, (0,255,0) ) #green is you
        
        for event in viewingPhysical.get_visible():
            ghost = event.get_ghostimage() #a ghost copy of the Physical your sensor spotted           
            ghost.draw_to_screen(self, (0,0,255) ) #blue is you seeing them
        pygame.display.flip()        
    
    
    def get_keys(self):
        """return the keyboard keys which have been pressed"""
        happenings = pygame.event.get(pygame.KEYDOWN)
        letters = [ev.unicode for ev in happenings]
        pygame.event.clear()
        if 'Q' in letters:  #hardcoded quit is Capital Q
            self.close()
        return letters
    
    ###-----------------NICE FUNCTIONS TO DRAW THINGS WITH------------------###
    
    def draw_circle(self,color,x,y,radius):
        pygame.draw.circle(self.screen,color,(int(x),int(y)),radius,0)
        
    def draw_triangle(self,color,x,y,theta):
        """Draw a triangle with its vertex at the given location, pointed at
        the given angle."""
        cos = np.cos(theta)
        sin = np.sin(theta)
        verts = [ (x,y), (x-10*cos+3*sin,y-10*sin-3*cos), (x-10*cos-3*sin,y-10*sin+3*cos), (x,y)]
        pygame.draw.polygon(self.screen,color,verts)

    def draw_line(self,color,x1,y1,x2,y2):
        pygame.draw.line(self.screen,color,(x1,y1),(x2,y2))
        
