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

if __name__ == '__main__':
    
    extract_json()