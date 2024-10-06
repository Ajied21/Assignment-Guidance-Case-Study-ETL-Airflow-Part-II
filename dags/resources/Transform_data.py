import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from .Extract_data import extract_csv, extract_json, extract_xml

# Fungsi untuk mengambil data JSON
def get_json(n):
    result = extract_json(n)  # Mengambil daftar pengguna
    data_json = []
    if result:  # Memeriksa apakah ada pengguna yang diambil
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

# Fungsi untuk mengambil data XML
def get_xml(n):
    results = extract_xml(n)

    root = ET.fromstring(results)

    user_data_list = []
    for user in root.findall('.//results'):
        user_data = {
            "id_user": user.find('login/uuid').text if user.find('login/uuid') is not None else None,
            "nama_user": user.find('login/username').text if user.find('login/username') is not None else None,
            "kata_sandi_user": user.find('login/password').text if user.find('login/password') is not None else None,
            "nama": f"{user.find('name/first').text if user.find('name/first') is not None else ''} " \
                    f"{user.find('name/last').text if user.find('name/last') is not None else ''}".strip(),
            "jenis_kelamin": user.find('gender').text if user.find('gender') is not None else None,
            "umur": user.find('dob/age').text if user.find('dob/age') is not None else None,
            "nomor_jalan": user.find('location/street/number').text if user.find('location/street/number') is not None else None,
            "nama_jalan": user.find('location/street/name').text if user.find('location/street/name') is not None else None,
            "kecamatan": user.find('location/state').text if user.find('location/state') is not None else None,
            "kota": user.find('location/city').text if user.find('location/city') is not None else None,
            "negara": user.find('location/country').text if user.find('location/country') is not None else None,
            "kode_pos": user.find('location/postcode').text if user.find('location/postcode') is not None else None,
            "email": user.find('email').text if user.find('email') is not None else None,
            "nomor_handphone": user.find('phone').text if user.find('phone') is not None else None,
            "nomor_telepon": user.find('cell').text if user.find('cell') is not None else None,
            "url_photo": user.find('picture/large').text if user.find('picture/large') is not None else None
        }

        if user_data["id_user"] is not None:
            user_data_list.append(user_data)
    
    if not user_data_list:
        return '<users></users>'

    root_element = ET.Element("results")
    for user_data in user_data_list:
        user_element = ET.SubElement(root_element, "user")
        for key, value in user_data.items():
            ET.SubElement(user_element, key).text = str(value) if value is not None else ''

    data_xml = ET.tostring(root_element, encoding='unicode')

    return data_xml

# Fungsi untuk menyimpan data ke dalam format CSV
def transfrom_to_csv(file_name,n):
    folder_path = './data/csv'
    os.makedirs(folder_path, exist_ok=True)  # Buat folder jika belum ada
    
    # Ambil data CSV
    data_csv = get_csv(n)
    
    # Simpan ke file CSV
    file_path = os.path.join(folder_path, f'{file_name}.csv')
    data_csv.to_csv(file_path, index=False)
    print(f"Data tersimpan ke {file_path}")

# Fungsi untuk menyimpan data ke dalam format JSON
def transfrom_to_json(file_name,n):
    folder_path = './data/json'
    os.makedirs(folder_path, exist_ok=True)
    
    # Ambil data JSON
    data_json = get_json(n)
    
    # Simpan ke file JSON
    file_path = os.path.join(folder_path, f'{file_name}.json')
    with open(file_path, 'w') as json_file:
        json.dump(data_json, json_file, indent=4)
    print(f"Data tersimpan ke {file_path}")

# Fungsi untuk menyimpan data ke dalam format XML
def transfrom_to_xml(file_name,n):
    folder_path = './data/xml'
    os.makedirs(folder_path, exist_ok=True)
    
    # Ambil data XML
    data_xml = get_xml(n)
    
    # Simpan ke file XML
    file_path = os.path.join(folder_path, f'{file_name}.xml')
    with open(file_path, 'w') as xml_file:
        xml_file.write(data_xml)
    print(f"Data tersimpan ke {file_path}")

def save_parquet_for_format(data_df, file_name):
    # Ubah tipe data kolom yang diperlukan
    data_df['kode_pos'] = data_df['kode_pos'].astype(str)
    file_path = f'./data/parquet/{file_name}.parquet'
    data_df.to_parquet(file_path, index=False)

# Fungsi untuk menyimpan data ke format parquet sesuai format
def transfrom_to_parquet(url, file_name, n):
    if url == "json":
        data = get_json(n)
        df_json = pd.DataFrame(data)
        save_parquet_for_format(df_json, file_name)  # Gunakan file_name
    elif url == "csv":
        data = get_csv(n)
        save_parquet_for_format(data, file_name)  # Gunakan file_name
    elif url == "xml":
        data_xml = get_xml(n)
        # Konversi data XML ke list of dict dan kemudian ke DataFrame
        user_data_list = []
        root = ET.fromstring(data_xml)
        for user in root.findall('user'):
            user_data = {child.tag: child.text for child in user}
            user_data_list.append(user_data)
        df_xml = pd.DataFrame(user_data_list)
        save_parquet_for_format(df_xml, file_name)  # Gunakan file_name

if __name__ == "__main__":

    print("Pilih format data:")
    print("- json")
    print("- csv")
    print("- xml")

    url = input("Masukkan format data: ")
    file_name = input("Masukan nama tabel: ")
    n = int(input("Masukan berapa rows data: "))

    if url == "json":
        transfrom_to_json(file_name, n)
        transfrom_to_parquet("json", file_name, n)  # Tambahkan file_name
    elif url == "csv":
        transfrom_to_csv(file_name, n)
        transfrom_to_parquet("csv", file_name, n)  # Tambahkan file_name
    elif url == "xml":
        transfrom_to_xml(file_name, n)
        transfrom_to_parquet("xml", file_name, n)  # Tambahkan file_name
    else:
        print("Format tidak diketahui.")