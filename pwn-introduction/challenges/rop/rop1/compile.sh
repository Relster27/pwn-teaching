#!/bin/bash

gcc rop1.c -o rop1 -Wl,-z,relro,-z,now -no-pie
