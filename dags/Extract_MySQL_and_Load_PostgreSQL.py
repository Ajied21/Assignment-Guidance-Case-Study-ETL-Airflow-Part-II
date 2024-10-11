from airflow.decorators import dag, task, branch_task
from airflow.operators.empty import EmptyOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.context import Context
from airflow.utils.email import send_email
from airflow.exceptions import AirflowFailException
from datetime import datetime

# Membaca skema tabel dari file SQL
with open("./dags/Client_DB/schema_table_PostgreSQL.sql", "r") as postgres:
    schema_table_postgres = postgres.read()

def send_email_on_failure(context: Context):
    send_email(
        to           = ["dhoifullah.luthmajied05@gmail.com"], #silakan masukan email anda
        subject      = "Airflow Failed!",
        html_content = f"""
            <center><h1>!!! DAG RUN FAILED !!!</h1></center>
            <b>Dag</b>    : <i>{ context['ti'].dag_id }</i><br>
            <b>Task</b>   : <i>{ context['ti'].task_id }</i><br>
            <b>Log URL</b>: <i>{ context['ti'].log_url }</i><br>
        """
    )

@dag(
    description="Dhoifullah Luth Majied",
    schedule_interval="15 9-21/2 * * 5", #DAG yang dijalankan setiap 2 jam sekali dari jam 9 pagi sampai 9 malam di Jumat minggu pertama dan ketiga
    start_date=datetime(2024, 10, 1),
    catchup=False,
    default_args={
        "owner": "Ajied(WhatsApp), Ajied(Email), dibimbing",
        "on_failure_callback": send_email_on_failure,
    },
    owner_links={
        "Ajied(WhatsApp)": "https://wa.me/+6287787106077",
        "Ajied(Email)": "mailto:dhoifullah.luthmajied05@gmail.com",
        "dibimbing": "https://dibimbing.id/",
    },
    tags=[
        "ETL_with_MySQL_&_PostgreSQL_Ajied",
    ]
)

def extract_in_mysql_load_to_postgres():

    @branch_task
    def check_connection_postgres():
        postgres_hook = PostgresHook(postgres_conn_id='id_postgres')
        
        try:
            connection = postgres_hook.get_conn()
            connection.cursor()  # Mencoba membuka cursor untuk memeriksa koneksi
            print("Koneksi ke PostgreSQL berhasil!")
            return "success_connection_to_postgres"  # Mengembalikan task_id jika berhasil
        except Exception as error:
            print(f"Koneksi ke PostgreSQL gagal: {str(error)}")
            return "failed_connection_to_postgres"  # Mengembalikan task_id jika gagal
        finally:
            if 'connection' in locals():
                connection.close()

    @task
    def success_connection_to_postgres():
        print("Melanjutkan ke langkah berikutnya setelah sukses koneksi ke PostgreSQL.")

    @task
    def failed_connection_to_postgres():
        raise AirflowFailException("ini task yang gagal & Koneksi ke PostgreSQL gagal. Proses dihentikan.")

    @task
    def create_postgres_schema():
        postgres_hook = PostgresHook(postgres_conn_id='id_postgres')

        create_schema_queries = schema_table_postgres.split(";")
        for query in create_schema_queries:
            if query.strip():  # Pastikan query tidak kosong
                postgres_hook.run(query)

    @task
    def extract_data_from_mysql():
        mysql_hook = MySqlHook(mysql_conn_id='id_mysql')
        connection = mysql_hook.get_conn()
        cursor = connection.cursor()

        cursor.execute("USE project_dibimbing;")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        data = {}
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name};")
            records = cursor.fetchall()

            column_names = [i[0] for i in cursor.description]
            data[table_name] = {"columns": column_names, "records": records}

        cursor.close()
        return data

    @task
    def load_data_to_postgresql(extracted_data):
        postgres_hook = PostgresHook(postgres_conn_id='id_postgres')

        # Pemuatan data dengan urutan yang benar & Mengurutkan tabel agar foreign key tidak melanggar
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

        for table_name in load_order:
            if table_name in extracted_data:
                table_data = extracted_data[table_name]
                placeholders = ", ".join(["%s"] * len(table_data["columns"]))
                column_names = ", ".join(table_data["columns"])
                insert_query = f"INSERT INTO project_dibimbing.{table_name} ({column_names}) VALUES ({placeholders});"

                for record in table_data["records"]:
                    postgres_hook.run(insert_query, parameters=record)
    

    start_task = EmptyOperator(task_id="start_task")
    process_completed = EmptyOperator(task_id="process_completed", trigger_rule=TriggerRule.ALL_DONE)
    end_task = EmptyOperator(task_id="end_task")

    PostgreSQL_check = check_connection_postgres()
    create_schema = create_postgres_schema()
    extracted_data = extract_data_from_mysql()
    loaded_data = load_data_to_postgresql(extracted_data)

    start_task >> PostgreSQL_check
    PostgreSQL_check >> failed_connection_to_postgres() >> process_completed >> end_task
    PostgreSQL_check >> success_connection_to_postgres() >> create_schema >> extracted_data >> loaded_data >> process_completed >> end_task

extract_in_mysql_load_to_postgres()