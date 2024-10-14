from airflow.decorators import dag, task, branch_task
from airflow.operators.empty import EmptyOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.context import Context
from airflow.utils.email import send_email
from airflow.exceptions import AirflowFailException
from datetime import datetime

# Membaca skema tabel PostgreSQL dari file SQL
with open("./dags/Client_DB/schema_table_PostgreSQL.sql", "r") as postgres:
    schema_table_postgres = postgres.read()

# Fungsi untuk mengirim email ketika ada kegagalan pada proses DAG
def send_email_on_failure(context: Context):
    send_email(
        to           = ["dhoifullah.luthmajied05@gmail.com"], # Masukkan email penerima
        subject      = "Airflow Failed!",
        html_content = f"""
            <center><h1>!!! DAG RUN FAILED !!!</h1></center>
            <b>Dag</b>    : <i>{ context['ti'].dag_id }</i><br>
            <b>Task</b>   : <i>{ context['ti'].task_id }</i><br>
            <b>Log URL</b>: <i>{ context['ti'].log_url }</i><br>
        """
    )

# Dekorator DAG untuk mendefinisikan pengaturan DAG
@dag(
    description="Dhoifullah Luth Majied",
    schedule_interval="15 9-21/2 * * 5", # Menjadwalkan DAG untuk dijalankan setiap 2 jam sekali pada hari Jumat di minggu pertama dan ketiga, dari jam 9 pagi hingga 9 malam
    start_date=datetime(2024, 10, 1),
    catchup=False,
    default_args={
        "owner": "Ajied(WhatsApp), Ajied(Email), dibimbing",
        "on_failure_callback": send_email_on_failure, # Memanggil fungsi pengiriman email ketika ada task yang gagal
    },
    owner_links={
        "Ajied(WhatsApp)": "https://wa.me/+6287787106077", # Link kontak WhatsApp
        "Ajied(Email)": "mailto:dhoifullah.luthmajied05@gmail.com", # Link kontak email
        "dibimbing": "https://dibimbing.id/", # Link website terkait
    },
    tags=[
        "ETL_with_MySQL_&_PostgreSQL_Ajied", # Tag untuk mengkategorikan DAG
    ]
)

# Fungsi DAG untuk melakukan extract data dari MySQL dan load ke PostgreSQL
def extract_in_mysql_load_to_postgres():

    # Task untuk memeriksa koneksi ke PostgreSQL
    @branch_task
    def check_connection_postgres():
        postgres_hook = PostgresHook(postgres_conn_id='id_postgres')
        
        try:
            connection = postgres_hook.get_conn()
            connection.cursor()  # Memastikan koneksi terbuka dengan membuka cursor
            print("Koneksi ke PostgreSQL berhasil!")
            return "success_connection_to_postgres"  # Mengembalikan task_id jika berhasil
        except Exception as error:
            print(f"Koneksi ke PostgreSQL gagal: {str(error)}")
            return "failed_connection_to_postgres"  # Mengembalikan task_id jika gagal
        finally:
            if 'connection' in locals():
                connection.close()  # Menutup koneksi jika terbuka

    # Task yang dieksekusi ketika koneksi ke PostgreSQL berhasil
    @task
    def success_connection_to_postgres():
        print("Koneksi ke PostgreSQL sukses. Melanjutkan ke langkah berikutnya.")

    # Task yang dieksekusi ketika koneksi ke PostgreSQL gagal
    @task
    def failed_connection_to_postgres():
        raise AirflowFailException("Task gagal: Koneksi ke PostgreSQL gagal. Proses dihentikan.")

    # Task untuk membuat skema tabel di PostgreSQL sesuai file SQL
    @task
    def create_postgres_schema():
        postgres_hook = PostgresHook(postgres_conn_id='id_postgres')

        create_schema_queries = schema_table_postgres.split(";")  # Memecah skema menjadi perintah SQL
        for query in create_schema_queries:
            if query.strip():  # Menjalankan query jika tidak kosong
                postgres_hook.run(query)

    # Task untuk mengekstrak data dari MySQL
    @task
    def extract_data_from_mysql():
        mysql_hook = MySqlHook(mysql_conn_id='id_mysql')
        connection = mysql_hook.get_conn()
        cursor = connection.cursor()

        cursor.execute("USE project_dibimbing;")  # Menggunakan database yang diinginkan
        cursor.execute("SHOW TABLES;")  # Mendapatkan daftar tabel
        tables = cursor.fetchall()

        data = {}
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name};")  # Menarik data dari setiap tabel
            records = cursor.fetchall()

            column_names = [i[0] for i in cursor.description]  # Mendapatkan nama kolom
            data[table_name] = {"columns": column_names, "records": records}

        cursor.close()
        return data  # Mengembalikan data yang diekstrak dalam format dictionary

    # Task untuk memuat data yang sudah diekstrak ke PostgreSQL
    @task
    def load_data_to_postgresql(extracted_data):
        postgres_hook = PostgresHook(postgres_conn_id='id_postgres')

        # Urutan pemuatan tabel yang memiliki dependensi foreign key
        load_order = [
            "customer_information",
            "payments",
            "employees",
            "room_class",
            "room_information",
            "reservation",
            "transactions",
            "reports"
        ]

        # Definisikan unique key untuk setiap tabel
        unique_keys = {
            "customer_information": "cust_ID",
            "payments": "payment_ID",
            "employees": "employee_ID",
            "room_class": "class_ID",
            "room_information": "room_ID",
            "reservation": "reservation_ID",
            "transactions": "transaction_ID",
            "reports": "report_ID"
        }

        # Proses memuat data ke dalam PostgreSQL sesuai urutan tabel
        for table_name in load_order:
            if table_name in extracted_data:
                table_data = extracted_data[table_name]
                placeholders = ", ".join(["%s"] * len(table_data["columns"]))  # Membuat string placeholder untuk query SQL
                column_names = ", ".join(table_data["columns"])  # Menggabungkan nama kolom
                insert_query = f"INSERT INTO project_dibimbing.{table_name} ({column_names}) VALUES ({placeholders})"
                
                unique_key = unique_keys.get(table_name, None)
                if unique_key is None:
                    raise ValueError(f"Tabel {table_name} tidak memiliki unique key yang didefinisikan.")  # Validasi kunci unik

                # Proses pengecekan dan pemuatan data
                for record in table_data["records"]:
                    select_query = f"SELECT COUNT(*) FROM project_dibimbing.{table_name} WHERE {unique_key} = %s"
                    existing_records = postgres_hook.get_first(select_query, parameters=(record[table_data["columns"].index(unique_key)],))

                    if existing_records[0] == 0:  # Memuat data jika belum ada di PostgreSQL
                        postgres_hook.run(insert_query, parameters=record)
                        print(f"Data baru dimuat ke {table_name}: {record}")
                    else:
                        print(f"Data sudah ada di {table_name}, melewati data: {record}")

    # Task dan alur eksekusi DAG
    start_task = EmptyOperator(task_id="start_task")
    process_completed = EmptyOperator(task_id="process_completed", trigger_rule=TriggerRule.ALL_DONE)
    end_task = EmptyOperator(task_id="end_task")

    PostgreSQL_check = check_connection_postgres()
    create_schema = create_postgres_schema()
    extracted_data = extract_data_from_mysql()
    loaded_data = load_data_to_postgresql(extracted_data)

    # Menyusun alur eksekusi task dalam DAG
    start_task >> PostgreSQL_check
    PostgreSQL_check >> failed_connection_to_postgres() >> process_completed >> end_task
    PostgreSQL_check >> success_connection_to_postgres() >> create_schema >> extracted_data >> loaded_data >> process_completed >> end_task

extract_in_mysql_load_to_postgres()
