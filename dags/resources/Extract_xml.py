import requests
import io
import xml.etree.ElementTree as ET  # Mengimpor modul ElementTree untuk memproses data dalam format XML

def extract_xml(n):
    # Melakukan permintaan HTTP GET ke API randomuser dengan parameter format XML dan jumlah hasil yang diminta
    response = requests.get(f"https://randomuser.me/api/?format=xml&results={n}")
    # Mengonversi respons XML menjadi objek ElementTree
    root = ET.fromstring(response.content)
    # Mengonversi elemen root XML menjadi string untuk ditampilkan
    data_xml = ET.tostring(root, encoding='unicode', method='xml')
    # Menampilkan data XML yang berhasil diekstrak
    print(f"Data berhasil ke extract:\n{data_xml}")
    
    return data_xml

if __name__ == '__main__':

    extract_xml()
