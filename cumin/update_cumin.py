import pandas as pd 



cumin_csv = pd.read_csv(r"C:\Users\chait\OneDrive\Desktop\scrape\cumin_data\cumin.csv")



cumin_csv_cloud = cumin_csv.to_csv(r'G:\My Drive\Rice Data\cumin data\cumin.csv', index=False)


