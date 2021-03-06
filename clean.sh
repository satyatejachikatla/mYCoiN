#!/bin/bash

. ./envrc.sh
if [ ! $? == 0 ]; then
	exit
fi


find $TOPDIR | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

