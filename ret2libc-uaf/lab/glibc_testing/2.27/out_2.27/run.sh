#!/usr/bin/bash
DIR=$(dirname "$0")
LD_LIBRARY_PATH=$DIR $DIR/ld.so $DIR/main
