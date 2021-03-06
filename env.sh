#!/bin/bash

. ./envrc.sh
if [ ! $? == 0 ]; then
	exit
fi

# Create virtual env pip3-env if not exists
if [ ! -d "pip3-env" ]; then
	virtualenv $TOPDIR/pip3-env
fi

# Activate virtual env
bash --rcfile $TOPDIR/pip3-env/bin/activate