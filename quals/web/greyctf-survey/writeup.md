# Overview

The vulnerability stems from calling `parseInt` on a float.  
The float is first converted to a string, then to an integer.
For small enough floats, scientific notation is used when converting to a string.  
For example, `0.000000005+"" == "5e-9"`. When this is converted to an integer, the resultant value is 5.


## Solve

```bash
curl -X POST -H "Content-Type: application/json" --data '{"vote":0.00000005}' localhost:3000/vote
```