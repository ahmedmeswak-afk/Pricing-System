import os
import json
import gspread
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials

def main():
    try:
        # 1. إعداد الاتصال (يجب أن تكون هذه الأسطر مزاحة للداخل)
        scopes = ["https://googleapis.com", "https://googleapis.com"]
        creds_json = os.environ.get('GOOGLE_CREDS')
        
        if not creds_json:
            print("❌ خطأ: لم يتم العثور على GOOGLE_CREDS")
            return

        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)

        # 2. فتح الجدول ورفع البيانات
        sh = client.open("Construction_Pricing_Dashboard").get_worksheet(0)
        
        # إنشاء بيانات تجريبية للتأكد من العمل
        df = pd.DataFrame({'ID': [1, 2], 'Status': ['Success', 'Active']})
        data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
        
        sh.clear()
        sh.update('A1', data_to_upload)
        print("✅ تم التحديث بنجاح!")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    main()
