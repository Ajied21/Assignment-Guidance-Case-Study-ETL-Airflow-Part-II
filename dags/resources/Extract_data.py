import requests
import csv
import pandas as pd
import io
import json
import xml.etree.ElementTree as ET
from tabulate import tabulate

def extract_json(n):
    response = requests.get(f"https://randomuser.me/api/?format=json&results={n}")
    formats = response.json()
    data_json = formats["results"]
    return data_json

def extract_csv(n):
    response = requests.get(f"https://randomuser.me/api/?format=csv&results={n}")
    csv_data = io.StringIO(response.text)
    reader = csv.DictReader(csv_data)
    data_csv = [row for row in reader]
    return data_csv

def extract_xml(n):
    response = requests.get(f"https://randomuser.me/api/?format=xml&results={n}")
    root = ET.fromstring(response.content)
    data_xml= ET.tostring(root, encoding='unicode', method='xml')
    return data_xml

