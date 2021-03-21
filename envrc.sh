#!/bin/bash

# Top env
export TOPDIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PATH=$PATH:`find $TOPDIR/vendor/ -name "node-v*" -type d`/bin
export PATH=$PATH:`find $TOPDIR/vendor/ -name "mongodb-*" -type d`/bin


export MONGDB_DBPATH=$TOPDIR/runningdb/
mkdir -p $MONGDB_DBPATH