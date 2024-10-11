-- Membuat Database
CREATE DATABASE IF NOT EXISTS project_dibimbing;

-- Gunakan Database yang baru dibuat
USE project_dibimbing;

-- Tabel Customer Information
CREATE TABLE IF NOT EXISTS customer_information (
    cust_ID INT AUTO_INCREMENT PRIMARY KEY,
    custfname VARCHAR(255),
    custlname VARCHAR(255),
    address VARCHAR(255),
    status VARCHAR(255)
);

-- Tabel Payments
CREATE TABLE IF NOT EXISTS payments (
    payment_ID INT AUTO_INCREMENT PRIMARY KEY,
    customer_ID INT,
    payment_date TIMESTAMP,
    FOREIGN KEY (customer_ID) REFERENCES customer_information(cust_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabel Employees
CREATE TABLE IF NOT EXISTS employees (
    employee_ID INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255),
    lname VARCHAR(255),
    job_department VARCHAR(255),
    address VARCHAR(255),
    contact_add INT,
    username VARCHAR(255),
    password VARCHAR(255)
);

-- Tabel Room Class
CREATE TABLE IF NOT EXISTS room_class (
    class_ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255)
);

-- Tabel Room Information
CREATE TABLE IF NOT EXISTS room_information (
    room_ID INT AUTO_INCREMENT PRIMARY KEY,
    class_ID INT,
    description VARCHAR(255),
    price INT,
    FOREIGN KEY (class_ID) REFERENCES room_class(class_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabel Reservation
CREATE TABLE IF NOT EXISTS reservation (
    reservation_ID INT AUTO_INCREMENT PRIMARY KEY,
    customer_ID INT,
    room_ID INT,
    reservation_date TIMESTAMP,
    date_in TIMESTAMP,
    date_out TIMESTAMP,
    FOREIGN KEY (customer_ID) REFERENCES customer_information(cust_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (room_ID) REFERENCES room_information(room_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabel Transaction
CREATE TABLE IF NOT EXISTS transactions (
    transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
    customer_ID INT,
    payment_ID INT,
    employee_ID INT,
    reservation_ID INT,
    transaction_date TIMESTAMP,
    transaction_name VARCHAR(255),
    FOREIGN KEY (customer_ID) REFERENCES customer_information(cust_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (payment_ID) REFERENCES payments(payment_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (employee_ID) REFERENCES employees(employee_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (reservation_ID) REFERENCES reservation(reservation_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabel Reports
CREATE TABLE IF NOT EXISTS reports (
    report_ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ID INT,
    information VARCHAR(255),
    date TIMESTAMP,
    FOREIGN KEY (transaction_ID) REFERENCES transactions(transaction_ID) ON DELETE CASCADE ON UPDATE CASCADE
);