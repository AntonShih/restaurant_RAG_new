# 如何使用的flex message
import json
from linebot.v3.messaging.models.flex_container import FlexContainer

def load_how_to_use_flex() -> FlexContainer:
    """
    讀取 how_to_use_card.json 並轉換為 FlexContainer。
    """
    try:
        with open("line_bot/templates/how_to_use_card.json", "r", encoding="utf-8") as f:
            raw = json.load(f)
        return FlexContainer.from_dict(raw)
    except Exception as e:
        print(f"❌ 無法載入使用說明卡片：{e}")
        raise


