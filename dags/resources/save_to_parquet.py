import os
import pandas as pd
import xml.etree.ElementTree as ET
from .Transform_json import get_json
from .Transform_csv import get_csv
from .Transform_xml import get_xml

def save_parquet_for_format(data_df, file_name):
    # Ubah tipe data kolom 'kode_pos' menjadi string
    data_df['kode_pos'] = data_df['kode_pos'].astype(str)
    
    # Tentukan path untuk file parquet
    file_path = f'./data/parquet/{file_name}.parquet'
    
    # Simpan DataFrame ke file parquet
    data_df.to_parquet(file_path, index=False)
    print(f"Data parquet tersimpan ke {file_path}")


def transfrom_to_parquet(url, file_name, n):
    folder_path = './data/parquet'
    
    # Buat folder jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    # Proses sesuai format (JSON, CSV, atau XML)
    if url == "json":
        data = get_json(n)  # Ambil data JSON
        df_json = pd.DataFrame(data)  # Ubah data ke DataFrame
        save_parquet_for_format(df_json, file_name)  # Simpan DataFrame ke format parquet
        print(f"Dataframe untuk di save ke parquet:\n{df_json}")
    elif url == "csv":
        df_csv = get_csv(n)  # Ambil data CSV dan ubah langsung ke DataFrame
        save_parquet_for_format(df_csv, file_name)  # Simpan DataFrame ke format parquet
        print(f"Dataframe untuk di save ke parquet:\n{df_csv}")
    elif url == "xml":
        data_xml = get_xml(n)
        # Konversi data XML ke list of dict dan kemudian ke DataFrame
        user_data_list = []
        root = ET.fromstring(data_xml)  # Parse XML menjadi root element
        for user in root.findall('user'):  # Iterasi tiap elemen 'user'
            user_data = {child.tag: child.text for child in user}  # Ambil data untuk setiap user
            user_data_list.append(user_data)
        
        # Ubah list of dict ke DataFrame
        df_xml = pd.DataFrame(user_data_list)
        save_parquet_for_format(df_xml, file_name)  # Simpan DataFrame ke format parquet
        print(f"Dataframe untuk di save ke parquet:\n{df_xml}")

if __name__ == '__main__':

    transfrom_to_parquet()
