## Overview
Upon decompiling the `stars` binary in IDA, we observe something like this:

![](https://storage.googleapis.com/files.junron.dev/greyctf-2024-9b83e2811d4afc06f3665a962d76a838/Screenshot%202024-07-20%20153046.png)

The program has been obfuscated with excessive levels of pointer indirection.

## Setup
Scrolling past the variable declarations, the decompilation becomes a little more informative:
```c
dest = mmap((void *)0x1337000, 0x10000uLL, PROT_WRITE|PROT_READ, MAP_ANON|MAP_PRIVATE, -1, 0LL);
memcpy(dest, &unk_4008, 0x44E0uLL);
memfrob(dest, 0x44E0uLL);
lineptr = 0LL;
n = 0LL;
getline(&lineptr, &n, stdin);
v3 = strlen(lineptr);
v275 = ****************************************************(int ****************************************************)dest
    * v3;
if ( v275
    % ****************************************************((int ****************************************************)dest
                                                        + 2) )
{
exit(-1);
}
  ```

A large chunk of memory `dest` is allocated at address `0x1337000`. `0x44e0` bytes from a constant memory region `unk_4008` is copied into `dest`, which is then XORed with `42`.

A line of input is then read into the `lineptr` variable. The length of the input is then multiplied with a constant, obtained from `****************************************************(int ****************************************************)dest`. While it is possible to analyze the structure of `dest` to determine what happens if we dereference it 52 times, it is much easier to just use a debugger.

Using the IDA debugger, we can see that the value of `dest` dereferenced 52 times is `8`:
![](https://storage.googleapis.com/files.junron.dev/greyctf-2024-9b83e2811d4afc06f3665a962d76a838/Screenshot%202024-07-20%20133944.png)

Next, the result of `strlen(lineptr) * 8` is divided by another constant located in `dest`. If the input is not divisible by this new constant, the program exits. Again, we can use the debugger to determine that this value is 9.

## Stars
After the program initializes buffers and reads input, it sets up a long chain (of 255 pointers) that eventually points to `v269`, which holds the value `0`.
```c
v269 = 0;
v268 = &v269;
v267 = &v268;
v266 = &v267;
v265 = &v266;
v264 = &v265;
v263 = &v264;
v262 = &v263;
v261 = &v262;
v260 = &v261;
v259 = &v260;
v258 = &v259;
v257 = &v258;
v256 = &v257;
v255 = &v256;
v254 = &v255;
v253 = &v254;
v252 = &v253;
// ...
v16 = &v17;
v15 = &v16;
v272 = &v15;
```
It is this long chain of indirection that results in the sea of `*` that appears when the program is first decompiled.

The chain ends at `v272`, such that when `v272` is dereferenced 255 times, we end up with the value 0. 

To deal with the massive amount of `*`, let `*[N]` represent the character `*` repeated `N` times. For example `v272` would have type `int *[255]`

We can use a bit of Python code to convert IDA's decompilation to our new convention:
```python
import re
re.sub(r"\*{4,}", lambda x: f"*[{len(x.group())}]", code)
```

Let's run this transformation on the remainder of the program:

```c
while ( 1 )
{
    v12 = *[128]v272;
    v13 = *[127]v12;
    if ( v13 >= num_bits_of_input )
        break;
    v5 = *[128]v272;
    v6 = *[127]v5;
    if ( ((lineptr[(int)(v6 / *[52](int *[52])dest)] >> (v6 % *[52](int *[52])dest)) & 1) != 0 )
    {
        if ( !v288 )
        v286 = (__int64 *)v273[1];
        if ( v288 == 1 )
        v285 = (__int64 *)v286[1];
        if ( v288 == 2 )
        v284 = (__int64 *)v285[1];
        if ( v288 == 3 )
        v283 = (__int64 *)v284[1];
        if ( v288 == 4 )
        v282 = (__int64 *)v283[1];
        if ( v288 == 5 )
        v281 = (__int64 *)v282[1];
        if ( v288 == 6 )
        v280 = (__int64 *)v281[1];
        if ( v288 == *[52]((_DWORD *[52])dest + 1) )
        v279 = (int *[2])v280[1];
        if ( v288 == *[52](_DWORD *[52])dest )
        v278 = v279[1];
    }
    else
    {
        if ( !v288 )
        v286 = (__int64 *)*v273;
        if ( v288 == 1 )
        v285 = (__int64 *)*v286;
        if ( v288 == 2 )
        v284 = (__int64 *)*v285;
        if ( v288 == 3 )
        v283 = (__int64 *)*v284;
        if ( v288 == 4 )
        v282 = (__int64 *)*v283;
        if ( v288 == 5 )
        v281 = (__int64 *)*v282;
        if ( v288 == 6 )
        v280 = (__int64 *)*v281;
        if ( v288 == *[52]((_DWORD *[52])dest + 1) )
        v279 = (int *[2])*v280;
        if ( v288 == *[52](_DWORD *[52])dest )
        v278 = *v279;
    }
    ++v288;
    v7 = *[128]v272;
    v8 = *[127]v7;
    *[127]v7 = v8 + 1;
    if ( v288 == *[52]((_DWORD *[52])dest + 2) )
    {
        v9 = v287 / *[52](int *[52])dest;
        v10 = ((1 << (*[52](_DWORD *[52])dest - v287 % *[52](int *[52])dest)) - 1) & *v278;
        output[v9] |= v10 << (v287 % *[52](int *[52])dest);
        v11 = *v278 >> (*[52](_DWORD *[52])dest - v287 % *[52](int *[52])dest);
        output[v287 / *[52](int *[52])dest + 1] = v11;
        v288 = 0LL;
        v287 += *[52]((int *[52])dest  + 2);
    }
}
for ( i = 0LL; i < v287 / *[52](int *[52])dest; ++i )
{
    printf("%02x", (unsigned __int8)output[i]);
}
putchar(10);
return 0LL;
```
This still isn't great, but it's much cleaner than before.  
From earlier, we have already determined the following values using the debugger:

- `*[52](int *[52])dest` is 8
- `*[52]((_DWORD *[52])dest + 2)` is 9

Now, to detemine the value `*[52]((_DWORD *[52])dest + 1)`, we can either use the debugger again, or we can observe the series of `if` statements below:

```c
if ( !v288 )
v286 = (__int64 *)*v273;
if ( v288 == 1 )                             // 1
v285 = (__int64 *)*v286;
if ( v288 == 2 )                             // 2
v284 = (__int64 *)*v285;
if ( v288 == 3 )                             // 3
v283 = (__int64 *)*v284;
if ( v288 == 4 )                             // 4
v282 = (__int64 *)*v283;
if ( v288 == 5 )                             // 5
v281 = (__int64 *)*v282;
if ( v288 == 6 )                             // 6
v280 = (__int64 *)*v281;
if ( v288 == *[52]((_DWORD *[52])dest + 1) ) // ???
v279 = (int *[2])*v280;
if ( v288 == *[52](_DWORD *[52])dest )       // 8
v278 = *v279;
```

We can guess (and subsequently verify) that `*[52]((_DWORD *[52])dest + 1)` is equal to 7.

Next, let's deal with `v272`. We can observe that `v272` is involved in the loop condition:
```c
while ( 1 )
{
    v12 = *[128]v272;
    v13 = *[127]v12;
    if ( v13 >= num_bits_of_input )
        break;

    // ...
}
```
Additionally, it is incremented at the end of the loop:
```c
    v7 = *[128]v272;
    v8 = *[127]v7;
    *[127]v7 = v8 + 1;
```
With this evidence, we can be quite confident that `*[255]v272` is the loop counter/index into the input. 

Note that the program appears to be processing our input at the bit level, instead of at the byte level (we know this because `*[255]v272` is compared against the number of bits in the input).

Let's replace the constants and loop counter with their original, deobfuscated forms:
```c
int counter = 0;

while ( 1 )
{
    if ( counter >= num_bits_of_input )
        break;
    if ( ((lineptr[(int)(counter / 8)] >> (counter % 8)) & 1) != 0 )
    {
        if ( !v288 )
        v286 = (__int64 *)v273[1];
        if ( v288 == 1 )
        v285 = (__int64 *)v286[1];
        if ( v288 == 2 )
        v284 = (__int64 *)v285[1];
        if ( v288 == 3 )
        v283 = (__int64 *)v284[1];
        if ( v288 == 4 )
        v282 = (__int64 *)v283[1];
        if ( v288 == 5 )
        v281 = (__int64 *)v282[1];
        if ( v288 == 6 )
        v280 = (__int64 *)v281[1];
        if ( v288 == 7 )
        v279 = (int *[2])v280[1];
        if ( v288 == 8 )
        v278 = v279[1];
    }
    else
    {
        if ( !v288 )
        v286 = (__int64 *)*v273;
        if ( v288 == 1 )
        v285 = (__int64 *)*v286;
        if ( v288 == 2 )
        v284 = (__int64 *)*v285;
        if ( v288 == 3 )
        v283 = (__int64 *)*v284;
        if ( v288 == 4 )
        v282 = (__int64 *)*v283;
        if ( v288 == 5 )
        v281 = (__int64 *)*v282;
        if ( v288 == 6 )
        v280 = (__int64 *)*v281;
        if ( v288 == 7 )
        v279 = (int *[2])*v280;
        if ( v288 == 8 )
        v278 = *v279;
    }
    ++v288;
    counter++;
    if ( v288 == 9 )
    {
        v9 = v287 / 8;
        v10 = ((1 << (8 - v287 % 8)) - 1) & *v278;
        output[v9] |= v10 << (v287 % 8);
        v11 = *v278 >> (8 - v287 % 8);
        output[v287 / 8 + 1] = v11;
        v288 = 0LL;
        v287 += 9;
    }
}
for ( i = 0LL; i < v287 / 8; ++i )
{
    printf("%02x", (unsigned __int8)output[i]);
}
putchar(10);
return 0LL;
```

At this point, we've pretty much defeated the pointer obfuscation and obtained the original source code of the program.

## Analysis

The main loop of the code can be broken down into 3 parts:
```c
v287 = 0LL;
v288 = 0LL;
counter = 0;
while ( 1 )
{
    if ( counter >= num_bits_of_input )
        break;
    if ( ((lineptr[(int)(counter / 8)] >> (counter % 8)) & 1) != 0 )
    {
        // part 1
        if ( !v288 )
        v286 = (__int64 *)v273[1];
        // ...
        v279 = (int *[2])v280[1];
        if ( v288 == 8 )
        v278 = v279[1];
    }
    else
    {
        // part 2
        if ( !v288 )
        v286 = (__int64 *)*v273;
        // ...
        if ( v288 == 8 )
        v278 = *v279;
    }
    ++v288;
    counter++;
    if ( v288 == 9 )
    {
        // part 3
        v9 = v287 / 8;
        v10 = ((1 << (8 - v287 % 8)) - 1) & *v278; // fancy bit shifting stuff
        output[v9] |= v10 << (v287 % 8);
        v11 = *v278 >> (8 - v287 % 8);
        output[v287 / 8 + 1] = v11;
        v288 = 0LL;
        v287 += 9;
    }
}
```
Control flow enters part 1 if the bit of the input at index `counter` is set. Otherwise, it enters part 2. 

9 `if` statements are located in each of part 1 and 2. Combining the two parts, we can see that each `if` statement is structured as follows:
```c
if(v288 == N){
    if(bit_is_set){
        // part 1
        result[N+1] = result[N][1];
    } else {
        // part 2
        result[N+1] = result[N][0];
    }
}
```
Where `N` ranges from 0 to 8. 

At this point, we might realize that the loop implements the traversal of a binary tree of height 9. If the current bit of the input is set, we set the right child to be current node. If the bit is unset, we visit the left child instead. This is repeated 9 times, until we reach the leaf node, which is `result[9]`. 

This final result is then written to the `output` buffer in part 3, using some complicated looking bit manipulation which I had to debug many times.

The whole algorithm is nothing but a simple 9-bit substitution cipher, implemented in a confusing and inefficient way.

## Decryption

Now that we've understood the encryption algorithm, we just need to extract the s-box of the substitution cipher. We can either statically analyze the 9 levels of pointers in `dest`, or we can just use dynamic analysis (aka bruteforce), which is much easier.

Such a script is provided in `recover_sbox.py`. We can then use the recovered sbox to reverse the encryption to obtain the flag:
```
grey{5uch_4_h34v3nly_v13w}
```
The main difficulty of this section is correctly interpreting the input and output of the program as a byte-level little endian bitstream, while the internal processing of the program uses 9-bit chunks. 


## Trivia
- The challenge name and flag is a reference to the [song](https://open.spotify.com/track/0FDzzruyVECATHXKHFs9eJ?si=8e38110c8c76407c) of the same name.
- A 9-bit substitution cipher was chosen as [Ghost Stories](https://open.spotify.com/album/2G4AUqfwxcV1UdQjm2ouYr?si=WCZMC6KNTYO1aEeZnrQo4g) has 9 tracks. More importantly, a 9-bit cipher is harder to accidentally bruteforce than a 8-bit cipher.
    - Unfortunately, 8 and 9 are coprime, limiting the length of the flag to a multiple of 9 bytes.
- The sbox is generated using `random.shuffle` with a seed of 267, the length of A Sky Full of Stars in seconds.
- Only 3 constants and one stack variable are obfuscated because it would take too long to decompile in IDA otherwise. Also we didn't want to make this challenge too hard.
- The maximum number of times that a pointer can be dereferenced in a single line in IDA is 128, but 128 characters is not quite long enough to cover the entire screen with `*` so I went for double that.