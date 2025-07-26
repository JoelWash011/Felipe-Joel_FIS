import sqlite3
import os, random
from datetime import date, timedelta


def searchTable(filename,tablename,idname):
        while True:
            #input number
            inputnumber = input(f"Enter {tablename} ID: ")
            #search number query
            sql_query_search = f"SELECT * FROM {tablename}  WHERE {idname} = '{inputnumber}';"
            try: 
                connection = sqlite3.connect(filename)
                my_cursor = connection.cursor()
                #Viewing the tables in the database
                my_cursor = connection.execute(sql_query_search)
                rows = my_cursor.fetchall()
            except sqlite3.Error as e:
                print(e)
            else:
                if rows:
                    print(f"Data found - {rows[0]}")
                    return rows[0]
                else:
                    print(f"no {idname} found try again...")
            finally:
                if connection:
                    connection.close()

def addInvoice(filename,order):
    createquestion = input("Create Invoice from Order? (Y/N)")
    if createquestion == "Y":
        VendorOrderID = order[0]
        VendorOrderTotal = order[4]
        insert_sql_statement = """insert into VENDOR_INVOICE(
            InvoiceID,VendorOrderID,VendorInvoiceDate,
            VendorInvoiceDueDate,VendorInvoiceTotalAmount,
            VendorInvoicePaymentStatus,VendorInvoiceDatePaid) values(?,?,?,?,?,?,?)"""
        try: 
            unique_invoice_id = str(random.randint(1000, 9999))
            connection = sqlite3.connect(filename)
            order_details = ('INV'+unique_invoice_id,VendorOrderID,date.today(),date.today()+ timedelta(days=30),VendorOrderTotal,'Pending',None)
            connection.execute(insert_sql_statement, order_details)
            connection.commit()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Invoice added")
            print('INV'+unique_invoice_id,VendorOrderID,date.today(),date.today()+ timedelta(days=30),VendorOrderTotal,'Pending',None)
        finally:
            if connection:
                connection.close()
    else:
        print("No invoice ordered")
        return

def addVendorPayment(filename,invoice):
    createquestion = input(f"Create Payment from Invoice {invoice[0]} for {invoice[4]}? (Y/N)")
    if createquestion == "Y":
        VendorInvoiceID = invoice[0]
        VendorPaymentTotal = invoice[4]
        insert_sql_statement = """insert into VENDOR_PAYMENT(
                                VendorPaymentID,InvoiceID,VendorPaymentDate,VendorAmountPaid
                                ) values(?,?,?,?)"""
        try: 
            unique_id = str(random.randint(1000, 9999))
            connection = sqlite3.connect(filename)
            sql_details = ('VPAY'+unique_id,VendorInvoiceID,date.today(),VendorPaymentTotal)
            connection.execute(insert_sql_statement, sql_details)
            connection.commit()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Payment Sent")
            print('VPAY'+unique_id,VendorInvoiceID,date.today(),VendorPaymentTotal)
            return 'Paid'
        finally:
            if connection:
                connection.close()
    else:
        print("No invoice ordered")
        return

def updateVendorInvoiceStatus(filename,invoice,status):
    createquestion = input(f"Update Invoice {invoice[0]} status to {status} today {date.today()}? (Y/N)")
    if createquestion == "Y":
        InvoiceID = invoice[0]
        VendorOrderID = invoice[1]
        sql_statement1 = """
        update VENDOR_INVOICE 
        set VendorInvoicePaymentStatus = ?
        where InvoiceID = ?
        """
        sql_statement2 = """
        update VENDOR_INVOICE 
        set VendorInvoiceDatePaid = ?
        where InvoiceID = ?
        """
        try: 
            connection = sqlite3.connect(filename)
            order_details = (status,InvoiceID)
            connection.execute(sql_statement1, order_details)
            order_details = (date.today(),InvoiceID)
            connection.execute(sql_statement2, order_details)
            connection.commit()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Invoice Paid")
            return VendorOrderID
        finally:
            if connection:
                connection.close()
    else:
        print("No invoice ordered")
        return

def updateVendorOrderStatus(filename,orderID,status):
    createquestion = input(f"Update Order {orderID} status to {status}? (Y/N)")
    if createquestion == "Y":
        sql_statement = """
        update VENDOR_ORDER
        set VendorOrderStatus = ?
        where VendorOrderID = ?
        """
        try: 
            connection = sqlite3.connect(filename)
            order_details = (status,orderID)
            connection.execute(sql_statement, order_details)
            connection.commit()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Order Completed")
            return
        finally:
            if connection:
                connection.close()
    else:
        print("No invoice ordered")
        return

def sendPayment(filename,orderID):
    #search order ID
    sql_query_search_vendor_order = f"SELECT * FROM VENDOR_ORDER  WHERE VendorOrderID = '{orderID}';"
    try: 
        connection = sqlite3.connect(filename)
        my_cursor = connection.cursor()
        #Viewing the tables in the database
        my_cursor = connection.execute(sql_query_search_vendor_order)
        rows = my_cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    else:
        if rows:
            print(f"Data found - {rows[0]}")
            vendorID = rows[0][1]
        else:
            print("no order number found try again...")
    finally:
        if connection:
            connection.close()
    
    #find vendor info
    sql_query_search_vendor = f"SELECT * FROM VENDOR  WHERE VendorID = '{vendorID}';"
    try: 
        connection = sqlite3.connect(filename)
        my_cursor = connection.cursor()
        #Viewing the tables in the database
        my_cursor = connection.execute(sql_query_search_vendor)
        rows = my_cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    else:
        if rows:
            #print(f"Data found - {rows[0]}")
            vendorname = rows[0][1]
            vendoremail = rows[0][2]
            print(f"Email payment sent to {vendorname} - {vendoremail}")
        else:
            print("no vendor number found try again...")
    finally:
        if connection:
            connection.close()

def searchDueInvoices(filename):
    while True:
        #invoices due in the last x days
        daysold = int(input("How many days back would you like to look for Due invoices?: "))
        daysold = date.today()+ timedelta(days=-daysold)
        #search invoice number
        sql_query_search = f"SELECT * FROM VENDOR_INVOICE  WHERE VendorInvoicePaymentStatus = 'Pending' and VendorInvoiceDueDate >= '{daysold}' and VendorInvoiceDueDate <= '{date.today()}' ;"
        try: 
            connection = sqlite3.connect(filename)
            my_cursor = connection.cursor()
            #Viewing the tables in the database
            my_cursor = connection.execute(sql_query_search)
            rows = my_cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        else:
            if rows:
                for row in rows:
                    print(f"Data found - {row}")
                return rows
            else:
                print("no invoice number found try again...")
                return
        finally:
            if connection:
                connection.close()

def payments_screen():
    Databasefilename = "FIS.db"
    #get current directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    #get full file path
    full_database_filepath = os.path.join(script_directory, Databasefilename)
    menu = """ 
                        *******************************************
                                       FIS - Payments
                        *******************************************
                 1. Pay Vendor on Due Date         2. Send payment\n
                 0. Back to Main Menu
                 >>>"""
    while True:
        choice = input(menu)
        match choice:
            case '1':
                invoices = searchDueInvoices(full_database_filepath)
                if invoices:
                    continuetoproccess = input("Pay these Invoices? (Y/N)")
                    if continuetoproccess == 'Y':
                        for invoice in invoices:
                            status = addVendorPayment(full_database_filepath,invoice)
                            #update invoice
                            orderID = updateVendorInvoiceStatus(full_database_filepath,invoice,status)
                            #update order
                            updateVendorOrderStatus(full_database_filepath,orderID,'Completed')
                            #email payment
                            sendPayment(full_database_filepath,orderID)
                    else:
                        print()
            case '2':
                #find the invoice to pay
                #invoice = searchInvoice(full_database_filepath)
                invoice = searchTable(full_database_filepath,'VENDOR_INVOICE','InvoiceID')
                if invoice[5] == 'Paid':
                    print("Already Paid")
                else:
                #add payment
                    status = addVendorPayment(full_database_filepath,invoice)
                    #update invoice
                    orderID = updateVendorInvoiceStatus(full_database_filepath,invoice,status)
                    #update order
                    updateVendorOrderStatus(full_database_filepath,orderID,'Completed')
                    #email payment
                    sendPayment(full_database_filepath,orderID)
            case '0':
                break
        x = input("Press enter to continue...")
        os.system("cls")

def invoices_screen():
    Databasefilename = "FIS.db"
    #get current directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    #get full file path
    full_database_filepath = os.path.join(script_directory, Databasefilename)
    menu = """ 
                        *******************************************
                                       FIS - Invoices
                        *******************************************
                 1. Add Invoice\n
                 0. Back to Main Menu
                 >>>"""
    while True:
        choice = input(menu)
        match choice:
            case '1':
                order = searchTable(full_database_filepath,'VENDOR_ORDER','VendorOrderID')
                if order[5] == 'Completed':
                    print('Order Already Completed')
                else:
                    addInvoice(full_database_filepath,order)
            case '0':
                break
        x = input("Press enter to continue...")
        os.system("cls")

if __name__ == '__main__':
    menu = """ 
                        *******************************************
                        Welcome to the Financial Institute Program
                            Below are the options to navigate
                                through the application
                        *******************************************
                 1. Invoices                            2. Payments\n
                 0. Exit
                 >>>"""
    #set database filename
    Databasefilename = "FIS.db"
    #full list of database tables for FIS data
    tables = ["INVENTORY","SUPPLIES","MATERIAL_ORDER","CUSTOMER","CUSTOMER_ORDER","CUSTOMER_BILL","CUSTOMER_PAYMENT","VENDOR","VENDOR_ORDER","VENDOR_INVOICE","VENDOR_PAYMENT"]
    #get current directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    #get full file path
    full_database_filepath = os.path.join(script_directory, Databasefilename)
    #verify database file exists
    while True:
        choice = input(menu)
        match choice:
            case '1':#go to invoices screen
                invoices_screen()
            case '2':#go to payments screen
                payments_screen()
            case '0':
                break
        x = input("Press enter to continue...")
        os.system("cls")
