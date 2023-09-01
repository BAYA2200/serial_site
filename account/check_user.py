import requests

url = "http://127.0.0.1:8000/api/account/login/"  # Замените на вашу конечную точку

data = {
    "email": "aurum2116@gamil.com.com",
    "password": "aurum2116"
}

response = requests.post(url, data=data)

print(response.json())