#!/bin/bash

. ./envrc.sh
if [ ! $? == 0 ]; then
	exit
fi

# Activate virtual env
bash --rcfile $TOPDIR/pip3-env/bin/activate