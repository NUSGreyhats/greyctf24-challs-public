## HTTP Parameter Pollution

The first vulnerability occurs in `code.gs`:
```js
UrlFetchApp.fetch(`http://challs.nusgreyhats.org:33340/form_response?teamname=${teamname}&challenge_file_id=${file_id}`, options);
```

The user-controlled `teamname` is directly interpolated into the URL, before the `challenge_file_id` parameter. This allows the attacker to inject another `challenge_file_id` to override the legitimate file id. This works because Flask uses the first occurrence of a parameter in a query string.

## XXE

The downloaded `xlsx` file is then unzipped. The `xl/sharedStrings.xml` file is then unsafely parsed:

```python
from lxml import etree as ET

parser = ET.XMLParser(load_dtd=True, no_network=False)
with zipfile.ZipFile(io.BytesIO(data)) as zf:
    ss = zf.open("xl/sharedStrings.xml", "r").read()
    shared_strings_data = ET.fromstring(ss, parser=parser)
```

This allows the attacker to extract the token using an out of band XXE attack via DTDs. PoCs for this kind of attack are readily available online. 

One possible `xlsx` is `solution.xlsx`. Once the attacker has the token, they can easily retrieve the flag via the `/flag` endpoint.