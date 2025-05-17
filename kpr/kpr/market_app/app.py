from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# Enable automatic template reloading
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

# URL to scrape
url = "https://vegetablemarketprice.com/market/tamilnadu/today"

# Define headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch and parse data
def fetch_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table")
        if table:
            rows = table.find_all("tr")
            table_headers = [header.text.strip() for header in rows[0].find_all("th")]
            data_list = []
            for row in rows[1:]:
                cols = row.find_all("td")
                data = [col.text.strip() for col in cols]
                data_list.append(data)
            return data_list
        else:
            print("No table found on the page.")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Function to calculate price increase
def calculate_increase(data):
    result = []
    for row in data:
        vegetable_name = row[1]
        current_price = float(row[2].replace("₹", "").strip())
        previous_price_range = row[3].split(" - ")
        previous_min_price = float(previous_price_range[0].strip())

        increase = current_price - previous_min_price

        row_dict = {
            "Vegetable": vegetable_name,
            "Current Price": current_price,
            "Previous Min Price": previous_min_price,
            "Price Increase": increase
        }
        result.append(row_dict)
    return result

# Fetch and process data
data = fetch_data(url)
if data:
    price_increases = calculate_increase(data)
    with open("price_increases.json", "w") as f:
        json.dump(price_increases, f, indent=4)
    print("Data saved to 'price_increases.json'")
else:
    print("No data fetched from the URL.")

@app.route('/market')
def home():
    with open("price_increases.json", "r") as f:
        price_data = json.load(f)
    return render_template('m.html', price_data=price_data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)  # Ensures auto-reload in development