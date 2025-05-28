# conftest.py 是 pytest 的「自動加載設定檔」，可以用來定義所有測試都會用到的設定、資料夾初始化、fixture。
from dotenv import load_dotenv

load_dotenv()
