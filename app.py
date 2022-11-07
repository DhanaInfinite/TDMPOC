import poc
import poc2
import MySQLdb 
from flask import Flask, render_template 
conn = MySQLdb.connect("localhost","root","1525","dhanatdmpoc" ) 
cursor = conn.cursor() 

app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/generate')
def generate():
    poc.mygen()
    return render_template('sample.html')

@app.route('/clone_to_dev')
def clone_to_dev():
    poc2.mygen2()
    return render_template('sample2.html')


@app.route('/customers')
def customers(): 
    cursor.execute("select * from customers") 
    data = cursor.fetchall() #data from database 
    return render_template("customers.html", value=data) 

@app.route('/products')
def products(): 
    cursor.execute("select * from products") 
    data = cursor.fetchall() #data from database 
    return render_template("products.html", value=data) 

@app.route('/orders')
def orders(): 
    cursor.execute("select * from orders") 
    data = cursor.fetchall() #data from database 
    return render_template("orders.html", value=data) 

@app.route('/dev_customers/<int:n>')
def dev_customers(n): 
    cursor.execute("select * from dev_customers") 
    data = cursor.fetchmany(n) #data from database 
    return render_template("dev_customers.html", value=data) 

if __name__=='__main__':
    app.run(debug=True)
    