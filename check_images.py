import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

def check_image_url(row):
    try:
        response = requests.head(row['Image_URL'], timeout=5)
        if response.status_code != 200:
            return row['Food Item']
    except:
        return row['Food Item']
    return None

# Read the CSV file
df = pd.read_csv('diabetesnew.csv')

# Check all image URLs in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(check_image_url, df.to_dict('records')))

# Filter out None values and print unavailable images
unavailable = [r for r in results if r is not None]
print("\nFood items with unavailable images:")
for item in unavailable:
    print(f"- {item}")
