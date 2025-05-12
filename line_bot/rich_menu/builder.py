from dotenv import load_dotenv
import os
from PIL import Image
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, MessagingApiBlob,
    RichMenuRequest, RichMenuSize, RichMenuArea,
    RichMenuBounds, MessageAction
)

# 讀取 .env
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# LINE SDK 初始化
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# 圖片路徑
ORIGINAL_IMAGE_PATH = "line_bot/rich_menu/rich_menu.png"
COMPRESSED_IMAGE_PATH = "richmenu.jpg"

# 壓縮圖片函式
def compress_rich_menu_image(input_path=ORIGINAL_IMAGE_PATH, output_path=COMPRESSED_IMAGE_PATH, quality=85):
    if not os.path.exists(input_path):
        print(f"❌ 找不到原始圖片：{input_path}")
        return False

    img = Image.open(input_path).convert("RGB")
    img.save(output_path, format="JPEG", optimize=True, quality=quality)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ 圖片已壓縮為 {int(size_kb)} KB，儲存為 {output_path}")
    return True

# 建立 Rich Menu 函式
def create_rich_menu():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        blob_api = MessagingApiBlob(api_client)

        areas = [
            RichMenuArea(bounds=RichMenuBounds(x=0, y=0, width=833, height=843), action=MessageAction(text="認證：normal")),
            RichMenuArea(bounds=RichMenuBounds(x=834, y=0, width=833, height=843), action=MessageAction(text="認證：reserve")),
            RichMenuArea(bounds=RichMenuBounds(x=1667, y=0, width=833, height=843), action=MessageAction(text="認證：leader")),
            RichMenuArea(bounds=RichMenuBounds(x=0, y=843, width=833, height=843), action=MessageAction(text="認證：vice_manager")),
            RichMenuArea(bounds=RichMenuBounds(x=834, y=843, width=833, height=843), action=MessageAction(text="認證：manager")),
            RichMenuArea(bounds=RichMenuBounds(x=1667, y=843, width=833, height=843), action=MessageAction(text="我要查詢"))
        ]

        rich_menu = RichMenuRequest(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="六宮格選單",
            chat_bar_text="點我展開功能選單",
            areas=areas
        )

        # 建立 Rich Menu
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu).rich_menu_id
        print(f"✅ 成功建立 RichMenu：{rich_menu_id}")

        # 上傳壓縮後圖片
        if os.path.exists(COMPRESSED_IMAGE_PATH):
            with open(COMPRESSED_IMAGE_PATH, 'rb') as image_file:
                blob_api.set_rich_menu_image(
                    rich_menu_id=rich_menu_id,
                    body=bytearray(image_file.read()),
                    _headers={'Content-Type': 'image/jpeg'}
                )
            print("✅ 圖片已上傳")
        else:
            print(f"⚠️ 找不到壓縮後圖片：{COMPRESSED_IMAGE_PATH}")
            return

        # 設定為預設
        line_bot_api.set_default_rich_menu(rich_menu_id)
        print("✅ 已設為預設 RichMenu")


if __name__ == "__main__":
    if compress_rich_menu_image():
        create_rich_menu()
