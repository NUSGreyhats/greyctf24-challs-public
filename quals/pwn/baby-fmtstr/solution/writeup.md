# Overview

```c
strftime(buf, 0x30, input, time_struct);
// remove newline at the end
buf[strlen(buf)-1] = '\0';

memcpy(output, buf, strlen(buf));
```

Buffer overflow occurs when the maximum 0x30 byte `buf` is copied to the `0x20` byte `output`.  
This overflows into the `command` variable, which is passed to `system`. The goal will be to overwrite the `command` variable to `sh`. 


# Exploitation

`strftime` gives us a lot of format specifiers to choose from to generate the desired string.   
As of writing this challenge, it is December (`Dec`), which in South Africa (st_ZA.utf8) is `Tsh`. 
Therefore changing the locale and sending the format string `%G%G%G%G%G%G%G%%%%%%%b` will cause the desired buffer overflow.

Upon exit, `system("sh")` will be executed.

If the CTF is held in a month/time with no possible solution it may be necessary to tweak the challenge slightly. 
The solution generation script is included as `generate_solution.py`. With so many locales and format specifiers it is likely that at least one of them will work :thinking:
