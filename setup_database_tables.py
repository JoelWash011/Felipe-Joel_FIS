import sqlite3
import os,csv

def create_database(filename):
    """ create a database connection to an SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(filename)
    except sqlite3.Error as e:
        print(e)
    else:
        print(f'Created the database file. - {filename}')
    finally:
        if connection:
            connection.close()

def create_tables(filename):
    create_sql_statement = ["CREATE TABLE INVENTORY (MaterialID TEXT PRIMARY KEY, MaterialName TEXT, Quantity INTEGER, ReorderAmount INTEGER, Location TEXT);",
"CREATE TABLE SUPPLIES (SupplyID TEXT PRIMARY KEY, VendorID TEXT, MaterialID TEXT, UnitPrice REAL);",
"CREATE TABLE MATERIAL_ORDER (MaterialOrderID TEXT PRIMARY KEY, MaterialID TEXT, SupplyID TEXT, InOrOut TEXT, Quantity INTEGER);",
"CREATE TABLE CUSTOMER (CustomerID TEXT PRIMARY KEY, CustomerName TEXT, ContactEmail TEXT);",
"CREATE TABLE CUSTOMER_ORDER (CustomerOrderID TEXT PRIMARY KEY, CustomerID TEXT, MaterialOrderID TEXT, CustomerOrderDate TEXT, CustomerOrderTotal REAL, CustomerOrderStatus TEXT);",
"CREATE TABLE CUSTOMER_BILL (BillID TEXT PRIMARY KEY, CustomerOrderID TEXT, CustomerID TEXT, BillDate TEXT, DueDate TEXT, TotalAmountBilled REAL, TotalAmountPaid REAL);",
"CREATE TABLE CUSTOMER_PAYMENT (CustomerPaymentID TEXT PRIMARY KEY, BillID TEXT, PaymentDate TEXT, AmountPaid REAL);",
"CREATE TABLE VENDOR (VendorID TEXT PRIMARY KEY, VendorName TEXT, VendorEmail TEXT);",
"CREATE TABLE VENDOR_ORDER (VendorOrderID TEXT PRIMARY KEY, VendorID TEXT, MaterialOrderID TEXT, VendorOrderDate TEXT, VendorOrderTotal REAL, VendorOrderStatus TEXT);",
"CREATE TABLE VENDOR_INVOICE (InvoiceID TEXT PRIMARY KEY, VendorOrderID TEXT, VendorInvoiceDate TEXT, VendorInvoiceDueDate TEXT, VendorInvoiceTotalAmount REAL, VendorInvoicePaymentStatus TEXT, VendorInvoiceDatePaid TEXT);",
"CREATE TABLE VENDOR_PAYMENT (VendorPaymentID TEXT PRIMARY KEY, InvoiceID TEXT, VendorPaymentDate TEXT, VendorAmountPaid REAL);"]
    
    for statement in create_sql_statement:
        try:
            connection = sqlite3.connect(filename)
            cursor = connection.cursor()
            cursor.execute(statement)
        except sqlite3.Error as e:
            print(e)
        else:
            print(f'created database table {statement}')
        finally:
            if connection:
                connection.close()

def insert_table(filename):
    insert_sql_statement = """insert into countries(country, continent) values(?,?)"""
    connection = sqlite3.connect(filename)
    try: 
        new_country = ('Japans','Asias' )
        connection.execute(insert_sql_statement, new_country)
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    else:
        print(f'added new row - {insert_sql_statement}')
    finally:
        if connection:
            connection.close()

def select_table(filename):
    connection = sqlite3.connect(filename)
    my_cursor = connection.cursor()
    query_statement = """Select * from countries where country = ?"""
    values = ('Japan',)
    try:
        my_cursor.execute(query_statement,values)
        rows = my_cursor.fetchall()
        if rows:
            print(my_cursor.description)
            print(f"Data for country: {values[0]}")
            # Optionally, print column headers if you know them or fetch them from cursor.description
            # For simplicity, just printing rows here:
            for row in rows:
                print(row)
        else:
            print(f"No data found for country: {values[0]}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close() # Always close the connection

def read_tables(filename):
    connection = sqlite3.connect(filename)
    my_cursor = connection.cursor()
#Viewing the tables in the database
# reuse the code from 00_create_database.py to see the list of tables <=== TO DO 
    sql_tables_list = "SELECT name FROM sqlite_master  WHERE type='table';"
    my_cursor = connection.execute(sql_tables_list)
    print(my_cursor.fetchall())

    my_cursor.execute('select * from INVENTORY')
    rows = my_cursor.fetchall()
    print(rows)
    for row in rows:
        print(row)
#==  Viewing the column names of a table
#using cursor.description
    column_names = [desc[0] for desc in my_cursor.description]
    print(column_names)
#
#using the rows  of sqlite_schema table
    my_cursor.execute('select * from sqlite_schema')
    rows = my_cursor.fetchall()
    for row in rows:
        print(row[4])

def delete_records(filename):
    connection = sqlite3.connect(filename)
    my_cursor = connection.cursor()
#print(my_cursor.execute('select * from sales where country = 'United States'))
    delete_sql_statement = """
    delete from sales 
    where country = ? and 
    year = ?
    """
    try:
        values = ('Canada', 2019)
        my_cursor.execute(delete_sql_statement, values )
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    else:
        print('Delete completed')
    finally:
        if connection:
            connection.close()

def update_table(filename):
    connection = sqlite3.connect(filename)
    my_cursor = connection.cursor()
#print(my_cursor.execute('select * from sales where country = 'United States'))
    update_sql_statement = """
    update sales 
    set sales = ? 
    where country = ? and 
    year = ?
    """
    try:
        values = (-200, 'United States', 2018)
        my_cursor.execute(update_sql_statement, values )
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    else:
        print('Update completed')
    finally:
        if connection:
            connection.close()

def bulk_import(filename,tables):

    for table in tables:
        data = []
        num_columns = 0
        filepath = os.path.dirname(os.path.abspath(__file__))+'/csv_files/'+table.lower()+'.csv'
        with open(filepath, 'r', newline='') as inputfile:
            reader = csv.DictReader(inputfile)
            fieldnames = reader.fieldnames
            if fieldnames:
                num_columns = len(fieldnames)
            for row in reader:
                ordered_values = tuple(row[col] for col in fieldnames) 
                data.append(ordered_values)
        #print(data)
        connection = sqlite3.connect(filename)
        my_cursor = connection.cursor()

        #calculate the ? marks string
        placeholders_string = ",".join(["?"] * num_columns)

    # Perform bulk insert
        try:
            my_cursor.executemany(f'INSERT INTO {table.lower()} VALUES ({placeholders_string})', data)
            connection.commit()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Import completed for "+table.lower())
        finally:
            if connection:
                connection.close()

if __name__ == '__main__':
    #set database filename
    Databasefilename = "FIS.db"
    #full list of database tables for FIS data
    tables = ["INVENTORY","SUPPLIES","MATERIAL_ORDER","CUSTOMER","CUSTOMER_ORDER","CUSTOMER_BILL","CUSTOMER_PAYMENT","VENDOR","VENDOR_ORDER","VENDOR_INVOICE","VENDOR_PAYMENT"]
    #get current directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    files_list = os.listdir(script_directory)
    #get full file path
    full_database_filepath = os.path.join(script_directory, Databasefilename)
    #verify database file exists
    if Databasefilename in files_list:
        print(f'file exists - {full_database_filepath}')
    else:
        #crete database file
        create_database(full_database_filepath)
    
    #create a tables in bulk
    create_tables(full_database_filepath)
    #insert into table
    #insert_table(full_database_filepath)
    #select data
    #select_table(full_database_filepath)
    #create a databse connection
    #bulk import
    bulk_import(full_database_filepath,tables)
    connection = sqlite3.connect(full_database_filepath)

    #print all tables
    for table in tables:
        #print(connection.execute(f'Select * from {table}').description)
        print(table)
        headers = connection.execute(f'Select * from {table}').description
        for header in headers:
            print(f'{header[0]:<20}', end=" ")
        print()
        print(connection.execute(f'Select * from {table}').fetchall())
    connection.close()

