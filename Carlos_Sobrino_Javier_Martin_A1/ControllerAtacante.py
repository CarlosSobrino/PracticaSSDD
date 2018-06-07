#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random

class RobotControllerAtacanteI(drobots.ControllerAtacante):
	def __init__(self):
		self.robot = None
		self.robotControllerContainer = None
		self.minas= None
		self.amigos = dict()
		self.location = 0
		self.energy = 100
		self.angle = -1
		self.angAmigos = []
		self.angEnemigos = []
		self.speed = 0
		self.contTurn = 0

	
	def setRobot(self,robot, jugador, robotControllerContainer, current = None,mines):
		self.robot = robot
		self.jugador = jugador
		self.robotControllerContainer = robotControllerContainer
		self.minas= mines
		
	def turn(self, current = None): 
		#Turno del atacante
		self.energy = 100
		self.amigos = self.getAmigos()
		self.location = self.robot.location()
		self.energy -= 1
		
		self.angAmigos = self.getangAmigos()

		self.angEnemigos = self.getangEnemigos()
	
		self.angle = self.selectangle()
		self.comprobarMinas()
		self.accion()

		self.contTurn += 1

	def selectangle(self, current = None):
		for anguloEnemigo in self.angEnemigos:
			for angle in self.angAmigos:
				if(angle < anguloEnemigo + 10 and angle > anguloEnemigo - 10):
					angle = -1
				else:
					angle = anguloEnemigo
		return angle
				
	def accion(self, current = None):
		if(self.energy > 50 and self.angle > -1):
            distancia = random.randint(1,10)*100
            print("Disparando atacante")
            self.disparar(self.angle, distancia)
            self.energy -= 50

		if(self.energy > 60):
			print("moviendose el atacante")
			self.moverRobot(self.location)
			self.energy -= 60
			

	def getAmigos(self, current = None):
		amigos = dict()
		lista = self.robotControllerContainer.listController()
		print("Buscando robot amigos")
		for i in range(0, len(lista)):
			keys = lista.keys()[i]
			values = lista.values()[i]
			if(self.jugador) in keys:
				amigos[keys] = values

		return amigos
        
	def moverRobot(self, current = None):

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


	def getangEnemigos(self, current = None):
		angEnemigos=[]
		for keys in self.amigos.keys():
			if("defensa") in keys:
				print("Enviando coordenadas enemigas")
				defen = drobots.ControllerDefensorPrx.checkedCast(self.amigos[keys])
				coordX = defen.getCoordenadaEnemigoX()
				coordY = defen.getCoordenadaEnemigoY()
				print("X: "+coordX+"Y: "+coordY)
				angle = self.calcularAngulo(coordX, coordY)
				angEnemigos.append(angle)

			if("detector") in keys:
				detec = drobots.ControllerDetectorPrx.checkedCast(self.amigos[keys])
				pos = detec.getEnemigo()
				print("Calcular posicion mediante el angulo")
				angle = self.calcularAngulo(pos.x, pos.y)
				angEnemigos.append(angle)

		return angEnemigos


	def getangAmigos(self, current = None):
		angAmigos=[]
		for keys in self.amigos.keys():
			if("atacante") in keys:
				atac = drobots.ControllerAtacantePrx.checkedCast(self.amigos[keys])
				coord = atac.getPosicionAmiga()
				angle = self.calcularAngulo(coord.x, coord.y)
				angAmigos.append(angle)

			elif("defensa") in keys:
				defen = drobots.ControllerDefensorPrx.checkedCast(self.amigos[keys])
				coord = defen.getPosicionAmiga()
				angle = self.calcularAngulo(coord.x, coord.y)
				angAmigos.append(angle)

		return angAmigos


	def calcularAngulo(self, coordX, coordY, current = None):
		pX = math.fabs(coordX - self.location.x)
		pY = math.fabs(coordY - self.location.y)
		angle = int(math.degrees(math.atan2(pY,pX)))
		if(angle < 0):
			angle = angle + 360
		elif(angle >= 360):
			angle = 0
		return angle

	def disparar(self, angle, dist, current = None):
        self.robot.cannon(angle, dist)
        self.angle = -1



	def getPosicionAmiga(self, current = None):
		location = self.robot.location()
		return location

	def robotDestroyed(self, current = None):
		print("Destroyed Robot")