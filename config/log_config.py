import os
import logging

def init_logging(level=logging.INFO, to_file=False, file_name="app.log"):
    # 以下保留你原本的 log 設定程式碼
    handlers = [logging.StreamHandler()]
    if to_file:
        handlers.append(logging.FileHandler(file_name))

    logging.basicConfig(
        level=logging.WARNING,  # 預設全域為 WARNING，模組再另外開
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=handlers
    )

    # 可動態設定指定模組的 log 等級
    target_module = os.getenv("LOG_TARGET_MODULE")
    if target_module:
        logging.getLogger(target_module).setLevel(level)

    # 壓低雜訊套件
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.INFO)

