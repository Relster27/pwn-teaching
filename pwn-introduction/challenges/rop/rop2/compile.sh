#!/bin/bash

gcc rop2.c -o rop2 -Wl,-z,relro,-z,now -no-pie
