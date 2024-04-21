## Challenge List

### Pwn

| Done? | Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - | - |
| y | Baby fmtstr | buffer overflow using strftime (using format string) into command to be executed, done by changing locale into something ending with 'sh' | 2 | 31234 |
| y | The Motorola 1 | simple ret2win with source code provided | 1 | 30211 |
| y | The Motorola 2 | wasm buffer overflow. buffer overflow from stack into the heap (fix dlmalloc header during overflow to not crash) | 3 | 30212 |
| y | Baby Goods | buffer overflow + ret2win | 1 | 32345 |
| y | heapheapheap | Worst fit heap implementation using a heap | 5 | 33456 |
| y | Slingring Factory | fmtstr to leak canary, uaf to leak address in libc, use static offset to find libc base, ret2libc with bof | 3.5-4 | 35678 |

### Crypto

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| filter-ciphertext | Implementation error | 1 | 32222 |
| filter-plaintext | Decryption oracle vulnerable to XOR | 1.5 | 32223 |
| AES | Attack AES without mix-columns | 2 | 35100 |
| PRG | Exploiting linear relationship and win the PRG game | 2.5 | 35101 |
| IPFE | Completely recover the secret value of Inner Product Functional Encryption by breaking the DDH assumption | 3 | 35102 |
| Curve | Solve DDH on tate pairing compatible curve | 4 | - |
| Coding | Breaking Code-based cryptography that uses linear code | 4 | 35103 |

### Web

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| No Sql Injection | auth is stored in MySql as base64 data. MySql queries are not case sensitive which allows corruption by confusing upper and lower case in base64 encoded auth token | 3-4 | 33336 |
| Markdown Parser | XSS in Markdown fenced code block | 1-2 | 33335 |
| GreyCTF Survey | Improper use of `parseInt` leads to unexpected results | 2 | 33334 |
| Fearless Concurrency 🦀🦀🦀 | Improper use of synchronization | 3 | 33333 |
| Baby Web | Basic warmup challenge | 1 | 33338 |
| Beautiful Styles | CSS XS-Leak | 2.5 | 33339 |

### Reverse Engineering

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| cooking mama | rust sudoku | 3 | - |
| mazeware | multi stage shellcode api hooking | 3 | - |
| pattern enigma matrix | cpp regex runtime matching | 3 | - |
| phaserjs-tutorial | javascript stuff? | 3 | 39876 |
| bee's password | python code optimization with data structure | 3 | - |
| serialcrypt | modified XXTEA | 3 | - |

### Blockchain

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| Greyhats Dollar | Transfer GHD to yourself to duplicate your balance | 1 | 30201, 30202 |
| Simple AMM Vault | Reset the vault share price to drain the AMM | 2-3 | 30301, 30302 |
| Voting Vault | Abuse rounding down to make votes underflow to a huge value when calling `delegate()` | 2-3 | 30401, 30402 |
| Escrow | Incorrect calldata size check in `initialize` can be bypassed by specifying ETH address as 19 zero bytes | 4 | 30101, 30102 |


### Miscellaneous

| Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| - | - | - | - |
| Grey Divers | Hell Divers 2 osint challenge | 1 | - |
| cats at the beach | osint challenge at the beach! | 1 | - |
| All About Timing | random seed by time at connection time | 1 | 31111 |
| Poly Playground | find polynomial coefficients | 1 | 31113 |
| Maze Runner | modified dfs | 2-3 | 31112 |
| Verilog Count | Describe an adder in verilog and do basic addition. | 2 | 31114 |
| Out In Plain Sight | flag is hidden in publicity video on instagram | 1 | - |
| CashHat The Ripper | brute forcing zip file password | 2 | - |

### Greycat's Adventure

| Name | Challenge Details | Estimated Difficulty (1-5) |
| - | - | - |
| Achievement 1 | Using cheat engine, hack the score to achieve a highscore of 1337420. | 2 |
| Achievement 2 | Using cheat engine, hack the money to purchase all items from the shop. Scan float instead of default (4-bytes). | 2.5 |
| Achievement 3 | View credit page and recognise that there is morse code hidden in the text. Concat and decode morse code to find secret. Use secret to unlock achievement for flag. | 2 |
| Timelock | Use speedhack to speed up the wait time. | 1.5 |
| Vault | Use speedhack to slow down the game and copy down the flag. | 1.5 |

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
