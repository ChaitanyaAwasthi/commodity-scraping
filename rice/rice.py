import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from datetime import datetime


rice_5kg_path = r'C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_5kg.csv'
rice_10kg_path = r'C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_10kg.csv'
rice_20kg_path = r'C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_20kg_path.csv'


    
url_amazon = 'https://www.amazon.ae/s?k=1121+sella+basmati+rice&crid=L1BKYP8WLXUX&sprefix=1121+sella+basmati+rice+%2Caps%2C210&ref=nb_sb_noss_2'
amazon_20kg_url = 'https://www.amazon.ae/Mahmood-Muntaha-1121-Basmati-Rice/dp/B08TJ39WLX/ref=sr_1_9?sr=8-9'
dubai_store_url = 'https://www.dubaistore.com/search?q=1121+sella+basmati'
lul_url = 'https://www.luluhypermarket.com/en-ae/search/?text=1121+sella+basmati+rice%3Arelevance'
dc_url = 'https://www.desertcart.ae/search/1121+sella+basmati+rice'

class RicePriceScraper:
    def __init__(self):
        self.amazon_5kg_df = pd.DataFrame()
        self.amazon_10kg_df = pd.DataFrame()
        self.amazon_20kg_df = pd.DataFrame()
        self.dubai_store_5kg = pd.DataFrame()
        self.dubai_store_10kg = pd.DataFrame()
        self.empty_data = pd.DataFrame()
        
    def scrape_amazon(self, url):
        while True:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                products = soup.find_all("div", class_="sg-col-inner")
                data_5kg = []
                data_10kg = []
                
                for product in products:
                    product_data = {}
                    name_element = product.find("span", class_="a-size-base-plus a-color-base")
                    if name_element:
                        product_data['name'] = name_element.get_text(strip=True)
                    else:
                        product_data['name'] = "Name not found"

                    price_element = product.find("span", class_="a-offscreen")
                    if price_element:
                        product_data['price'] = price_element.get_text(strip=True)
                    else:
                        product_data['price'] = "Price not available"

                    qty_element = product.find_all('span', string=re.compile(r'\b(\d+)\s*kg\b'))

                    for qty in qty_element:
                        match = re.search(r'\b(\d+)\s*kg\b', qty.text)
                        if match:
                            kg = int(match.group(1))
                            if kg == 5:
                                data_5kg.append(product_data)
                            elif kg == 10:
                                data_10kg.append(product_data)
                        else:
                            print("Match not found for the regex provided.")

                # Assign DataFrame values after the loop
                self.amazon_5kg_df = pd.DataFrame(data_5kg)
                self.amazon_10kg_df = pd.DataFrame(data_10kg)

                self.amazon_5kg_df['Qty'] = '5 kg'
                self.amazon_10kg_df['Qty'] = '10 kg'

                self.amazon_5kg_df['website'] = 'Amazon'
                self.amazon_10kg_df['website'] = 'Amazon'

                self.amazon_5kg_df['date'] = datetime.now().date()
                self.amazon_10kg_df['date'] = datetime.now().date()

                self.amazon_5kg_df = self.amazon_5kg_df.drop_duplicates()
                self.amazon_10kg_df = self.amazon_10kg_df.drop_duplicates()

                self.amazon_5kg_df['price'] = self.amazon_5kg_df['price'].str.replace('AED', '').str.strip()
                self.amazon_10kg_df['price'] = self.amazon_10kg_df['price'].str.replace('AED', '').str.strip()

                self.amazon_5kg_df['price'] = pd.to_numeric(self.amazon_5kg_df['price'], errors='coerce')
                self.amazon_10kg_df['price'] = pd.to_numeric(self.amazon_10kg_df['price'], errors='coerce')
                
                return self.amazon_5kg_df, self.amazon_10kg_df
            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}. Retrying")

    def scrape_amazon_20kg(self, url):
        while True:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                name_amazon_20kg = soup.find('span', id='productTitle')
                price_amazon_20kg = soup.find('span', class_='a-price-whole')

                if name_amazon_20kg and price_amazon_20kg:
                    name_amazon_20kg = name_amazon_20kg.get_text(strip=True)
                    price_amazon_20kg_text = price_amazon_20kg.get_text(strip=True)
                    price_amazon_20kg = float(price_amazon_20kg_text.replace(',', ''))

                    self.amazon_20kg_df = pd.DataFrame({
                        'name': [name_amazon_20kg],
                        'price': [price_amazon_20kg],
                        'website': ['Amazon'],
                        'Qty': ['20 kg'],
                        'date': [datetime.now().date()]
                    })
                    return self.amazon_20kg_df
                else:
                    print("Product information not found on Amazon.")
                    return pd.DataFrame()
            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}. Retrying")

    def scrape_dubai_store(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all("div", class_='card card-product card-plain no-shadow product-list-item js-productContainer')

        data = []
        for product in products:
            if product:
                name_element = product.find("h4", class_="card-title product-title").get_text(strip=True)
                price_element = product.find("div", class_="discounted-percent").get_text()

                pattern = r'AED(\d+\.\d+)'  # Match AED followed by numerical part
                price_match = re.search(pattern, price_element)
                if price_match:
                    price = float(price_match.group(1))  # Extract the numerical part and convert to float
                else:
                    price = np.nan  # Set price to NaN if no match found

                pattern = r'(\d+)\s*Kg'
                qty_match = re.findall(pattern, name_element, flags=re.IGNORECASE)

                # Check if quantity is recognized and append data to list
                if qty_match:
                    qty = int(qty_match[0])  # Extract the quantity as an integer
                    data.append({'name': name_element, 'price': price, 'Qty': qty})
                else:
                    # If quantity is not recognized, add data to list with NaN quantity
                    data.append({'name': name_element, 'price': price, 'Qty': np.nan})


        data_df = pd.DataFrame(data)
        self.dubai_store_5kg = data_df[data_df['Qty'] == 5].copy()
        self.dubai_store_10kg = data_df[data_df['Qty'] == 10].copy()
        self.empty_data = data_df[data_df['Qty'].isna()].copy()

        self.dubai_store_5kg['website'] = 'Dubai Store'
        self.dubai_store_10kg['website'] = 'Dubai Store'

        self.dubai_store_5kg['date'] = datetime.now().date()
        self.dubai_store_10kg['date'] = datetime.now().date()

        return self.dubai_store_5kg, self.dubai_store_10kg, self.empty_data
    
    def update_data(self, csv_file_path, df):

        existing_data = pd.read_csv(csv_file_path)
        updated_data = pd.concat([existing_data, df], ignore_index=True)

        updated_data.to_csv(csv_file_path, index=False)

        return updated_data

# Example usage:
if __name__ == '__main__':

    scraper = RicePriceScraper()
    amazon_5kg, amazon_10kg = scraper.scrape_amazon(url_amazon)
    amazon_20kg = scraper.scrape_amazon_20kg(amazon_20kg_url)
    dubai_store_5kg, dubai_store_10kg, empty_data = scraper.scrape_dubai_store(dubai_store_url)

    final_5kg = pd.concat([amazon_5kg, dubai_store_5kg], axis=0)
    final_10kg = pd.concat([amazon_10kg, dubai_store_10kg], axis=0) 

    updated_5kg = scraper.update_data(r'C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_5kg.csv', final_5kg)
    updated_10kg = scraper.update_data(r'C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_10kg.csv', final_10kg)


    # updated_5kg_cloud = updated_5kg.to_csv(r'G:\My Drive\Rice Data\rice data new\5kg\5kg_rice.csv', index=False)
    # updated_10kg_cloud = updated_10kg.to_csv(r'G:\My Drive\Rice Data\rice data new\10kg\10kg_rice.csv', index=False)



    # rice_5kg_csv = final_5kg.to_csv(rice_5kg_path, index=False)
    # rice_10kg_csv = final_10kg.to_csv(rice_10kg_path, index=False)




    # Displaying the results
    print("Amazon 5kg:")
    print(amazon_5kg)
    print("\nAmazon 10kg:")
    print(amazon_10kg)
    print("\nAmazon 20kg:")
    print(amazon_20kg)
    print("\nDubai Store 5kg:")
    print(dubai_store_5kg)
    print("\nDubai Store 10kg:")
    print(dubai_store_10kg)
    print("\nProducts with unknown quantity:")
    print(empty_data)
    print("\n Final 5kg")
    print(final_5kg)
    print("\n Final 10kg")
    print(final_10kg)

# final_5kg = final_5kg
# final_10kg = final_10kg