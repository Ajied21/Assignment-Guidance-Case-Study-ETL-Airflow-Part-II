# load.py
import os
import pandas as pd
from sqlalchemy import create_engine

def get_latest_parquet_file(folder_path):
    # Cek apakah folder_path ada dan berisi file
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder {folder_path} tidak ditemukan")

    # Dapatkan semua file .parquet di folder
    parquet_files = [f for f in os.listdir(folder_path) if f.endswith('.parquet')]

    if not parquet_files:
        print("Tidak ada file parquet ditemukan di folder.")
        return None  # Mengembalikan None jika tidak ada file ditemukan

    # Urutkan file berdasarkan waktu modifikasi (terbaru di urutan terakhir)
    parquet_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=True)

    # Kembalikan file terbaru
    latest_file = parquet_files[0]
    return os.path.join(folder_path, latest_file)

def load_data_from_latest_parquet():
    # Tentukan path folder untuk file parquet
    folder_path = './data/parquet'
    
    # Dapatkan file parquet terbaru
    latest_file = get_latest_parquet_file(folder_path)
    
    if latest_file:
        print(f"File parquet terbaru ditemukan: {latest_file}")
        # Load parquet file ke dalam Pandas DataFrame
        df = pd.read_parquet(latest_file)
        # Return DataFrame dan nama file
        return df, latest_file
    else:
        # Jika tidak ada file ditemukan, return None
        print("Proses dihentikan: Tidak ada file parquet yang ditemukan.")
        return None, None

def load_data_to_sqlite():
    # Tentukan path untuk menyimpan SQLite database di folder 'plugins'
    plugins_folder = './plugins'
    os.makedirs(plugins_folder, exist_ok=True)  # Buat folder jika belum ada
    db_path = os.path.join(plugins_folder, 'database_airflow.db')

    # Create a SQLite engine dengan path ke folder 'plugins'
    engine = create_engine(f'sqlite:///{db_path}')

    # Load data dari file parquet terbaru dan ambil juga nama file-nya
    df, latest_file = load_data_from_latest_parquet()

    if df is not None and latest_file is not None:
        # Nama tabel diambil dari nama file tanpa ekstensi
        file_name = os.path.basename(latest_file).replace('.parquet', '')

        # Load the DataFrame into a SQLite table
        df.to_sql(file_name, con=engine, if_exists='replace', index=False)

        print(f"Data loaded into SQLite table dengan nama: {file_name}")
        print(f"Database SQLite disimpan di: {db_path}")
    else:
        print("Tidak ada data yang di-load ke SQLite karena file parquet tidak ditemukan.")

if __name__ == "__main__":
    # Load data dari parquet terbaru dan masukkan ke SQLite
    load_data_to_sqlite()
