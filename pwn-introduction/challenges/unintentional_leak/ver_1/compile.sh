#!/usr/bin/bash

gcc unintentional1.c -o unintentional1 -Wl,-z,relro,-z,now
