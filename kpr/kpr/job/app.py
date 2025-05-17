from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',       # Default XAMPP username
    'password': '',       # Default XAMPP password (empty)
    'host': 'localhost',  # Default host
    'database': 'job_registeration',  # Your database name
    'port': 3306          # Default MySQL port
}

def get_db_connection():
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def fetch_labors(district=None, village=None):
    """Fetch laborers from the database based on district and village filters."""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        
        if district and village:
            # Query to filter laborers by district and village
            query = """SELECT * FROM form 
                       WHERE `district-` = %s AND village = %s"""
            cursor.execute(query, (district, village))
        else:
            # Query to fetch all laborers
            query = "SELECT * FROM form"
            cursor.execute(query)
        
        labors = cursor.fetchall()
        return labors
    except Error as err:
        print(f"Error executing query: {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    district = request.form.get('district') if request.method == 'POST' else None
    village = request.form.get('village') if request.method == 'POST' else None

    # Fetch laborers based on filters
    labors = fetch_labors(district, village)
    
    if labors is None:
        return "An error occurred while fetching data from the database.", 500

    return render_template('index.html', labors=labors)

if __name__ == '__main__':
    app.run(debug=True)