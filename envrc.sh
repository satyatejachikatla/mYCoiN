#!/bin/bash

# Top env
export TOPDIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PATH=$PATH:$TOPDIR/vendor/bin