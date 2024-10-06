import os
import json
from .Extract_json import extract_json

# Fungsi untuk mengambil data JSON
def get_json(n):
    result = extract_json(n)  # Mengambil daftar pengguna
    data_json = []
    if result:
        for dataset_json in result:
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
            data_json.append(transform_data)
        return data_json
    return None

def transfrom_to_json(file_name, n):
    folder_path = './data/json'
    os.makedirs(folder_path, exist_ok=True)

    # Ambil data JSON
    data_json = get_json(n)

    # Simpan ke file JSON
    file_path = os.path.join(folder_path, f'{file_name}.json')
    with open(file_path, 'w') as json_file:
        json.dump(data_json, json_file, indent=4)
    print(f"Data tersimpan ke {file_path}")

if __name__ == '__main__':
    
    transfrom_to_json()