import requests

response = requests.get("https://api.ipify.org?format=json")
data = response.json()
print(f"Your Real IP Address is {data['ip']}")
