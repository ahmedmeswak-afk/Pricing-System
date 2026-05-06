import os
import json
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    try:
        print("🚀 بدء عملية تحديث البيانات...")
        
        # 1. تجهيز بيانات تجريبية (100 بند لضمان السرعة والنجاح)
        data = []
        for i in range(1, 101):
            price = np.random.randint(500, 5000)
            data.append([
                f"ITM-{i:03d}", 
                "أعمال إنشائية وتوريد", 
                f"بند توريد رقم {i} - فئة أ", 
                price, 
                round(price * 1.15, 2)
            ])
        
        df = pd.DataFrame(data, columns=["الكود", "القسم", "الوصف", "السعر الأساسي", "الإجمالي شامل الضريبة"])

        # 2. إعداد الاتصال بجوجل (إضافة تصريح Google Drive الضروري)
        # تم دمج النطاقات لضمان رؤية الملف وتعديله
        scopes = [
            "https://google.com",
            "https://googleapis.com"
        ]
        
        # جلب المفتاح المشفر من GitHub Secrets
        creds_json = os.environ.get('GOOGLE_CREDS')
        if not creds_json:
            raise ValueError("❌ خطأ: لم يتم العثور على GOOGLE_CREDS في GitHub Secrets")
            
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
        client = gspread.authorize(creds)

        # 3. فتح الجدول وتحديثه
        # ملاحظة: تأكد أن اسم الجدول في جوجل هو Construction_Pricing_Dashboard
        spreadsheet_name = "Construction_Pricing_Dashboard"
        sh = client.open(spreadsheet_name).get_worksheet(0)
        
        # مسح البيانات القديمة وكتابة الجديدة
        sh.clear()
        sh.update([df.columns.values.tolist()] + df.values.tolist())
        
        print(f"✅ تم التحديث بنجاح! تم رفع {len(df)} بند إلى الجدول.")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التنفيذ: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
