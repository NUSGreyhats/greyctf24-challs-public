# Overview

As hinted by the challenge description, the exploit starts with prototype pollution.

The next phase proceeds with a sort of buffer overflow, finally overwriting WebAssembly code to manipulate the flag checker.

# Exploitation

Prototype pollution occurs in the boringly named `copy` function in `util.js`:
```js
function copy(src, dst) {
    for (const key of Object.keys(src)) {
        const val = src[key];
        if (is_object(val)) {
            copy(src[key], dst[key]);
        } else if (typeof val == "string") {
            dst[key] = decode_user_hex_string(src[key]);
        } else {
            dst[key] = src[key];
        }
    }
}
```

The target for pollution would be `config.size` in `decode_user_hex_string`:
```js
function decode_user_hex_string(str) {
    const length = config.size;

    const buf = new Uint8Array(Buffer.from("a".repeat(length)).buffer);

    for (let i = 0; i < length * 2; i += 2) {
        const byte = parseInt(str.substring(i, i + 2), 16);
        if (Number.isNaN(byte)) {
            buf[i >>> 1] = 0;
        }
        buf[i >>> 1] = byte;
    }
    return buf;
}
```

Upon carefully reading the source code, one would discover that there is no `size` property in `config.json` (it is instead named `length`). Therefore, an attacker can use the prototype pollution vulnerability to control `config.size` and allocate arbitrarily long buffers.

Without using the prototype pollution vulnerability, the size of the buffer allocated would be 0 regardless of the length of the string and it would thus be impossible to solve the challenge.

Next, the attacker would realize that the buffer allocation mechanism is unnecessarily complex and insecure. The whole function could just be replaced with `Buffer.from(str, 'hex')`. 

The main vulnerability here is that `Buffer.from` [returns an offset into a global shared buffer](https://github.com/nodejs/node/issues/41467) which can be accessed using `Buffer.from(...).buffer`.

For example:
```js
➜  proto_grader node
Welcome to Node.js v18.13.0.
Type ".help" for more information.
> a = Buffer.from('a')
<Buffer 61>
> b = Buffer.from('b')
<Buffer 62>
> a.buffer == b.buffer
true
> a.buffer
ArrayBuffer {
  [Uint8Contents]: <2f 1c 5f ed 42 7f 00 00 2f 1c 5f ed 42 7f 00 00 61 00 00 00 00 00 00 00 62 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 46 61 73 74 42 75 66 66 65 72 66 65 42 75 66 66 a8 04 99 b4 d4 55 00 00 30 3d 9e b4 d4 55 00 00 0a 00 00 00 00 00 00 00 e2 72 82 0a 01 00 00 00 62 75 66 66 ... 8092 more bytes>,
  byteLength: 8192
}
```

So the `decode_user_hex_string` incorrectly pollutes the global shared buffer instead of writing to the offset that `Buffer.from` assigned to it.

Let's examine the contents of the global shared buffer at the point `decode_user_hex_string` is called:
```
//const fs = require("fs");
const code = fs.readFileSync(__dirname + "/grader/grader.wasm");

const util = require("./util.js")
const grader = require("./grader")
const flag = util.config.flag;


const src = JSON.parse(atob(process.argv[2]));

const dst = {};
util.copy(src, dst);

const input = dst["input"];

if (!input) {
    console.log("???");
} else {
    console.log(grader(code, input, flag));
}
asm`envmemory▒
                             levenshteinmemory
��@  Ak- -cFA
                            @ Ak! Ak!


                                     @  K - -dFA
                                                @ Aj!


                                                       k"E  k"AIr@ 
```

As this is a shared global memory buffer, we see lots of interesting stuff. First appears to be the source code of `index.js`. Next are some lines containing `asm` and `envmemory`. We may guess that this is the WASM code for the grader.

Interestingly, `fs` returns buffers that are subsections of the global shared buffer (as of Node.js 18)! Therefore, if we can overwrite the global shared buffer, can possibly control what WASM code is executed and thus manipulate the grading process and get the flag. 

However, the shared buffer has a maximum size of 8192 bytes. If this is not enough, `Buffer.from` will return a new buffer and we won't be able to overwrite the WASM code. Therefore, we must limit the size of the payload.

If we send 500 `0xff` bytes, we observe the following error:
```
/app/backend/grader/index.js:22
   const module = new WebAssembly.Module(code);
                  ^ 
 CompileError: WebAssembly.Module(): expected magic word 00 61 73 6d, found ff ff ff ff @+0
     at module.exports (/app/backend/grader/index.js:22:18)
     at Object.<anonymous> (/app/backend/index.js:19:17)
     at Module._compile (node:internal/modules/cjs/loader:1105:14)
     at Module._extensions..js (node:internal/modules/cjs/loader:1159:10)
     at Module.load (node:internal/modules/cjs/loader:981:32)
     at Module._load (node:internal/modules/cjs/loader:827:12)
     at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:77:12)
     at node:internal/main/run_main_module:17:47
 
 Node.js v18.0.0
```

This demonstrates that we have successfully modified the WASM code. Now, we can use binary search/actually examine the global buffer to determine the appropriate offset. Fortunately, we don't seem to overwrite anything else that's actually important. 

Anyway, we can determine the offset to be 424. Now we just need to find what code to inject to get the flag. One thing to note is that the size of the code must be exactly the same as the size of the buffer has already been fixed.

The easiest way to do this is to modify the `.wat` file that is produced when the `index.ts` file is complied (source helpfully provided). Two places will be need to modified to ensure that the return value of the function is always 0 (or something < 3). Luckily, this replacement is fairly easy and straightforward as it doesn't change the size of the bytecode.

The modified `wat` can be found in `solution.wat` and is compiled to `solution.wasm`. Now, the only thing left is to send the payload to the server (see `solve.py`) and the flag will be returned.