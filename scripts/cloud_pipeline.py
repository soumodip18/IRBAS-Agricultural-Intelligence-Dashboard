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
import json
import os
from datetime import datetime
from io import StringIO

# ==========================================
# 1. CONFIGURATION: ALL 30 STATES & TARGET FILE
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

BASE_URL      = "https://www.commoditymarketlive.com/mandi-price-state/"
FILE_NAME     = "India_Master_Mandi_DB.csv"
EXISTING_FILE_ID = "1m2yakFq4PMgDfl_aaCIBT2LS6rSLxoXO"  # target Drive file to overwrite

def clean_currency(col):
    return col.astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False).str.strip().astype(float)

def scrape_all_states():
    all_data = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=chrome_options)

    print(f"🚀 Starting National Data Extraction: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for state, slug in STATES.items():
        print(f"Scraping {state}...")
        try:
            driver.get(BASE_URL + slug)
            time.sleep(2)

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
                    break

            html    = driver.page_source
            tables  = pd.read_html(StringIO(html))

            for df in tables:
                if 'Market' in df.columns:
                    df['state']    = state.lower()
                    df['market']   = df['Market'].str.strip()
                    df['district'] = df['Market'].str.split(' ').str[0].str.strip()
                    df[['commodity', 'variety']] = df['Commodity'].str.split(' - ', n=1, expand=True)
                    df['commodity'] = df['commodity'].str.strip()
                    df['variety']   = df['variety'].fillna('Standard').str.strip()

                    df['modal_price'] = clean_currency(df['Price'])
                    df[['max_price', 'min_price']] = df['High - Low'].str.split('-', expand=True)
                    df['max_price'] = clean_currency(df['max_price'])
                    df['min_price'] = clean_currency(df['min_price'])

                    df['arrival_date'] = df['Date'].str.strip()

                    api_cols = ['state', 'district', 'market', 'commodity', 'variety',
                                'min_price', 'max_price', 'modal_price', 'arrival_date']
                    all_data.append(df[api_cols])
                    break

        except Exception as e:
            print(f"⚠️ Failed {state}: {e}")
            continue

    driver.quit()

    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df.to_csv(FILE_NAME, index=False)
        print(f"✅ Master Database Compiled. Total Rows: {len(master_df)}")
        return True
    return False

def upload_to_drive():
    print("☁️ Uploading to Google Drive...")
    try:
        creds_json = os.environ.get('GCP_CREDENTIALS')
        if not creds_json:
            print("❌ ERROR: GCP_CREDENTIALS environment variable is empty or not found.")
            return

        # ✅ json.loads() — safe replacement for eval()
        credentials_info = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        drive_service = build('drive', 'v3', credentials=credentials)

        media = MediaFileUpload(FILE_NAME, mimetype='text/csv')
        print(f"📡 Overwriting destination file ID: {EXISTING_FILE_ID}")

        uploaded_file = drive_service.files().update(
            fileId=EXISTING_FILE_ID,
            media_body=media,
            fields='id'
        ).execute()

        print(f"🎉 SUCCESS! Dataset updated. File ID: {uploaded_file.get('id')}")

    except Exception as e:
        print(f"❌ UPLOAD FAILED: {str(e)}")
        raise e

if __name__ == "__main__":
    print("Script started")
    if scrape_all_states():
        upload_to_drive()
