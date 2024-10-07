import requests
import csv
import io

def extract_csv(n):
    # Melakukan permintaan HTTP GET ke API randomuser dengan parameter format CSV dan jumlah hasil yang diminta
    response = requests.get(f"https://randomuser.me/api/?format=csv&results={n}")
    # Mengonversi respons teks menjadi objek StringIO agar dapat dibaca sebagai file CSV
    csv_data = io.StringIO(response.text)
    # Membaca data CSV menggunakan DictReader, yang akan mengubah baris CSV menjadi dictionary
    reader = csv.DictReader(csv_data)
    # Menyimpan setiap baris data CSV ke dalam list
    data_csv = [row for row in reader]
    # Menampilkan data yang telah diekstrak
    print(f"Data berhasil ke extract:\n{data_csv}")

    return data_csv

if __name__ == '__main__':

    extract_csv()