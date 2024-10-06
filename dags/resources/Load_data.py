# load.py
from sqlalchemy import create_engine, Table, MetaData
import pandas as pd
import xml.etree.ElementTree as ET
from .Transform_data import get_json, get_csv, get_xml

def load_data_to_sqlite(file_name, url, n):
    # Create a SQLite engine
    engine = create_engine('sqlite:///database_airflow.db')

    # Load the parquet file into a Pandas DataFrame
    if url == "json":
        data = get_json(n)
        df = pd.DataFrame(data)
    elif url == "csv":
        data = get_csv(n)
        df = data
    elif url == "xml":
        data_xml = get_xml(n)
        user_data_list = []
        root = ET.fromstring(data_xml)
        for user in root.findall('user'):
            user_data = {child.tag: child.text for child in user}
            user_data_list.append(user_data)
        df = pd.DataFrame(user_data_list)

    # Load the DataFrame into a SQLite table
    df.to_sql(file_name, con=engine, if_exists='replace', index=False)

    print(f"Data loaded into SQLite table {file_name}")

if __name__ == "__main__":

    load_data_to_sqlite()