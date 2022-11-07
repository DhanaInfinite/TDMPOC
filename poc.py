from faker import Faker
import secrets
import string
import pandas as pd
import re
import mysql.connector
from sqlalchemy import create_engine
from cryptography.fernet import Fernet
from random import *
n=100
def mygen():
    con=mysql.connector.connect(user='root',password='1525',host='localhost',database='dhanatdmpoc')
    cursor=con.cursor()
    cursor.execute('''create table if not exists customers(customer_id int NOT NULL primary key,customer_name varchar(150),
                customer_address varchar(256),customer_dob varchar(50),credit_card_number int,customer_ssn int)''')

    cursor.execute('''create table if not exists products(product_id int NOT NULL primary key,product_name varchar(150),
                product_price double(8,2))''')

    cursor.execute('''create table if not exists orders(order_id int NOT NULL primary key,customer_id int,product_id int,
                quantity int,order_total double(8,2))''')

    #cursor.execute('''create table if not exists dev_customers(customer_id int primary key,customer_name varchar(150),
                #customer_address varchar(256),customer_dob varchar(50),credit_card_number int,customer_ssn int)''')

    engine=create_engine('mysql+mysqldb://root:1525@localhost/dhanatdmpoc')
    con.commit()


    fake = Faker(locale='en_US')
    fake_customers = [
            {'customer_id': fake.random_number(4),
             'customer_name': fake.name(),
             'customer_address': fake.address(),
             'customer_dob': fake.date_between(start_date='-60y', end_date='-20y'),
             'credit_card_number': fake.credit_card_number(),
             'customer_ssn': ''.join(secrets.choice(string.digits) for i in range(9))
             }
            for x in range(0,n)]

    df1 = pd.DataFrame(fake_customers)
    
    df1.to_excel('Customers/customers.xlsx')
    df1.to_sql('customers',engine,if_exists='replace',index=False)

    #df1.customer_ssn = df1.customer_ssn.apply(lambda x: re.sub(r'\d', '*', x, count=5))
    #df1.credit_card_number = df1.credit_card_number.apply(lambda x: re.sub(r'\d', '*', x, count=10))

    #df1.to_excel('Dev_Customers/dev_customers.xlsx')
    #df1.to_sql('dev_customers',engine,if_exists='replace',index=False)

    list=['pen','laptop','pencil','laptop bag','monitor','generator','tablet','mobile','ipad','computer','luggage bag','earphones','pendrive','headphones']
    fake_products = [
            {'product_id': fake.random_number(6),
             'product_name': choice(list),
             'product_price': fake.random_number(3)
             }
            for x in range(0,n)]

    df2 = pd.DataFrame(fake_products)
    df2.to_excel('Products/products.xlsx')
    df2.to_sql('products',engine,if_exists='replace',index=False)


    #print("Fetching Data from Customer table")

    list1=[]
    cursor.execute("select customer_id from customers")
    data=cursor.fetchall()
    #print(data)
    for i in data:
        for x in i:
            list1.append(x)
    #print(list1)

    list2=[]
    cursor.execute("select product_id from products")
    data=cursor.fetchall()
    #print(data)
    for i in data:
        for x in i:
            list2.append(x)
    #print(list2)

    list3=[1,2,3,4,5,6,7,8,9,10]
    fake_orders = [
            {'oder_id': fake.random_number(4),
             'customer_id':choice(list1),
             'product_id': choice(list2),
             'quantity':choice(list3),
             'order_total': (choice(list3)*fake.random_number(3))
             }
            for x in range(0,n)]


    df3 = pd.DataFrame(fake_orders)
    df3.to_excel('Orders/orders.xlsx')
    df3.to_sql('orders',engine,if_exists='replace',index=False)

    con.close()
    
    #Encrypt and Decrypt
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()

    with open('mykey.key', 'wb') as mykey:
        mykey.write(key)
    with open('mykey.key', 'rb') as mykey:
        key = mykey.read()
    #print(key)
    f = Fernet(key)
    
    #Customers Data
    with open('Customers/customers.xlsx', 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open ('Customers/enc_customers.xlsx', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    

    with open('Customers/enc_customers.xlsx', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open('Customers/dec_customers.xlsx', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

    #Product Dta
    with open('Products/products.xlsx', 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open ('Products/enc_products.xlsx', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    

    with open('Products/enc_products.xlsx', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open('Products/dec_products.xlsx', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

    #Orders Data
    with open('Orders/orders.xlsx', 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open ('Orders/enc_orders.xlsx', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    

    with open('Orders/enc_orders.xlsx', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open('Orders/dec_orders.xlsx', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
#mygen()
        