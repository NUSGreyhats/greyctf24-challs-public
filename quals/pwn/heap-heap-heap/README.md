# Challenge Summary

auth is stored in MySql as base64 data. MySql queries are not case sensitive which allows corruption by confusing upper and lower case in base64 encoded auth token

# Details

I heard you like heap, so I made a heap using a heap based heap!

# Author

jro

# Hints

1. Make good use of the halloc `debug` functionality.
2. Examine the chunk management algorithm more closely.


# Flag

`grey{h34p5_0f_h34p_f0r_m4x1mum_c0nfu510n}`

# Learning Objectives

1. Identify logic bugs in simple memory management algorithms
2. Organize and visualize information to develop an exploit for a custom heap allocator
    - This is hard because no attempt is made to properly align heap chunks XD