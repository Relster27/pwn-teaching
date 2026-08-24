#!/usr/bin/bash

gcc unintentional2.c -o unintentional2 -Wl,-z,relro,-z,now
