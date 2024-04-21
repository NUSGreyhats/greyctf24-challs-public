# Overview

It appears that the attacker only has one query to get the flag as a lock is acquired that prevents access to the database while the secret is present. However, the lock does not prevent other users from accessing the shared database. Therefore, by SLEEPing during the first user's injection, the table can be kept alive long enough for the second user to issue two queries to leak the table name, then read the table to get the flag.

See `src/main.rs` for full implementation of solution.