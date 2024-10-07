import requests
import io
import xml.etree.ElementTree as ET

def extract_xml(n):
    response = requests.get(f"https://randomuser.me/api/?format=xml&results={n}")
    root = ET.fromstring(response.content)
    data_xml= ET.tostring(root, encoding='unicode', method='xml')
    print(f"Data berhasil ke extract:\n{data_xml}")
    return data_xml

if __name__ == '__main__':
    
    extract_xml()