#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
import os
Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')
import drobots
import math
import random
import ControllerDefensor
import ControllerAtacante
import ControllerDetector

class FactoriaI(drobots.ControllerFactory):

	def make(self, robot, tipo, jugador, container, contador, current=None, mines):

		if(tipo == "defensa"):
			ControladorServidor = ControllerDefensor.RobotControllerDefensorI()
			Controladorproxy = current.adapter.addWithUUID(ControladorServidor)
			directProxyController = current.adapter.createDirectProxy(Controladorproxy.ice_getIdentity())
			controlador = drobots.ControllerDefensorPrx.checkedCast(directProxyController)
			
			key = tipo+"-"+str(contador)+"-"+jugador
			container.linkControlador(key,controlador)
			controlador.setRobot(robot, jugador, container, mines)

		if(tipo == "ataque"):
			ControladorServidor = ControllerAtacante.RobotControllerAtacanteI()
			Controladorproxy = current.adapter.addWithUUID(ControladorServidor)
			directProxyController = current.adapter.createDirectProxy(Controladorproxy.ice_getIdentity())
			controlador = drobots.ControllerAtacantePrx.checkedCast(directProxyController)

			key = tipo+"-"+str(contador)+"-"+jugador
			container.linkControlador(key,controlador)
			controlador.setRobot(robot, jugador,container, mines)

		return controlador

	def makeDetector(self, tipo, jugador, container, contador, current=None):

		ControladorServidor = ControllerDetector.RobotControllerDetectorI()
		Controladorproxy = current.adapter.addWithUUID(ControladorServidor)

		directProxyController = current.adapter.createDirectProxy(Controladorproxy.ice_getIdentity())
		controlador = drobots.ControllerDetectorPrx.checkedCast(directProxyController)
		key = tipo+"-"+str(contador)+"-"+jugador
		container.linkControlador(key,controlador)

		return controlador


class Server(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		servidor = FactoriaI()

		adaptador = broker.createObjectAdapter("FactoryAdapter")
		proxy = adaptador.add(servidor, broker.stringToIdentity("factoria"))

		proxyContainer = broker.stringToProxy("container")
		factoriasContainer = drobots.ContainerPrx.checkedCast(proxyContainer)
		factoriasContainer.linkFactory("Factoria"+"-"+str(os.getpid()), proxy)

		adaptador.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
 
		return 0

if __name__ == '__main__':
	sys.exit(Server().main(sys.argv))	
