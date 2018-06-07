#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random

class RobotControllerDefensorI(drobots.ControllerDefensor):
	def __init__(self):
        self.robot = None
        self.robotControllerContainer = None
        self.minas = None
        self.amigos = dict()
        self.location = 0
        self.energy = 100
        self.angle = -1
        self.amplitud = 20
        self.angAmigos = []
        self.speed = 0
        self.coordXEnemigo = -1
        self.coordYEnemigo = -1
        self.contTurn = 0
    
    
    def setRobot(self,robot, jugador, robotControllerContainer, current = None, mines):
        self.robot = robot
        self.jugador = jugador
        self.robotControllerContainer = robotControllerContainer
        self.minas = mines

    def turn(self, current = None):
        self.energy = 100
        self.amigos = self.getAmigos()
        
        self.location = self.robot.location()
        self.energy -= 1
        self.angAmigos = self.getangAmigos()
        self.angle = random.randint(0, 359)
        self.accion()

        self.contTurn += 1

   

    def accion(self, current = None):
        if(self.energy > 10):
            print("Escaneando si hay Robot")
            self.escanear(self.angle, self.amplitud)


        if(self.energy > 60):
            print("Moviendose a otra posicion")
            self.moverRobot(self.location)
            self.energy -= 60


    def moverRobot(self, current = None):
    '''cuadrado invertido '''
        if(self.contTurn == 0):
            self.robot.drive(random.randint(0,360),100)
            self.speed = 100

        elif(self.location.x > 390):
            self.robot.drive(225, 100)
            self.speed = 100

        elif(self.location.x < 100):
            self.robot.drive(45, 100)
            self.speed = 100

        elif(self.location.y > 390):
            self.robot.drive(315, 100)
            self.speed = 100

        elif(self.location.y < 100):
            self.robot.drive(135, 100)
            self.speed = 100

    def escanear(self, angle, amplitud, current = None):
        self.coordXEnemigo = -1
        self.coordYEnemigo = -1
        located = self.robot.scan(angle, amplitud)
        if(located > 0):
            for anguloAmigo in self.angAmigos:
                print("Robot encontrado")
                if(angle > anguloAmigo + 10 and angle < anguloAmigo - 10):
                    print("Robot encontrado:ENEMIGO")
                    coordEnemigoX = int((self.location.x + math.cos(angle) * random.randint(1,4)*100)%1000)
                    self.coordXEnemigo = coordEnemigoX
                    coordEnemigoX = int((self.location.y + math.sin(angle) * random.randint(1,4)*100)%1000)
                    self.coordYEnemigo = coordEnemigoX
                else:
                    print("Robot encontrado:AMIGO")
                    self.angle = -1
                    self.coordXEnemigo = -1
                    self.coordYEnemigo = -1


    def getangAmigos(self, current = None):
        angAmigos=[]
        print("Buscar angulos donde estan los robot amigos")
        for keys in self.amigos.keys():
            if("ataque") in keys:
                atac = drobots.ControllerAtacantePrx.checkedCast(self.amigos[keys])
                coord = atac.getPosicionAmiga()
                angle = self.calcularangle(coord)
                angAmigos.append(angle)

            elif("defensa") in keys:
                defen = drobots.ControllerDefensorPrx.checkedCast(self.amigos[keys])
                coord = defen.getPosicionAmiga()
                angle = self.calcularangle(coord)
                angAmigos.append(angle)


        return angAmigos
                    
            
    def getCoordEnemigoX(self, current = None):
        coordenadaX = self.coordXEnemigo
        return coordenadaX

    def getCoordEnemigoY(self, current = None):
        coordenadaY = self.coordYEnemigo
        return coordenadaY
    

    def calcularangle(self, coord, current = None):
        pX = math.fabs(coord.x - self.location.x)
        pY = math.fabs(coord.y - self.location.y)
        angle=int(math.degrees(math.atan2(pY,pX)))
        if(angle < 0):
            angle = angle + 360
        elif(angle >= 360):
            angle = 0
        return angle


    def getAmigos(self, current = None):
        amigos = dict()
        lis = self.robotControllerContainer.listController()
        for i in range(0, len(lis)):
            keys = lis.keys()[i]
            values = lis.values()[i]
            if(self.jugador) in keys:
                amigos[keys] = values

        return amigos


    def robotDestroyed(self, current = None):
        print("Destroyed Robot")

    def getPosicionAmiga(self, current = None):
        location = self.robot.location()
        return location
