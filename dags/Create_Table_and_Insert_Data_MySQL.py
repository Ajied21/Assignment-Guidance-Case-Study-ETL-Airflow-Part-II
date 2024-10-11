from airflow.decorators import dag, task, branch_task
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.utils.context import Context
from airflow.utils.email import send_email
from airflow.exceptions import AirflowFailException
from Client_DB.Data_Dummy import insert_data_dummy_to_MySQL


with open("./dags/Client_DB/schema_table_MySQL.sql", "r") as mysql:
    schema_table_mysql = mysql.read()

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

# Fungsi DAG utama
@dag(
    description="Dhoifullah Luth Majied",
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
    ],
)

def create_and_insert_MySQL():
    
    # Task untuk memeriksa koneksi MySQL
    @branch_task
    def check_connection_mysql():
        mysql_hook = MySqlHook(mysql_conn_id='id_mysql')
        
        try:
            connection = mysql_hook.get_conn()
            connection.cursor()  # Mencoba membuka cursor untuk memeriksa koneksi
            print("Koneksi ke MySQL berhasil!")
            return "success_connection_to_mysql"  # Mengembalikan task_id jika berhasil
        except Exception as error:
            print(f"Koneksi ke MySQL gagal: {str(error)}")  # Mencetak error jika gagal
            return "failed_connection_to_mysql"  # Mengembalikan task_id jika gagal
        finally:
            if 'connection' in locals():
                connection.close()

    # Task untuk menangani koneksi yang berhasil
    @task
    def success_connection_to_mysql():
        print("Melanjutkan ke langkah berikutnya setelah sukses koneksi ke MySQL.")

    # Task untuk menangani koneksi yang gagal
    @task
    def failed_connection_to_mysql():
        raise AirflowFailException("ini task yang gagal & Koneksi ke MySQL gagal. Proses dihentikan.")

    # Task untuk membuat tabel menggunakan MySqlHook
    @task
    def create_table_mysql():
        mysql_hook = MySqlHook(mysql_conn_id='id_mysql')
        connection = mysql_hook.get_conn()
        cursor = connection.cursor()

        # Memisahkan query berdasarkan titik koma (;)
        queries = schema_table_mysql.split(';')
        
        # Menjalankan setiap query satu per satu
        for run in queries:
            run = run.strip()  # Menghilangkan whitespace
            if run:
                cursor.execute(run)

        connection.commit()
        cursor.close()

    @task
    def insert_data_mysql():
        return insert_data_dummy_to_MySQL()
    
    # Mendefinisikan alur DAG
    start_task = EmptyOperator(task_id="start_task")
    process_completed = EmptyOperator(task_id="process_completed", trigger_rule=TriggerRule.ALL_DONE)
    end_task = EmptyOperator(task_id="end_task")

    MySQL = check_connection_mysql()

    # Alur DAGs
    start_task >> MySQL
    MySQL >>  failed_connection_to_mysql() >> process_completed >> end_task
    MySQL >> success_connection_to_mysql() >> create_table_mysql() >> insert_data_mysql() >> process_completed >> end_task

create_and_insert_MySQL()
