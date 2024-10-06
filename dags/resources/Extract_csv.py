import requests
import csv
import pandas as pd
import io
import json
import xml.etree.ElementTree as ET
from tabulate import tabulate

def extract_csv(n):
    response = requests.get(f"https://randomuser.me/api/?format=csv&results={n}")
    csv_data = io.StringIO(response.text)
    reader = csv.DictReader(csv_data)
    data_csv = [row for row in reader]
    return data_csv

if __name__ == '__main__':
    
    extract_csv()