import requests
import csv
import pandas as pd
import io
import json
import xml.etree.ElementTree as ET
from tabulate import tabulate

def extract_xml(n):
    response = requests.get(f"https://randomuser.me/api/?format=xml&results={n}")
    root = ET.fromstring(response.content)
    data_xml= ET.tostring(root, encoding='unicode', method='xml')
    return data_xml

if __name__ == '__main__':
    
    extract_xml()