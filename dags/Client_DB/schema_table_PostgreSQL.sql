-- Membuat Schema Database
CREATE SCHEMA IF NOT EXISTS project_dibimbing;

-- Tabel Customer Information
CREATE TABLE IF NOT EXISTS project_dibimbing.customer_information (
    cust_ID SERIAL PRIMARY KEY,
    custfname VARCHAR(255),
    custlname VARCHAR(255),
    address VARCHAR(255),
    status VARCHAR(255)
);

-- Tabel Payments
CREATE TABLE IF NOT EXISTS project_dibimbing.payments (
    payment_ID SERIAL PRIMARY KEY,
    customer_ID INT,
    payment_date TIMESTAMP,
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_ID) 
        REFERENCES project_dibimbing.customer_information(cust_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Tabel Employees
CREATE TABLE IF NOT EXISTS project_dibimbing.employees (
    employee_ID SERIAL PRIMARY KEY,
    fname VARCHAR(255),
    lname VARCHAR(255),
    job_department VARCHAR(255),
    address VARCHAR(255),
    contact_add INT,
    username VARCHAR(255),
    password VARCHAR(255)
);

-- Tabel Room Class
CREATE TABLE IF NOT EXISTS project_dibimbing.room_class (
    class_ID SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255)
);

-- Tabel Room Information
CREATE TABLE IF NOT EXISTS project_dibimbing.room_information (
    room_ID SERIAL PRIMARY KEY,
    class_ID INT,
    description VARCHAR(255),
    price INT,
    CONSTRAINT fk_room_class
        FOREIGN KEY (class_ID) 
        REFERENCES project_dibimbing.room_class(class_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Tabel Reservation
CREATE TABLE IF NOT EXISTS project_dibimbing.reservation (
    reservation_ID SERIAL PRIMARY KEY,
    customer_ID INT,
    room_ID INT,
    reservation_date TIMESTAMP,
    date_in TIMESTAMP,
    date_out TIMESTAMP,
    CONSTRAINT fk_customer_reservation
        FOREIGN KEY (customer_ID) 
        REFERENCES project_dibimbing.customer_information(cust_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_room_reservation
        FOREIGN KEY (room_ID) 
        REFERENCES project_dibimbing.room_information(room_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Tabel Transaction
CREATE TABLE IF NOT EXISTS project_dibimbing.transactions (
    transaction_ID SERIAL PRIMARY KEY,
    customer_ID INT,
    payment_ID INT,
    employee_ID INT,
    reservation_ID INT,
    transaction_date TIMESTAMP,
    transaction_name VARCHAR(255),
    CONSTRAINT fk_customer_transaction
        FOREIGN KEY (customer_ID) 
        REFERENCES project_dibimbing.customer_information(cust_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_payment_transaction
        FOREIGN KEY (payment_ID) 
        REFERENCES project_dibimbing.payments(payment_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_employee_transaction
        FOREIGN KEY (employee_ID) 
        REFERENCES project_dibimbing.employees(employee_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_reservation_transaction
        FOREIGN KEY (reservation_ID) 
        REFERENCES project_dibimbing.reservation(reservation_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Tabel Reports
CREATE TABLE IF NOT EXISTS project_dibimbing.reports (
    report_ID SERIAL PRIMARY KEY,
    transaction_ID INT,
    information VARCHAR(255),
    date TIMESTAMP,
    CONSTRAINT fk_transaction_report
        FOREIGN KEY (transaction_ID) 
        REFERENCES project_dibimbing.transactions(transaction_ID)  -- tambahkan schema project_dibimbing
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);
