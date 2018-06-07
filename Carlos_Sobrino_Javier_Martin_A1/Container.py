#!/usr/bin/python -u
# -*- coding:utf-8; tab-width:4; mode:python -*-

#fuente: repositorio ice-hello de la asignatura
import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
'''Ice.loadSlice('-I. --all drobotsAux.ice')'''

import drobots

class ContainerI(drobots.Container):
    def __init__(self):
        self.proxies = dict()
        self.factories = dict()
        self.Controlador = dict()
        self.mines = dict()

    def link(self, key, proxy, current=None):
        if(key) in self.proxies:
            raise drobots.AlreadyExists(key)

        self.proxies[key] = proxy

    def list(self, current=None):
        return self.proxies



    def linkFactory(self, key, proxy, current=None): 
        if(key) in self.factories:
            raise drobots.AlreadyExists(key)

        self.factories[key] = proxy

    def listFactory(self, current=None): 
        return self.factories



    def linkControlador(self, key, proxy, current=None): 
        if(key) in self.Controlador:
            raise drobots.AlreadyExists(key)

        self.Controlador[key] = proxy

    def listControlador(self, current=None): 
        return self.Controlador



    def linkmines(self, key, proxy, current=None): 
        if(key) in self.mines:
            raise drobots.AlreadyExists(key)

        self.mines[key] = proxy

    def listmines(self, current=None):
        return self.mines



    def unlink(self, key, current=None):
        if not (key) in self.proxies:
            raise drobots.NoSuchKey(key)

        del self.proxies[key]


    def get(self, key, current=None):
        return self.proxies[key]

    def keys(self, current=None):
        return self.proxies.keys()

    def items(self, current=None):
        return self.proxies.items()

    def getValuefactory(self, index, current=None): 
        return self.factories.values()[index]

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servidor = ContainerI()
        adaptador = broker.createObjectAdapter("ContainerAdapter")
        proxy = adaptador.add(servidor, broker.stringToIdentity("container"))
        adaptador.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
