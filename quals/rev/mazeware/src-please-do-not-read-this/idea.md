the maze will be stored in binary data

8 bits - FLAG Y
8 bits - START Y
8 bits - FLAG X
8 bits - START X
8 bits - WIDTH
8 bits - HEIGHT
(W * H) bits - maze data

we can obfuscate with the use of nanomites

----- 

every SIGILL decrypts the next 0x20 bytes of instructions and re-encrypts the previous 0x20 bytes of instructions

-----

the maze only has ONE correct path, if the player strays from the path, the entire routine is immediately destroyed --- can we do this via api hooking?

0. we can use ptrace to constantly monitor 
1. at the end of FUNCTION ??, we will have a hidden routine that will find and decrypt a code cave, then does API hooking to point to that code cave
2. after hooking, it will destroy itself (aka the hidden routine) to avoid suspicion


if they patch to the correct flag location, print a rick roll

--- 

1. return hijack at the end of print_maze to redirect to shellcode
2. shellcode finds a code cave in LIBC .text section
3. decrypts another shellcode (from .data) using the key into the code cave
4. destroy entire first shellcode and jump to code cave
5. shellcode in code cave will egghunt for the current level by parsing the values in the stack
6. if level == 2, it will use the current x and y value to destroy the current shellcode and decrypt the next shellcode which is the real maze

---

```
##################
#   ##   #   ##F##
# # #  #   #  #  #
# #^# ####### ## #
# ### ##    #    #
#   # ## ## ######
### # ## #  #    #
#   #    # ## ## #
# ########    #  #
#  #    ####### ##
##   ##         ##
##################
```
> WWAASSSSDDSSAASSDSDDWDDDSDDDDDDDDWWDWWAAASSAAAWWDWWAAASSSAAAWWWWWDWDDSDDWDDSDSSDDDWWAW

> maze1: ssssssssssdddddddddddddawwwwwwwwwwwwwddsssssssddddddddssssssssa
