import os, json, pandas as pd, numpy as np, gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    # 1. بناء البيانات
    data = []
    for i in range(1, 1001):
        price = np.random.randint(100, 5000)
        data.append([f"ITM-{i:04d}", "بند مقاولات", f"وصف {i}", price, round(price*1.15, 2)])
    df = pd.DataFrame(data, columns=["الكود", "القسم", "الوصف", "السعر", "الإجمالي"])

    # 2. التحديث لـ Google Sheets
    scope = ["https://google.com", "https://googleapis.com"]
    creds_dict = json.loads(os.environ['GOOGLE_CREDS'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sh = client.open("Construction_Pricing_Dashboard").get_worksheet(0)
    sh.clear()
    sh.update([df.columns.values.tolist()] + df.values.tolist())
    print("✅ تم التحديث بنجاح!")

if __name__ == "__main__":
    main()
