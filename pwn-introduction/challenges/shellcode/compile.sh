#!/bin/bash

gcc shellcode.c -o shellcode -no-pie -fno-stack-protector -z execstack
