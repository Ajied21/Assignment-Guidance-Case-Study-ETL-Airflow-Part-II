import requests
import csv
import io

def extract_csv(n):
    response = requests.get(f"https://randomuser.me/api/?format=csv&results={n}")
    csv_data = io.StringIO(response.text)
    reader = csv.DictReader(csv_data)
    data_csv = [row for row in reader]
    print(f"Data berhasil ke extract:\n{data_csv}")
    return data_csv

if __name__ == '__main__':
    
    extract_csv()