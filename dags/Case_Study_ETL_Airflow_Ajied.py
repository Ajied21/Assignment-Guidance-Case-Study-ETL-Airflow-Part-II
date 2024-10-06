from airflow.models.param import Param
from airflow.decorators import dag, task, branch_task
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from resources.Extract_csv import extract_csv
from resources.Extract_json import extract_json
from resources.Extract_xml import extract_xml
from resources.Transform_csv import transfrom_to_csv 
from resources.Transform_json import transfrom_to_json
from resources.Transform_xml import transfrom_to_xml
from resources.save_to_parquet import transfrom_to_parquet
from resources.Load_data import load_data_to_sqlite

# Fungsi DAG utama
@dag(
    description="Assignment Guidance: Case Study ETL Airflow",
    default_args={
        "owner": "Ajied(WhatsApp), Ajied(Email), dibimbing",
    },
    owner_links={
        "Ajied(WhatsApp)": "https://wa.me/+6287787106077",
        "Ajied(Email)": "mailto:dhoifullah.luthmajied05@gmail.com",
        "dibimbing": "https://dibimbing.id/",
    },
    params={
        "Table_Name": Param("", type="string", description="silakan masukan nama tabel dan bila ingin di spasi tambahkan ( _ atau - )"),
        "Extension": Param("", type="string", description="silakan sesuaikan format file pada url ya dan tulis huruf kecil semua, \
        adapun format yang disarankan (csv, json, xml)"),
        "Row_Count": Param(10, type="integer", description="Masukkan jumlah baris data yang ingin diambil (default: 100)"),
    }
)
def etl_branch_dag():

    @branch_task
    def extract_data(extension):
        # Menentukan jalur extract berdasarkan extension
        if extension == "csv":
            return "extract_from_csv"
        elif extension == "json":
            return "extract_from_json"
        elif extension == "xml":
            return "extract_from_xml"
        else:
            raise ValueError("Kesalahan format data")

    @task
    def extract_from_csv(row_count):
        return extract_csv(row_count)

    @task
    def extract_from_json(row_count):
        return extract_json(row_count)

    @task
    def extract_from_xml(row_count):
        return extract_xml(row_count)

    @task(trigger_rule=TriggerRule.ONE_SUCCESS)
    def transform_from_csv(table_name, row_count):
        return transfrom_to_csv(table_name, row_count)

    @task(trigger_rule=TriggerRule.ONE_SUCCESS)
    def transform_from_json(table_name, row_count):
        return transfrom_to_json(table_name, row_count)

    @task(trigger_rule=TriggerRule.ONE_SUCCESS)
    def transform_from_xml(table_name, row_count):
        return transfrom_to_xml(table_name, row_count)

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def save_to_parquet(extension, table_name, row_count):
        # Transformasi data menjadi format parquet
        return transfrom_to_parquet(extension, table_name, row_count)

    @task
    def load_data(table_name, extension, row_count):
        # Load data ke SQLite
        return load_data_to_sqlite(table_name, extension, row_count)

    # Mendefinisikan alur DAG
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")

    # Extract data berdasarkan parameter 'Extension' dan 'Row Count'
    extract_choice = extract_data('{{ params.Extension }}')

    # Tugas extract per format
    csv_task = extract_from_csv('{{ params.Row_Count }}')
    json_task = extract_from_json('{{ params.Row_Count }}')
    xml_task = extract_from_xml('{{ params.Row_Count }}')

    transform_csv = transform_from_csv('{{ params.Table_Name }}', '{{ params.Row_Count }}')
    transform_json = transform_from_json('{{ params.Table_Name }}', '{{ params.Row_Count }}')
    transform_xml = transform_from_xml('{{ params.Table_Name }}', '{{ params.Row_Count }}')

    # Proses Parquet berdasarkan extension yang dipilih
    save_task_parquet = save_to_parquet('{{ params.Extension }}', '{{ params.Table_Name }}', '{{ params.Row_Count }}')

    # Load data setelah transformasi
    load = load_data('{{ params.Table_Name }}', '{{ params.Extension }}', '{{ params.Row_Count }}')

    # Alur DAG
    start_task >> extract_choice

    # Menghubungkan task extract ke transform task
    extract_choice >> csv_task >> transform_csv
    extract_choice >> json_task >> transform_json
    extract_choice >> xml_task >> transform_xml

    # Menghubungkan transform task ke save task dan load task
    [transform_csv, transform_json, transform_xml] >> save_task_parquet >> load >> end_task

# Menjalankan DAG
etl_branch_dag()
