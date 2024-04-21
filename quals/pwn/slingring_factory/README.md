# Challenge Summary

3 separate vulnerabilities exist in the binary: format string, uaf (read -> info leak), buffer overflow

All security mitigations enabled

First use format string to leak canary

In order to use the uaf for info leak, we need to fill up the tcache bins and free 1 more bin on top of that. To prevent coalescing, 1 bin needs to be on top. Hence, a total of 9 bins should be created, 8 should be freed. Since there's a uaf in discard_rings(), show_slingrings() will actually display an address on the heap as a string.

This info leak works because the size of the slingrings struct is 0x84 (0x80 description, 0x4 amt), which means that it is within both tcache and smallbins (and hence by extension, unsorted bin) size. So first 7 frees would go into tcache, 8th will go into unsorted bin and hence point to main arena. 9th bin must still be malloc'd to prevent coalescing.

Once an address in libc is leaked via show_slingrings(), libc base can be calculated, then just perform ret2libc bof with the use_slingring() function.

# Challenge Description

In following Greycat's adventures, you have stumbled upon a factory that produces weirdly-shaped rings. Upon closer inspection, you realise that the rings seem very familiar -- they looked exactly like the Sling Rings you saw from the Marvel Comics universe! Having some time leftover, you decide to explore the factory. Alas, you eventually come to realise that these Sling Rings were in fact not the same as those you knew: during forging, their destinations have to already be set. You wonder what you could do with these rings...

# Author

uhg

# Hints

NIL

# Flag

`grey{y0u_4r3_50rc3r3r_supr3m3_m45t3r_0f_th3_myst1c_4rts_mBRt!y4vz5ea@uq}`

# Learning Objectives

- How to bypass canary
- How to make use of limited format string for information leak
- How does malloc() and free() work: tcache, smallbins etc.
- ret2libc
