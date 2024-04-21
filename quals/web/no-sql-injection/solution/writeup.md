# Overview

The vulnerability stems from storing base64 encoded user tokens in MySQL.  
```js
// This is not completely safe
const result = await query("select 1 from tokens where token = ?", [token]);

if (result.length != 1) {
    return res.json({ err: "Token not found!" });
}

await query("delete from tokens where token = ?", [token]);

const { name, admin } = JSON.parse(atob(token));
```

By default mysql comparisons are case-insensitive (for some reason) so 'A' == 'a'. This is a problem for Base64 which is case sensitive, so 'A' and 'a' mean completely different things.


An attacker can exploit this vulnerability to manipulate tokens that are then parsed in an unintended way, resulting in the attacker gaining admin permissions.

# Exploitation

The original token is something like this:
```json
{"name":"dd","admin":false}
```

our target will be to corrupt it to something like this:
```json
{"name":"dd","admin":true}
```

Obviously, the field we can control here is the name field. Our goal will be to somehow smuggle in `"` so that we can escape from the quoted string and affect the other JSON properties.

Since Base64 transforms 3 byte chunks to 4 Base64 characters, we will have to corrupt groups of 3 characters.

For example, we want to inject the string `aa"`. This base64 encodes to `YWEi`. However, the string `YWei` is also a valid base64 string and decodes to `ag¢` which does not contain any bad characters.

We can pass all 256 byte values through `JSON.stringify` to determine which are 'bad' (produce more than one byte of output):
```python
bad = [
0,  1,  2,  3,  4,  5,  6,  7,  8,
9, 10, 11, 12, 13, 14, 15, 16, 17,
18, 19, 20, 21, 22, 23, 24, 25, 26,
27, 28, 29, 30, 31, 34, 92
]
```
Fortunately, much of the upper range byte values are not escaped. (This is not the case with Python's `json.dump`).

Therefore, given a string to inject, we can cycle through all 16 combinations of upper and lowercase characters to determine which do not produce any 'bad' characters.

This is implemented in `solve.py`.

After this, we can successfully escape from the quoted string and inject `"admin":true`. However, we are not done yet, as the `"admin":false` behind it will override the injected value. 

This is not a big problem as we can do the reverse process by corrupting `"admin"` to some other valid JSON key so that it will be ignored.

This is one possible safe/malicious payload combination:
```python
safe = b'{"name":"sshsh \x8a, \x8ag\xe4min\x8a:tr{\xe5\x95\xc6\xa2\xc9y\xe2\x8a3\xa2","admin":false}'

malicious = b'{"name":"sshsh ", "admin":true, "asb":"","\xc9j\xedin":false}'
```

Logging in with the altered username and password will yield the flag.