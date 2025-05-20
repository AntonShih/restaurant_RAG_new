from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
import os

from line_bot.services.user_service import save_user_role, get_user_role
from line_bot.services.auth_state import (
    start_auth, complete_auth, is_auth_pending,
    get_pending_role, increment_attempt
)
from line_bot.config.role_config import ROLE_TEXT_MAP, ROLE_ACCESS_LEVEL

# 初始化 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

def verify_password(role: str, password: str) -> bool:
    expected = os.getenv(f"PASSWORD_{role.upper()}")
    return password == expected

def handle_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

            # Step 1：身份認證流程
        if text.startswith("認證："):
            role = text.replace("認證：", "").strip()
            # ... reverse_map 和白名單驗證略
            start_auth(user_id, role)  # ✅ 改成封裝的
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")]
                )
            )
            return

        # Step 2：密碼驗證
        if is_auth_pending(user_id):  # ✅ 判斷改封裝
            role = get_pending_role(user_id)  # ✅ 拿角色

            if verify_password(role, text):
                save_user_role(user_id, role)
                complete_auth(user_id)  # ✅ 成功後移除
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"✅ 密碼正確，您已成功認證為：{ROLE_TEXT_MAP.get(role, role)}")]
                    )
                )
            else:
                attempts = increment_attempt(user_id)  # ✅ 嘗試次數封裝
                remaining = 3 - attempts

                if attempts >= 3:
                    complete_auth(user_id)  # ✅ 清除失敗者
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text="❌ 已連續輸入錯誤 3 次，已幫您轉換為QA回答模式。若想請重新驗證請選擇角色。")]
                        )
                    )
                else:
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=f"❌ 密碼錯誤，請重新輸入。您還有 {remaining} 次機會")]
                        )
                    )
            return