# Challenge Summary

Typical ransomware with some anti-static analysis features (eg encrypted shellcode, IAT)

# Challenge Description
Oh no! One of our services got hacked, and the attackers encrypted the flag!  
Luckily, our incident response team managed to obtain a packet capture of the attack in progress. Can you recover the flag?


> PS: the attacker is on `[::1]:43064` and the service is on `[::1]:1338`  
PPS: ignore any wireshark errors about checksums  
PPPS: pretend that the attacker is not attacking from localhost (I'm too lazy to setup a network for this)

# Author
jro

# Flag

`grey{r4n50m_m0r3_l1k3_r4nd0m_XD}`

# Learning Objectives
Some common malware analysis techniques, network traffic analysis