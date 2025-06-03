# rich menu 搭建
from dotenv import load_dotenv
import os
from PIL import Image
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, MessagingApiBlob,
    RichMenuRequest, RichMenuSize, RichMenuArea,
    RichMenuBounds,PostbackAction
)

# 讀取 .env
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初始化 LINE SDK
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# 圖片路徑
ORIGINAL_IMAGE_PATH = "tools/line_bot_tools/rich_menu1.png"
COMPRESSED_IMAGE_PATH = "tools/line_bot_tools/richmenu1.jpg"


def compress_rich_menu_image(input_path=ORIGINAL_IMAGE_PATH, output_path=COMPRESSED_IMAGE_PATH, quality=85):
    if not os.path.exists(input_path):
        print(f"❌ 找不到原始圖片：{input_path}")
        return False

    target_width, target_height = 2500, 1686
    img = Image.open(input_path).convert("RGB")

    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    # 等比放大並裁切至 2500x1686
    if img_ratio > target_ratio:
        new_height = target_height
        new_width = int(new_height * img_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / img_ratio)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    img_cropped = img_resized.crop((left, top, right, bottom))

    img_cropped.save(output_path, format="JPEG", optimize=True, quality=quality)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ 圖片已等比例放大並裁切為 {target_width}×{target_height}，大小約 {int(size_kb)} KB，儲存為 {output_path}")
    
    if size_kb > 1024:
        print("⚠️ 圖片超過 1MB，可能會被 LINE 拒絕，建議壓縮品質調低至 80 或更小。")
    
    return True


def create_rich_menu():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        blob_api = MessagingApiBlob(api_client)

        areas = [
            RichMenuArea(bounds=RichMenuBounds(x=0, y=0, width=833, height=843), action=PostbackAction(label="認證一般員工", data="role:normal")),
            RichMenuArea(bounds=RichMenuBounds(x=834, y=0, width=833, height=843), action=PostbackAction(label="認證儲備幹部", data="role:reserve")),
            RichMenuArea(bounds=RichMenuBounds(x=1667, y=0, width=833, height=843), action=PostbackAction(label="認證組長", data="role:leader")),
            RichMenuArea(bounds=RichMenuBounds(x=0, y=843, width=833, height=843), action=PostbackAction(label="認證副店長", data="role:vice_manager")),
            RichMenuArea(bounds=RichMenuBounds(x=834, y=843, width=833, height=843), action=PostbackAction(label="認證店長", data="role:manager")),
            RichMenuArea(bounds=RichMenuBounds(x=1667, y=843, width=833, height=843), action=PostbackAction(label="我要查詢", data="action:how_to_use"))
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

        # 上傳圖片，包 try-except
        try:
            with open(COMPRESSED_IMAGE_PATH, 'rb') as image_file:
                blob_api.set_rich_menu_image(
                    rich_menu_id=rich_menu_id,
                    body=bytearray(image_file.read()),
                    _headers={'Content-Type': 'image/jpeg'}
                )
            print("✅ 圖片已上傳")
        except Exception as e:
            print("❌ 圖片上傳失敗：", e)
            return

        # 設為預設 RichMenu
        try:
            line_bot_api.set_default_rich_menu(rich_menu_id)
            print("✅ 已設為預設 RichMenu")
        except Exception as e:
            print("⚠️ 設定預設 RichMenu 失敗：", e)


if __name__ == "__main__":
    if compress_rich_menu_image():
        create_rich_menu()

