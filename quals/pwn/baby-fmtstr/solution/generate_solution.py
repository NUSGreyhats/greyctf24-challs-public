import locale
import os
import datetime

locales = os.popen("locale -a").read().split("\n")
locales = [x for x in locales if '.' in x]

now = datetime.datetime.now()
possible = ["%a", "%A", "%b", "%B", "%p"]

target = b"sh"
for loc in locales:
    locale.setlocale(locale.LC_TIME, loc)
    for fmtstr in possible:
        result = now.strftime(fmtstr).encode()
        if len(result) == 0:
            continue
        if result[-2:] == target:
            print(loc, fmtstr)
            exit(0)

print("Not found :(")