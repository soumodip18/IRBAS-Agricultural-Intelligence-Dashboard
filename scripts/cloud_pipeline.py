from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pandas as pd
import time
from datetime import datetime
from io import StringIO
import os
import json

# ==========================================
# 1. CONFIGURATION: ALL 30 STATES & CLOUD
# ==========================================
STATES = {
    "Andaman and Nicobar": "andaman-and-nicobar", "Andhra Pradesh": "andhra-pradesh", 
    "Arunachal Pradesh": "arunachal-pradesh", "Assam": "assam", "Bihar": "bihar", 
    "Chandigarh": "chandigarh", "Chhattisgarh": "chhattisgarh", "Goa": "goa", 
    "Gujarat": "gujarat", "Haryana": "haryana", "Himachal Pradesh": "himachal-pradesh", 
    "Jammu and Kashmir": "jammu-and-kashmir", "Karnataka": "karnataka", "Kerala": "kerala", 
    "Madhya Pradesh": "madhya-pradesh", "Maharashtra": "maharashtra", "Manipur": "manipur", 
    "Meghalaya": "meghalaya", "Nagaland": "nagaland", "NCT of Delhi": "nct-of-delhi", 
    "Odisha": "odisha", "Pondicherry": "pondicherry", "Punjab": "punjab", 
    "Rajasthan": "rajasthan", "Tamil Nadu": "tamil-nadu", "Telangana": "telangana", 
    "Tripura": "tripura", "Uttar Pradesh": "uttar-pradesh", "Uttarakhand": "uttarakhand", 
    "West Bengal": "west-bengal"
}

BASE_URL = "https://www.commoditymarketlive.com/mandi-price-state/"
FILE_NAME = "India_Master_Mandi_DB.csv"

# Google Drive Folder ID — set as a GitHub Actions secret named DRIVE_FOLDER_ID
DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID', '') 

def clean_currency(col):
    return col.astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False).str.strip().astype(float)

def scrape_all_states():
    all_data = []
    
    # Setup Headless Chrome (Required for Cloud Servers to not crash)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"🚀 Starting National Data Extraction: {datetime.now().strftime('%Y-%m-%d')}")

    for state, slug in STATES.items():
        print(f"Scraping {state}...")
        try:
            driver.get(BASE_URL + slug)
            time.sleep(2)
            
            # Click "Show More" until all data loads
            clicks = 0
            while True:
                try:
                    btn_xpath = "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more')]"
                    btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    driver.execute_script("arguments[0].click();", btn)
                    clicks += 1
                    time.sleep(1.5)
                except:
                    print(f"   ↳ Finished loading {state} after {clicks} clicks.")
                    break # No more buttons
            
            html = driver.page_source
            tables = pd.read_html(StringIO(html))
            
            # Find the core data table
            for df in tables:
                if 'Market' in df.columns:
                    # Clean the state data into API Schema
                    df['state'] = state.lower()
                    df['market'] = df['Market'].str.strip()
                    df['district'] = df['Market'].str.split(' ').str[0].str.strip()
                    df[['commodity', 'variety']] = df['Commodity'].str.split(' - ', n=1, expand=True)
                    df['commodity'] = df['commodity'].str.strip()
                    df['variety'] = df['variety'].fillna('Standard').str.strip()
                    
                    df['modal_price'] = clean_currency(df['Price'])
                    df[['max_price', 'min_price']] = df['High - Low'].str.split('-', expand=True)
                    df['max_price'] = clean_currency(df['max_price'])
                    df['min_price'] = clean_currency(df['min_price'])
                    
                    df['arrival_date'] = df['Date'].str.strip()
                    
                    api_cols = ['state', 'district', 'market', 'commodity', 'variety', 'min_price', 'max_price', 'modal_price', 'arrival_date']
                    all_data.append(df[api_cols])
                    break
        except Exception as e:
            print(f"⚠️ Failed {state}: {e}")
            continue

    driver.quit()
    
    # Merge everything into one massive table
    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df.to_csv(FILE_NAME, index=False)
        print(f"✅ Master Database Compiled. Total Rows: {len(master_df)}")
        return True
    return False

def upload_to_drive():
    print("☁️ Uploading to Google Drive...")
    # Authenticate using the hidden secret key
    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ['GCP_CREDENTIALS']))
    service = build('drive', 'v3', credentials=credentials)
    
    file_metadata = {'name': FILE_NAME, 'parents': [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(FILE_NAME, mimetype='text/csv')
    
    # Uploads the new file to the folder
    service.files.create(body=file_metadata, media_body=media, fields='id').execute()
    print("🎉 SUCCESS! Baseline Master File is now live in your Team's Google Drive.")

if __name__ == "__main__":
    if scrape_all_states():
        upload_to_drive()