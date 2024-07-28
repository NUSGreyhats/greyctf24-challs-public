# Challenge Summary

shellcoding challenge with seccomp.

all registers are cleared except $fs, which can be used to access the TLS to find gadgets

# Details

Everyone rekt the Blob Runner so hard in Greyhats Welcome CTF 2023, I made sure to make it extra secure this time ;)

# Author

Elma

# Hints

nil

# Flag

`grey{ret_to_thread_local_storage_via_fs_register}`
