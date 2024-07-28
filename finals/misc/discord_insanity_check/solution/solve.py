import requests
import re

flag = requests.get("https://cdn.discordapp.com/emojis/1246722891941285980.png")
print(re.findall(r"grey{.*}", flag.text)[0])
