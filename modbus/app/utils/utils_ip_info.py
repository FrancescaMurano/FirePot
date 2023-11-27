import requests

def get_ip_info(ip_address):
    
    url = f"https://freeipapi.com/api/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    return data