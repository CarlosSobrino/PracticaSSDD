#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-


import sys
import Ice
import random
import math

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots

class Cliente(Ice.Application):
    def run(self, argv):   
        participante = "Jugador" + str(random.randint(0,999))
        broker = self.communicator()
        proxycontenedor = broker.stringToProxy("container")
        cont = drobots.ContainerPrx.checkedCast(proxycontenedor)
        
        adaptador = broker.createObjectAdapter("PlayerAdapter")
        servPlayer = PlayerI(participante,cont)
        proxPlayer = adaptador.addWithUUID(servPlayer)
        directProxPlayer = adaptador.createDirectProxy(proxPlayer.ice_getIdentity())
        player = drobots.PlayerPrx.uncheckedCast(directProxPlayer)

        adaptador.activate()
        

        try:
            print('Logeando.')
            game.login(player, participante)
            print('waiting for Robot.')
        except drobots.GameInProgress:
            print("Game in Progress.")
        except drobots.InvalidProxy:
            print("Invalid Proxy")
        except drobots.InvalidName as e:
            print("Invalid Name")
            print(str(e.reason))
        except drobots.BadNumberOfPlayers:
            print("Numbers of Players Invalid")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()
 
        return 0

class PlayerI(drobots.Player):
    def __init__(self, participante, cont):
        self.participante = participante
        self.cont = cont
        self.count = 0
        self.countDetec = 0
        self.countMinas = 0
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]
        
    def makeController(self, robot, current=None):
        print("Make Controller, indice: " +str(self.count))
        lista = self.cont.listFactory()

        if(robot.ice_ids() == ['::Ice::Object', '::drobots::Attacker', '::drobots::RobotBase']):
            print("Robot Atacante")
            factory = drobots.ControllerFactoryPrx.checkedCast(lista.values()[self.count])
            controlador = factory.make(robot, "ataque", self.participante, self.cont, self.count, mines)
            self.count = self.count + 1

        elif(robot.ice_ids() == ['::Ice::Object', '::drobots::Defender', '::drobots::RobotBase']):
            print("Robot Defensor")
            factory = drobots.ControllerFactoryPrx.checkedCast(lista.values()[self.count])
            controlador = factory.make(robot, "defensa", self.participante, self.cont, self.count, mines)
            self.count = self.count + 1
       
        return controller

    def makeDetectorController(self, current=None):
     
        factoria = drobots.ControllerFactoryPrx.checkedCast(self.cont.listFactory().values()[self.countDetec])
        controller = factoria.makeDetector("detector", self.participante, self.cont, self.countDetec)
        self.countDetec = self.countDetec + 1
        
        return controller

    def win(self, current=None):
        print("Has Ganado")
        current.adaptador.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has Perdido")
        current.adaptador.getCommunicator().shutdown()


    def gameAbort(self, current=None):
        print("El juego ha sido Abortado")
        current.adaptador.getCommunicator().shutdown()
    
sys.exit(Cliente().main(sys.argv))
