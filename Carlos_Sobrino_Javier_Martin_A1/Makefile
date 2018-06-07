#!/usr/bin/make -f
# -*- mode:makefile -*-

carpetas: 
	mkdir -p db
	mkdir -p db/registry

all:
	make carpetas

patch:
	icepatch2calc code

clean:
	$(RM) *~
	$(RM) *.pyc
	$(RM) code/*.pyc
	$(RM) code/*~
	sudo rm -r db/
	sudo killall icegridnode
	sudo killall -q -9 python