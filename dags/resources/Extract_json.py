import requests
import io
import json

def extract_json(n):
    # Melakukan permintaan HTTP GET ke API randomuser dengan parameter format JSON dan jumlah hasil yang diminta
    response = requests.get(f"https://randomuser.me/api/?format=json&results={n}")
    # Mengonversi respons JSON menjadi dictionary Python
    formats = response.json()
    # Mengambil data pada kunci "results" dari dictionary yang dihasilkan
    data_json = formats["results"]
    # Menampilkan data yang berhasil diekstrak
    print(f"Data berhasil ke extract:\n{data_json}")
    
    return data_json

if __name__ == '__main__':
    
    extract_json()
