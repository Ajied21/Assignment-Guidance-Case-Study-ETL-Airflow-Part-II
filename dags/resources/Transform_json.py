import os
import json
from .Extract_json import extract_json

def get_json(n):
    # Mengambil daftar pengguna melalui fungsi extract_json
    result = extract_json(n)
    data_json = []  # Menyimpan hasil transformasi data

    if result:
        for dataset_json in result:
            # Mengubah data JSON menjadi format yang sesuai
            transform_data = {
                "id_user": dataset_json['login']['uuid'],
                "nama_user": dataset_json['login']['username'],
                "kata_sandi_user": dataset_json['login']['password'],
                "nama": f"{dataset_json['name']['first']} {dataset_json['name']['last']}",
                "jenis_kelamin": dataset_json['gender'],
                "umur": dataset_json['dob']['age'],
                "nomor_jalan": dataset_json['location']['street']['number'],
                "jalan": dataset_json['location']['street']['name'],
                "kecamatan": dataset_json['location']['state'],
                "kota": dataset_json['location']['city'],
                "negara": dataset_json['location']['country'],
                "kode_pos": dataset_json['location']['postcode'],
                "email": dataset_json['email'],
                "nomor_handphone": dataset_json['phone'],
                "nomor_telepon": dataset_json['cell'],
                "url_photo": dataset_json['picture']['large']
            }
            data_json.append(transform_data)  # Menambahkan hasil transformasi ke dalam list
        return data_json
    return None


def transfrom_to_json(file_name, n):
    # Tentukan direktori penyimpanan file JSON
    folder_path = './data/json'
    os.makedirs(folder_path, exist_ok=True)  # Membuat folder jika belum ada

    # Ambil data JSON yang telah diproses
    data_json = get_json(n)

    # Simpan data JSON ke dalam file
    file_path = os.path.join(folder_path, f'{file_name}.json')  # Tentukan path untuk file JSON
    with open(file_path, 'w') as json_file:
        json.dump(data_json, json_file, indent=4)  # Simpan data JSON dengan indentasi 4 spasi
    print(f"Data tersimpan ke {file_path}")  # Informasi lokasi file JSON tersimpan
    print(f"Data berhasil ke transform:\n{data_json}")  # Menampilkan data yang telah diproses

if __name__ == '__main__':

    transfrom_to_json()
