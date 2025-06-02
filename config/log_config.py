import os
import logging

def init_logging(level=logging.INFO, to_file=False, file_name="app.log"):
    """
    初始化全域 logging 設定
    - level: 日誌等級（預設 INFO，可設為 DEBUG）
    - to_file: 是否輸出到檔案
    - file_name: log 檔案名稱（預設 app.log）
    """
    handlers = [logging.StreamHandler()]
    if to_file:
        handlers.append(logging.FileHandler(file_name, encoding="utf-8"))

    logging.basicConfig(
        level=level,  # ✅ 改為使用傳入參數，不再寫死 WARNING
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=handlers
    )

    # ✅ 動態指定模組等級（例如 LOG_TARGET_MODULE=services.query_service）
    target_module = os.getenv("LOG_TARGET_MODULE")
    if target_module:
        logging.getLogger(target_module).setLevel(level)
        print(f"✅ Logging 已啟用 DEBUG 模組：{target_module}")

    # 壓制常見雜訊套件
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.INFO)

    logging.info("✅ Logging 系統初始化完成")
