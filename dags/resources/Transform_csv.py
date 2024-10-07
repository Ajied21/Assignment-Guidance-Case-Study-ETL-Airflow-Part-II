import os
import pandas as pd
from .Extract_csv import extract_csv

# Fungsi untuk mengambil data CSV
def get_csv(n):
    users = extract_csv(n)  # Mengambil pengguna menggunakan fungsi extract
    df = pd.DataFrame(users)

    extracted_data = {
        "id_user": [],
        "nama_user": [],
        "kata_sandi_user": [],
        "nama": [],
        "jenis_kelamin": [],
        "umur": [],
        "nomor_jalan": [],
        "jalan": [],
        "kecamatan": [],
        "kota": [],
        "negara": [],
        "kode_pos": [],
        "email": [],
        "nomor_handphone": [],
        "nomor_telepon": [],
        "url_photo": []
    }

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

    data_csv = pd.DataFrame(extracted_data)

    return data_csv

def transfrom_to_csv(file_name, n):
    folder_path = './dags/data/csv'
    os.makedirs(folder_path, exist_ok=True)

    # Ambil data CSV
    data_csv = get_csv(n)

    # Simpan ke file CSV
    file_path = os.path.join(folder_path, f'{file_name}.csv')
    data_csv.to_csv(file_path, index=False)
    print(f"Data tersimpan ke {file_path}")
    print(f"Data berhasil ke transform:\n{data_csv}")

if __name__ == '__main__':
    
    transfrom_to_csv()
