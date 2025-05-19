from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
import os

from line_bot.services.user_service import save_user_role, get_user_role
from line_bot.services.auth_state import pending_password_check
from RAG.query.query_engine_safe import answer_query_secure
from line_bot.config.role_config import ROLE_TEXT_MAP, ROLE_ACCESS_LEVEL

# 初始化 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

def handle_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # Step 1：身份認證流程
        if text.startswith("認證："):
            role = text.replace("認證：", "").strip()

            # 可選：支援中文轉英文 role
            reverse_map = {v: k for k, v in ROLE_TEXT_MAP.items()}
            if role in reverse_map:
                role = reverse_map[role]

            # 白名單驗證
            if role not in ROLE_ACCESS_LEVEL:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="❌ 無效的身份，請重新選擇正確角色。")]
                    )
                )
                return

            # ✅ 初始化使用者認證狀態（role + attempts）
            pending_password_check[user_id] = {
                "role": role,
                "attempts": 0
            }

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")]
                )
            )
            return

        # Step 2：正在進行密碼認證
        if user_id in pending_password_check:
            role_info = pending_password_check[user_id]

            # 🛡 保險：如果格式是舊版字串，自動轉新格式
            if isinstance(role_info, str):
                role_info = {
                    "role": role_info,
                    "attempts": 0
                }
                pending_password_check[user_id] = role_info

            role = role_info["role"]
            expected_password = os.getenv(f"PASSWORD_{role.upper()}")

            if text == expected_password:
                save_user_role(user_id, role)
                del pending_password_check[user_id]

                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"✅ 密碼正確，您已成功認證為：{ROLE_TEXT_MAP.get(role, role)}")]
                    )
                )
            else:
                role_info["attempts"] += 1
                remaining = 3 - role_info["attempts"]

                if role_info["attempts"] >= 3:
                    del pending_password_check[user_id]
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

        # Step 3：進行 RAG 查詢
        try:
            response = answer_query_secure(text, user_id)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=str(response).strip())]
                )
            )
        except Exception as e:
            print("❌ GPT 查詢失敗：", str(e))
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="⚠️ 查詢時發生錯誤，請稍後再試。")]
                )
            )
