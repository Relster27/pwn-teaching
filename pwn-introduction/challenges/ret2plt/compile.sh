#!/bin/bash

gcc ret2plt.c -o ret2plt -fno-stack-protector -no-pie -Wl,-z,relro,-z,now