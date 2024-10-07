import requests
import io
import json

def extract_json(n):
    response = requests.get(f"https://randomuser.me/api/?format=json&results={n}")
    formats = response.json()
    data_json = formats["results"]
    print(f"Data berhasil ke extract:\n{data_json}")
    return data_json

if __name__ == '__main__':
    
    extract_json()