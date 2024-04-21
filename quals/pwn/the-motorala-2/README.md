
# Challenge Summary

buffer overflow in a wasm binary. since the stack and the heap is adjacent in memory, we can do a stack overflow to overwrite the heap buffer

there is one small issue, where we will overwrite crucial metadata when overwriting into the heap buffer. however, there is no ASLR in wasm, we can just dump that section of memory in a debugger, then write it back in during our overflow.

# Challenge Description

same source code, same bug, easy solve?

# Author

Elma

# Hints

NIL

# Flag

`grey{s1mpl3_buff3r_0v3rfl0w_w4snt_1t?_r3m3mb3r_t0_r34d_th3_st0ryl1ne:)}`

# Learning Objectives

linear memory in wasm

lack of randomization in wasm

security protections of a wasm binary
