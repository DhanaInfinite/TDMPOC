from faker import Faker
import secrets
import string
import pandas as pd
import re
import mysql.connector
from sqlalchemy import create_engine
from random import *
import farmhash
from sqlalchemy import Integer, String,BigInteger,DateTime
#from sqlalchemy.dialects.mysql import VARCHAR

def mygen2():
    con=mysql.connector.connect(user='root',password='1525',host='localhost',database='dhanatdmpoc')
    cursor=con.cursor()

    cursor.execute('''create table if not exists dev_customers(customer_id int NOT NULL primary key,customer_name varchar(150),
                customer_address varchar(256),customer_dob varchar(50),credit_card_number BIGINT ,customer_ssn BIGINT)''')

    engine=create_engine('mysql+mysqldb://root:1525@localhost/dhanatdmpoc')
    
    con.commit()
    
    df1=pd.read_sql('customers',engine,columns=['customer_id','customer_name','customer_address','customer_dob','credit_card_number','customer_ssn'])

    
    #df1.customer_ssn = df1.customer_ssn.apply(lambda x: re.sub(r'\d', '*', x, count=5))
    #df1.credit_card_number = df1.credit_card_number.apply(lambda x: re.sub(r'\d', '*', x, count=10))
    
    df1.credit_card_number = df1.credit_card_number.apply(lambda x: farmhash.hash64(x))
    df1.customer_ssn = df1.customer_ssn.apply(lambda x: farmhash.hash64(x))
    
    #print(df1)
    

    df1.to_excel('Dev_Customers/dev_customers.xlsx')
    df1.to_sql('dev_customers',engine,if_exists='replace',index=False,dtype={'credit_card_number':String(200),'customer_ssn':String(200)})

#mygen2()
