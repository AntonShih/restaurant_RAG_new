# line_bot/routers/message.py

from services.auth_service import AuthService
# from services.rag_service import RagService  # 假設你也有封裝查詢邏輯
from adapters.user_role_adapter import get_user_role
from linebot.v3.messaging import TextMessage, ReplyMessageRequest
from RAG.query.query_engine_safe import answer_query_secure

def handle_message(event, line_bot_api, index, namespace):
    user_id = event.source.user_id
    text = event.message.text.strip()

    # 認證流程處理
    if AuthService(user_id, text, line_bot_api, event).process():
        return

    # 進入 RAG 查詢流程
    user = get_user_role(user_id)
    if user:
        try:
            rag_answer = answer_query_secure(text, user_id, index, namespace)
        except Exception as e:
            print("❌ RAG 查詢失敗：", str(e))
            rag_answer = "❌ 回答時發生錯誤，請稍後再試。"
    else:
        rag_answer = "⚠️ 查無使用者身份資訊，請先完成認證。"

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=rag_answer)],
        )
    )

