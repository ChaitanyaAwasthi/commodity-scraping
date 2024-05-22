import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time



cumin_dir = r'C:\Users\chait\OneDrive\Desktop\scrape\cumin_data\cumin.csv'

  # Import the time module

def scrape_amazon_data(url):
    while True:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200: 
            break  # If successful, break out of the loop
        else:
            print("Failed to retrieve data from Amazon. Retrying in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before retrying
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract product names
    names = soup.find_all("span", class_='a-size-base-plus a-color-base a-text-normal')
    names_list = [name.get_text(strip=True) for name in names]
    
    # Extract whole prices
    price_whole = soup.find_all("span", class_='a-price-whole')
    whole_price = [price.get_text(strip=True) for price in price_whole]
    
    # Extract decimal prices
    price_decimal = soup.find_all("span", class_='a-price-fraction')
    decimal_price = [price.get_text(strip=True) for price in price_decimal]
    
    # Combine whole and decimal prices
    prices = [a + b for a, b in zip(whole_price, decimal_price)]
    
    # Create a DataFrame to store the data
    cumin_amazon = pd.DataFrame({
        'Name': names_list,
        'Price': prices,
        'Website': 'Amazon',
        'datetime': datetime.now().date()
    })
    
    # Extract quantities using regex pattern
    pattern = r'(\d+)\s*([a-zA-Z]+)'
    qty = cumin_amazon['Name'].str.extract(pattern)
    cumin_amazon['Qty'] = qty[0] + qty[1]
    
    return cumin_amazon


def update_data(csv_file_path, df):

        existing_data = pd.read_csv(csv_file_path)
        updated_data = pd.concat([existing_data, df], ignore_index=True)

        updated_data.to_csv(csv_file_path, index=False)

        return updated_data


# Example usage
url = "https://www.amazon.ae/s?k=cumin&crid=32P820YBOEQF9&sprefix=cumin%2Caps%2C287&ref=nb_sb_noss_2"
result = scrape_amazon_data(url)
print(result)

# cumin_csv = result.to_csv(cumin_dir, index=False)

updated_result = update_data(r'C:\Users\chait\OneDrive\Desktop\scrape\cumin_data\cumin.csv', result)




