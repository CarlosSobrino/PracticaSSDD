#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random

class RobotControllerDetectorI(drobots.ControllerDetector):
	def __init__(self):
		self.enemigos = -1
		self.pos = None

        
	def alert(self, pos, enemigos, current = None):
        self.enemigos = enemigos
        self.pos = pos 

    def robotDestroyed(self, current = None):
        print("Destroyed Robot") 

    def getEnemigo(self, current = None):
        if(self.enemigos > 0):
            return self.pos
        
    