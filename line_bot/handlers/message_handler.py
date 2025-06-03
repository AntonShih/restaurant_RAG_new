# 處理handle_message 資訊 1.驗證身分流程 2.若在DB中找到身分則可以開始進行RAG查詢
from services.auth_service import AuthService
from adapters.user_role_adapter import get_user_role
from linebot.v3.messaging import TextMessage, ReplyMessageRequest,PushMessageRequest
from services.query_service import handle_secure_query

def handle_message(event, line_bot_api, index, namespace):
    user_id = event.source.user_id
    text = event.message.text.strip()

    # 認證流程處理
    if AuthService(user_id, text, line_bot_api, event).process():
        return
    
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text="📚 FAQ 匹配中，請稍候...")]
        )
    )

    # 進入 RAG 查詢流程
    user = get_user_role(user_id)
    if user:
        try:
            rag_answer = handle_secure_query(text, user, index, namespace)
        except Exception as e:
            print("❌ RAG 查詢失敗：", str(e))
            rag_answer = "❌ 回答時發生錯誤，請稍後再試。"
    else:
        rag_answer = "⚠️ 查無使用者身份資訊，請先完成認證。"

    line_bot_api.push_message(
    PushMessageRequest(
        to=user_id,
        messages=[TextMessage(text=rag_answer)]
    )
)
