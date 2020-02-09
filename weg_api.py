import requests

url = "https://api.wegmans.io/products/search?query=Milk&api-version=2018-10-18&subscription-key=e79ddcf58c304ed9ad482ba020726690"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
