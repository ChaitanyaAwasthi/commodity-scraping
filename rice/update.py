import pandas as pd 



rice_5kg = pd.read_csv(r"C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_5kg.csv")
rice_10kg = pd.read_csv(r"C:\Users\chait\OneDrive\Desktop\scrape\rice_data\rice_10kg.csv")



rice_5kg_csv = rice_5kg.to_csv(r'G:\My Drive\Rice Data\rice data new\5kg\5kg_rice.csv', index=False)
rice_10kg_csv = rice_10kg.to_csv(r'G:\My Drive\Rice Data\rice data new\10kg\10kg_rice.csv', index=False)

# C:\Users\chait\AppData\Local\Microsoft\WindowsApps\python.exe
#C:\Users\chait\OneDrive\Desktop\scrape\rice\update.py
