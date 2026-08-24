# Challenge Exploitation Flow

## Ret2libc
### 1. The Troll Zone
Vuln: Format string leak -> Buffer overflow -> ret2libc

### 2. Guezz
[GO CREATE THE CHALLENGE] \
Vuln: Intentional leak -> Buffer overflow -> ret2libc

### 3. Mr. Blue Melville
Vuln: Arbitrary file read -> Limited read on heap chunk -> Buffer overflow -> ret2libc

## Use-After-Free
### **1. Hazy submission**
Libc ver: 2.27 \
Vuln: `Direct UAF` \
Shell:
- Overwrite `__free_hook` atau `__malloc_hook`

Full writeup: https://docs.google.com/document/d/1E6UUQlgKprjTwF7Q49fqFJ8q6b1kQ_6S01ulTCOPHsk/edit?tab=t.0

### **2. Baby Heap**
Libc ver: 2.39 \
Vuln: `Direct UAF` \
Shell:
- Overwrite `__exit_funcs`
- ROP on stack (ret2libc)

Full writeup: https://relster.gitbook.io/home/ctf/pwn/justctf-2025-babyheap

### **3. Double Trouble**
Libc ver: 2.36 \
Vuln: Type-confusion -> one byte overflow -> `Indirect UAF` \
Shell: 
- ROP on stack (ret2libc)
- Overwrite `__exit_funcs`
- File Struct Oriented Programming (FSOP)
