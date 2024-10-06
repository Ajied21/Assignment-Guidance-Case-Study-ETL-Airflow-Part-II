import os
import pandas as pd
import xml.etree.ElementTree as ET
from .Transform_json import get_json
from .Transform_csv import get_csv
from .Transform_xml import get_xml

def save_parquet_for_format(data_df, file_name):
    # Ubah tipe data kolom yang diperlukan
    data_df['kode_pos'] = data_df['kode_pos'].astype(str)
    file_path = f'./data/parquet/{file_name}.parquet'
    data_df.to_parquet(file_path, index=False)
    print(f"Data parquet tersimpan ke {file_path}")

# Fungsi untuk menyimpan data ke format parquet sesuai format
def transfrom_to_parquet(url, file_name, n):
    folder_path = './data/parquet'
    os.makedirs(folder_path, exist_ok=True)

    if url == "json":
        data = get_json(n)
        df_json = pd.DataFrame(data)
        save_parquet_for_format(df_json, file_name)
    elif url == "csv":
        data = get_csv(n)
        save_parquet_for_format(data, file_name)
    elif url == "xml":
        data_xml = get_xml(n)
        # Konversi data XML ke list of dict dan kemudian ke DataFrame
        user_data_list = []
        root = ET.fromstring(data_xml)
        for user in root.findall('user'):
            user_data = {child.tag: child.text for child in user}
            user_data_list.append(user_data)
        df_xml = pd.DataFrame(user_data_list)
        save_parquet_for_format(df_xml, file_name)

if __name__ == '__main__':
    
    transfrom_to_parquet()