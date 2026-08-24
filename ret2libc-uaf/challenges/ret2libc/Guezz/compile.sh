#!/bin/bash

gcc chall.c -o chall -fno-stack-protector -Wl,-z,relro,-z,now

