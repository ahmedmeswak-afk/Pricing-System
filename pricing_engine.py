import os, json, gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    try:
        # 1. الاتصال بجوجل
        scopes = ["https://google.com", "https://googleapis.com"]
        creds_dict = json.loads(os.environ.get('GOOGLE_CREDS'))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
        client = gspread.authorize(creds)

        # 2. فتح الجدول وتحديثه
        sh = client.open("Construction_Pricing_Dashboard").get_worksheet(0)
        sh.clear()
        # كتابة سطر تجريبي للتأكد من الاتصال
        sh.update('A1', [['✅ نجاح! النظام يعمل بنجاح']])
        print("✅ تم تحديث الجدول بنجاح!")
    except Exception as e:
        print(f"❌ الخطأ هو: {e}")
        raise e

if __name__ == "__main__":
    main()
