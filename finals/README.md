## Challenge List

port range: `30000-50000`

### Pwn


| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| memecat | Free of invalid pointer  | 4 | 34567 |
| overly simplified pwn challenge | ret2dlresolve but u actually need to know what ure doing :3 | 4 | 35123 |
| super secure blob runner | shellcoding with seccomp, use $fs register to access TLS to restore register values and make syscalls | 2.5 | 35678 |
| AVL | ?? | ?? | 34569 |

### Crypto

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| HMAC-CRC | abuse CRC xor magic | 2.5 | 32000 |
| RC4 Signing Scheme | exploit RC4 key scheduling to forge same state | 2 | 32001 |
| Baby RSA | Simple RSA | 1 | - |
| Learning With Mistakes | LWE but with GF(2^n) instead of Zmod(2^n) | 3 | - |

### Web

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| Proto Grader | Various types of NodeJS global state corruption | 3-4 | 33337 |
| GreyCTF Survey (REAL!) | XXE via Excel | 3 | 33340 |
| Hi Doggy | Sanitising template engine AST | 2-3 | 33433 |
| Flag Shop | Invoke unintended functions via JS Protoype vulnerability | 2-3 | 33335 |


### Reverse Engineering

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| overly simplified rev challenge | heavily obfuscated program | 4 | - |
| A Sky Full of Stars | 200 levels of pointer indirection | 2 | - |
| Ransomware | ransomware delivered over network | 3 | - |
| hungry ghost festival | retf to transit from 64 bit to execute 32 bit shellcode. | 1 | - |

### Blockchain

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| Gnosis Unsafe | ?? | ? | 33321, 33322 |
| Meta Staking | ?? | ? | 33325,33326 |

### Miscellaneous

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| Discord Insanity Check | flag is hidden in the strings of the png emoji of gigachad | 1.5 | - |
| 13-piece Puzzle | Find all solutions to a puzzle | 5 | - |
| Poolside Paradise Or Criminal Hideout | geoint/osint | 2 | - |
| Tones 2 | ? | ? | ? |
| FoxHunt | ? | ? | ? |

### Hardware

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| Hornet 9 Homework | simple q&a, answers can be googled | 1 | - |
| Short | connect 2 pads together as told by the badge | 1 | - |
| Name | understand that stm32 uses printf, and `%s` to read the flag | 2 | - |
| Serialous | connect 2 badges together to read the uart data | 3 | - |
| Bootloader | pull boot1 high to bypass password, dump out the firmware, and reverse xors | 4 | - |

### DSTA

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| RF Signal Analysis | demodulation of radio frequencies to decrypt the flag | 2 | - |
| IP Camera | cgi-bin vulnerabilities | 2.5 | - |

## Challenge Creation Template

### File Organization

```
.
├── README.md
├── docker_compose.yml
├── distribution/
│   └── files_to_be_distributed_on_CTFd
├── service/
│   ├── Dockerfile
│   └── files_required_for_hosting_remote
├── solve.py (if possible)
└── flag.txt
```

### README Templates

Essentially, all **README.md** files should contain the following information

| Things to include               | Example                                                                   |
| ------------------------------- | ------------------------------------------------------------------------- |
| Challenge Details               | `Caesar thought of the perfect cipher. Can you break it?`                 |
| Possible hints                  | `Hint: What Caesar Cipher?`                                               |
| Key concepts                    | `Scripting`                                                               |
| Solution (Can also be a script) | `Write a script to brute force all the combinations of the caesar cipher` |
| Learning objectives             | `Learn about the Caesar Cipher`                                           |
| Flag                            | `grey{salad_is_great_but_cipher_is_not}`                                  |

copy from [templates](./templates/README.md) as necessary

### Dockerfile Templates

copy from [dockerfile template](./templates/dockerfile) and [docker-compose.yml template](./templates/docker-compose.yml) as per necessary
