#!/usr/bin/make -f
# -*- mode:makefile -*-


all:
	gnome terminal -e "./Container.py --Ice.Config=container.config"

	gnome terminal -e "./Factoria.py --Ice.Config=factoryA1.config"
	gnome terminal -e "./Factoria.py --Ice.Config=factoryA2.config"
	gnome terminal -e "./Factoria.py --Ice.Config=factoryD1.config"
	gnome terminal -e "./Factoria.py --Ice.Config=factoryD2.config"


	gnome terminal -e "./Main.py --Ice.Config=client.config"
clean:
