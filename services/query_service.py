# rag主流程控制
import logging
from core.query_logic import get_top_k_matches, filter_by_permission, generate_judged_answer
from adapters.openai_adapter import get_embedding
from adapters.pinecone_adapter import filter_matches_by_role

logger = logging.getLogger(__name__)

def handle_secure_query(query: str, user: dict, index, namespace) -> str:
    """
    主流程：查詢 → 比對 → 過濾 → 生成回答
    """
    user_id = user.get("user_id", "<unknown>")
    user_level = user.get("access_level")

    matches = get_top_k_matches(query, index, namespace, embedding_func=get_embedding)
    filtered = filter_by_permission(matches, user_level, filter_func=filter_matches_by_role)

    logger.info(f"🔍 使用者 {user_id} 查詢：「{query}」")
    logger.debug(f"🎯 原始比對筆數：{len(matches)}，通過權限過濾：{len(filtered)}")

    if not filtered:
        logger.warning(f"⛔ 使用者 {user_id} 無法查詢任何權限內 FAQ")
        return "⚠️ 您的職等無法查閱資料，請洽詢管理者"

    return generate_judged_answer(query, filtered)
