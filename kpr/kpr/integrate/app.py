from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration for 'sale' database
sale_db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 'sale'
}

# Database configuration for 's2c_store' database
s2c_store_db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 's2c_store'
}

# Function to fetch products from the 'sale' database
def get_products():
    connection = mysql.connector.connect(**sale_db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT product_name, amount, stoks FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

# Function to fetch store details from the 's2c_store' database
def get_store_details():
    connection = mysql.connector.connect(**s2c_store_db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT store_name, full_name, address FROM store_detials LIMIT 1")  # Fetch the first store
    store_details = cursor.fetchone()
    cursor.close()
    connection.close()
    return store_details

# Home route (for 'sale' database)
@app.route('/')
def home():
    products = get_products()  # Fetch products from the 'sale' database
    return render_template('index.html', products=products)

# Dashboard route (for 's2c_store' database)
@app.route('/dashboard')
def dashboard():
    store_details = get_store_details()  # Fetch store details from the 's2c_store' database
    if store_details:
        return render_template('dashboard.html', store_details=store_details)
    else:
        return "No store details found in the database."

if __name__ == '__main__':
    app.run(debug=True)