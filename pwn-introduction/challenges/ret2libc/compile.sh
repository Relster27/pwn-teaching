#!/bin/bash

gcc ret2libc.c -o ret2libc -Wl,-z,relro,-z,now