from airflow.providers.mysql.hooks.mysql import MySqlHook
from faker import Faker
import random
from datetime import timedelta

# Inisialisasi Faker
fake = Faker()

# Fungsi untuk membuat data dummy customer_information
def insert_customer_information(cur, n):
    try:
        for _ in range(n):
            custfname = fake.first_name()
            custlname = fake.last_name()
            address = fake.address()
            status = random.choice(['Active', 'Inactive'])
            cur.execute("INSERT INTO customer_information (custfname, custlname, address, status) VALUES (%s, %s, %s, %s)",
                        (custfname, custlname, address, status))
            
        print("Data dummy untuk tabel customer_information berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel customer_information: {error}")

# Fungsi untuk membuat data dummy payments
def insert_payments(cur, n):
    try:
        cur.execute("SELECT cust_ID FROM customer_information")
        customer_ids = [row[0] for row in cur.fetchall()]
        for _ in range(n):
            customer_ID = random.choice(customer_ids)
            payment_date = fake.date_time_this_year()
            cur.execute("INSERT INTO payments (customer_ID, payment_date) VALUES (%s, %s)", (customer_ID, payment_date))

        print("Data dummy untuk tabel payments berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel payments: {error}")

# Fungsi untuk membuat data dummy employees
def insert_employees(cur, n):
    try:
        for _ in range(n):
            fname = fake.first_name()
            lname = fake.last_name()
            job_department = random.choice(['Hotel Manager', 'Hotel assistant manager','Marketing','Sales', 'Finance', 'HR', 'IT/Engineering', 
                                            'Housekeeping supervisor','Housekeeper', 'Maintenance','Chef', 'Concierge','Receptionist', 'Porter',
                                            'Hostes', 'Staff Hotel'])
            address = fake.address()
            contact_add = fake.random_number(digits=8, fix_len=True)
            username = fake.user_name()
            password = fake.password()
            cur.execute("INSERT INTO employees (fname, lname, job_department, address, contact_add, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (fname, lname, job_department, address, contact_add, username, password))
            
        print("Data dummy untuk tabel employees berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel employees: {error}")

# Fungsi untuk membuat data dummy room_class
def insert_room_class(cur, n):
    try:
        for _ in range(n):
            name = fake.word()
            description = fake.text()
            cur.execute("INSERT INTO room_class (name, description) VALUES (%s, %s)", (name, description))

        print("Data dummy untuk tabel room_class berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel room_class: {error}")

# Fungsi untuk membuat data dummy room_information
def insert_room_information(cur, n):
    try:
        cur.execute("SELECT class_ID FROM room_class")
        class_ids = [row[0] for row in cur.fetchall()]
        for _ in range(n):
            class_ID = random.choice(class_ids)
            description = fake.text()
            price = fake.random_number(digits=5)
            cur.execute("INSERT INTO room_information (class_ID, description, price) VALUES (%s, %s, %s)", (class_ID, description, price))

        print("Data dummy untuk tabel room_information berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel room_information: {error}")

# Fungsi untuk membuat data dummy reservation
def insert_reservation(cur, n):
    try:
        cur.execute("SELECT cust_ID FROM customer_information")
        customer_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT room_ID FROM room_information")
        room_ids = [row[0] for row in cur.fetchall()]
        for _ in range(n):
            if not customer_ids or not room_ids:
                print("Tidak ada data pelanggan atau kamar.")
                return

            customer_ID = random.choice(customer_ids)
            room_ID = random.choice(room_ids)
            reservation_date = fake.date_time_this_year()
            date_in = reservation_date + timedelta(days=random.randint(1, 10))
            date_out = date_in + timedelta(days=random.randint(1, 14))
            cur.execute("INSERT INTO reservation (customer_ID, room_ID, reservation_date, date_in, date_out) VALUES (%s, %s, %s, %s, %s)",
                        (customer_ID, room_ID, reservation_date, date_in, date_out))
            
        print("Data dummy untuk tabel reservation berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel reservation: {error}")

# Fungsi untuk membuat data dummy transactions
def insert_transactions(cur, n):
    try:
        cur.execute("SELECT cust_ID FROM customer_information")
        customer_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT payment_ID FROM payments")
        payment_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT employee_ID FROM employees")
        employee_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT reservation_ID FROM reservation")
        reservation_ids = [row[0] for row in cur.fetchall()]

        for _ in range(n):
            if not customer_ids or not payment_ids or not employee_ids or not reservation_ids:
                print("Tidak ada data pelanggan, pembayaran, karyawan, atau reservasi.")
                return
            
            customer_ID = random.choice(customer_ids)
            payment_ID = random.choice(payment_ids)
            employee_ID = random.choice(employee_ids)
            reservation_ID = random.choice(reservation_ids)
            transaction_date = fake.date_time_this_year()
            transaction_name = random.choice(['Room Booking', 'Room Service', 'Spa Services', 'Laundry Service', 
                                            'Restaurant Bill', 'Mini Bar', 'Conference Room Booking', 'Gym Membership', 
                                            'Transport Service', 'Extra Bed', 'WiFi Charge', 'Late Check-out', 'Early Check-in', 
                                            'Parking Fee', 'Event Booking'])
            cur.execute("INSERT INTO transactions (customer_ID, payment_ID, employee_ID, reservation_ID, transaction_date, transaction_name) VALUES (%s, %s, %s, %s, %s, %s)",
                        (customer_ID, payment_ID, employee_ID, reservation_ID, transaction_date, transaction_name))
            
        print("Data dummy untuk tabel transactions berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel transactions: {error}")

# Fungsi untuk membuat data dummy reports
def insert_reports(cur, n):
    try:
        cur.execute("SELECT transaction_ID FROM transactions")
        transaction_ids = [row[0] for row in cur.fetchall()]
        for _ in range(n):
            if not transaction_ids:
                print("Tidak ada data transaksi.")
                return
            
            transaction_ID = random.choice(transaction_ids)
            information = fake.text()
            date = fake.date_time_this_year()
            cur.execute("INSERT INTO reports (transaction_ID, information, date) VALUES (%s, %s, %s)", (transaction_ID, information, date))

        print("Data dummy untuk tabel reports berhasil dimasukkan.")
    
    except Exception as error:
        print(f"Error saat memasukkan data dummy ke tabel reports: {error}")

def insert_data_dummy_to_MySQL():
    # Mendapatkan koneksi dari MySqlHook
    hook = MySqlHook(mysql_conn_id='id_mysql')
    conn = hook.get_conn()
    cur = conn.cursor()

    # Pilih database yang ingin digunakan
    cur.execute("USE project_dibimbing")

    # Menjalankan fungsi-fungsi di atas untuk memasukkan data dummy
    insert_customer_information(cur, 100)
    insert_employees(cur, 50)
    insert_room_class(cur, 5)
    insert_room_information(cur, 100)
    insert_reservation(cur, 100)
    insert_payments(cur, 100)
    insert_transactions(cur, 100)
    insert_reports(cur, 100)

    # Commit perubahan dan tutup koneksi
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":

    insert_data_dummy_to_MySQL()
