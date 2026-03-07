import requests

api_key = "42cdf13a7cec4fa33a78ef263034b5dc"
city = "Lahore"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code)