# TODO: 後續將 openai 相關邏輯移至 adapter

import logging
from core.compare import compare_vectors
import openai

logger = logging.getLogger(__name__)

def get_top_k_matches(query: str, index, namespace: str, embedding_func, top_k: int = 3) -> list[dict]:
    """
    輸入純文字自動轉向量，取得語意最相近的 Top-K 答案（使用外部注入的 embedding function）
    """
    query_vector = embedding_func(query)
    return compare_vectors(query_vector, index, namespace, top_k)

def filter_by_permission(matches: list[dict], user_level: int, filter_func) -> list[dict]:
    """
    用職等過濾答案（使用外部注入的過濾邏輯）
    """
    return filter_func(matches, user_level)

def generate_judged_answer(query: str, filtered_matches: list[dict]) -> str:
    """
    根據匹配結果讓 GPT 回覆，並列印 debug 訊息
    """
    context = "\n".join(
        f"{i}. 問題: {m['metadata']['question']}\n   回答: {m['metadata']['answer']}"
        for i, m in enumerate(filtered_matches, 1)
    )

    logger.debug("\n📋 [DEBUG] 最終可用 FAQ：\n%s", context)

    messages = [
        {
            "role": "system",
            "content": (
                "你是一位餐飲 FAQ 助理。\n"
                "請依照以下流程處理使用者的問題：\n"
                "\n"
                "Step 1：閱讀以下 FAQ，判斷是否可以根據內容回答。\n"
                "- 若 FAQ 中的語意可清楚支撐回答，即使文字不完全相同，也可進行回覆。\n"
                "- 回答僅限於 FAQ 所涵蓋的內容，禁止引入額外常識。\n"
                "- 若確實無資料可參考，請回：「目前無法提供準確答案」。\n"
                "\n"
                "Step 2：若 FAQ 可回應，請確認該問題是否屬於餐飲業常見工作或行政工作處理範疇。\n"
                "- 若都不是，請回：「這不是我能處理的範疇哦～」。\n"
                "\n"
                "⚠️ 禁止使用任何非 FAQ 的知識。即使你知道正確答案，只要 FAQ 沒寫，也不能說。\n"
                "❌ 不得加入結語，不得說額外關心「歡迎再次提問」、「有其他問題請詢問」「希望可以幫你解決問題」等句子。"
            )
        },
        {
            "role": "user",
            "content": f"使用者問：「{query}」\n以下是他有權限查閱的 FAQ：\n{context}"
        }
    ]

    logger.debug("\n📤 [DEBUG] 傳送給 GPT 的 Prompt：\n%s\n%s", messages[0]["content"], messages[1]["content"])

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
        temperature=0.1
    )

    reply = completion.choices[0].message.content.strip()
    logger.debug("\n🧾 [DEBUG] GPT 回覆內容：\n%s\n--------------------", reply)
    return reply
