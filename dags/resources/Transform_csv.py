import os
import pandas as pd
from .Extract_csv import extract_csv

def get_csv(n):
    # Mengambil pengguna menggunakan fungsi extract_csv
    users = extract_csv(n)
    df = pd.DataFrame(users)

    # Struktur dictionary untuk menyimpan data yang diekstrak
    extracted_data = {
        "id_user": [],  # Menyimpan ID pengguna
        "nama_user": [],  # Menyimpan nama pengguna
        "kata_sandi_user": [],  # Menyimpan kata sandi pengguna
        "nama": [],  # Menyimpan nama lengkap pengguna
        "jenis_kelamin": [],  # Menyimpan jenis kelamin pengguna
        "umur": [],  # Menyimpan umur pengguna
        "nomor_jalan": [],  # Menyimpan nomor jalan alamat pengguna
        "jalan": [],  # Menyimpan nama jalan alamat pengguna
        "kecamatan": [],  # Menyimpan kecamatan pengguna
        "kota": [],  # Menyimpan kota pengguna
        "negara": [],  # Menyimpan negara pengguna
        "kode_pos": [],  # Menyimpan kode pos pengguna
        "email": [],  # Menyimpan email pengguna
        "nomor_handphone": [],  # Menyimpan nomor telepon pengguna
        "nomor_telepon": [],  # Menyimpan nomor ponsel pengguna
        "url_photo": []  # Menyimpan URL foto pengguna
    }

    # Mengisi dictionary dengan data dari hasil ekstraksi
    for result in users:
        extracted_data["id_user"].append(result["login.uuid"])
        extracted_data["nama_user"].append(result["login.username"])
        extracted_data["kata_sandi_user"].append(result["login.password"])
        extracted_data["nama"].append(f"{result['name.first']} {result['name.last']}")
        extracted_data["jenis_kelamin"].append(result["gender"])
        extracted_data["umur"].append(result["dob.age"])
        extracted_data["nomor_jalan"].append(result["location.street.number"])
        extracted_data["jalan"].append(result["location.street.name"])
        extracted_data["kecamatan"].append(result["location.state"])
        extracted_data["kota"].append(result["location.city"])
        extracted_data["negara"].append(result["location.country"])
        extracted_data["kode_pos"].append(result["location.postcode"])
        extracted_data["email"].append(result["email"])
        extracted_data["nomor_handphone"].append(result["phone"])
        extracted_data["nomor_telepon"].append(result["cell"])
        extracted_data["url_photo"].append(result["picture.large"])

    # Mengubah data yang diekstrak menjadi DataFrame
    data_csv = pd.DataFrame(extracted_data)

    return data_csv


def transfrom_to_csv(file_name, n):
    # Membuat folder tempat menyimpan file CSV
    folder_path = './data/csv'
    os.makedirs(folder_path, exist_ok=True)

    # Ambil data CSV yang telah diproses
    data_csv = get_csv(n)

    # Menyimpan data ke file CSV
    file_path = os.path.join(folder_path, f'{file_name}.csv')
    data_csv.to_csv(file_path, index=False)  # Simpan data CSV tanpa index
    print(f"Data tersimpan ke {file_path}")  # Informasi file CSV tersimpan
    print(f"Data berhasil ke transform:\n{data_csv}")  # Menampilkan data yang telah diproses

if __name__ == '__main__':

    transfrom_to_csv()
