import openai
from RAG.core.compare import search_similar_faqs
from line_bot.services.user_service import get_user_role
from config.environment import init_openai,get_pinecone_index,get_namespace,init_pinecone

import logging
logger = logging.getLogger(__name__)

def answer_query_secure(query: str, user_id: str, index, namespace):
    
    """安全版查詢：查 top3，權限過濾後交由 LLM 判斷"""
    user = get_user_role(user_id)
    user_level = user.get("access_level", 0) if user else 0

    #查top3有沒有符合權限可看內容 留下可看的
    matches = search_similar_faqs(query, index, namespace, top_k=3)
    filtered_matches = [m for m in matches if m["metadata"].get("access_level") <= user_level]

    logger.info(f"使用者 {user_id} 查詢：{query}")
    logger.debug(f"原始比對筆數：{len(matches)}；權限內筆數：{len(filtered_matches)}")

    if not filtered_matches:
        logger.warning(f"使用者 {user_id} 無法查詢權限內 FAQ")
        return "⚠️ 您的職等無法查閱資料，請洽詢管理者"

    return generate_judged_answer(query, filtered_matches)


def generate_judged_answer(query, filtered_matches):
    """請 LLM 根據過濾後的內容生成回覆或拒答
    
    ⚠️ 回傳格式（openai.chat.completions.create）：
    {
        "id": "...",
        "object": "chat.completion",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "您好，歡迎光臨本餐廳！"
                }
            }
        ],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150
        }
    }
    
    """
    context = ""
    # 這邊的1是enumerate從1號開始context只給他問題跟答案而已，語意完整
    for i, m in enumerate(filtered_matches, 1):
        meta = m["metadata"]
        context += f"{i}. 問題: {meta['question']}\n   回答: {meta['answer']}\n"

    print("\n📋 [DEBUG] 最終可用 FAQ：")
    print(context)

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

    print("\n📤 [DEBUG] 傳送給 GPT 的 Prompt：")
    print(messages[0]["content"])
    print(messages[1]["content"])

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
        temperature=0.1
    )

    reply = completion.choices[0].message.content.strip()
    
    print("\n🧾 [DEBUG] GPT 回覆內容：")
    print(reply)
    print("--------------------\n")

    return reply

if __name__ == "__main__":
    # 測試 poetry run python -m RAG.query.query_engine_safe

    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()

    # 手動測試區：輸入問題與使用者 ID 來模擬查詢流程
    query = input("請輸入你要查詢的問題：\n> ")
    user_id = input("請輸入模擬的使用者 ID：\n> ")

    answer = answer_query_secure(query, user_id, index, namespace)
    
    print("\n💬 最終回覆內容：")
    print(answer)

# -----------------------------------------------------------------------
# async

# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from RAG.core.compare import search_similar_faqs
# from openai import AsyncOpenAI
# from pinecone import Pinecone
# from line_bot.services.user_service import get_user_role

# client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# async def answer_query_secure(query, user_id):
#     pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
#     index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
#     namespace = os.getenv("PINECONE_NAMESPACE")

#     user = get_user_role(user_id)
#     user_level = user.get("access_level", 0) if user else 0

#     matches = search_similar_faqs(query, index, namespace, top_k=3)
#     filtered_matches = [m for m in matches if m["metadata"].get("access_level") <= user_level]

#     print("🔍 [DEBUG] 使用者問題：", query)
#     print("👤 [DEBUG] 使用者 ID：", user_id, "職等等級：", user_level)

#     print("📥 Top3 FAQ:")
#     for m in matches:
#         meta = m["metadata"]
#         print(f" - ({meta.get('access_level')}) {meta['question']}")

#     print("🔒 Filtered FAQ（符合職等）:")
#     for m in filtered_matches:
#         meta = m["metadata"]
#         print(f" ✅ ({meta.get('access_level')}) {meta['question']}")

#     if not filtered_matches:
#         return "⚠️ 抱歉，您目前的職等無法查閱相關資料，請洽詢上級或管理者。"

#     return await generate_judged_answer(query, filtered_matches)


# def get_embedding(query):
#     # TODO: 改為實際嵌入邏輯，如 OpenAI Embedding
#     return [0.1] * 1536


# async def generate_judged_answer(query, filtered_matches):
#     context = ""
#     for i, m in enumerate(filtered_matches, 1):
#         meta = m["metadata"]
#         context += f"{i}. 問題: {meta['question']}\n   回答: {meta['answer']}\n"

#     print("\n📋 [DEBUG] 最終可用 FAQ：")
#     print(context)

#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "你是一位餐飲 FAQ 助理。\n"
#                 "請依照以下流程處理使用者的問題：\n"
#                 "\n"
#                 "Step 1：閱讀以下 FAQ，判斷是否可以根據內容回答。\n"
#                 "- 若 FAQ 中的語意可清楚支撐回答，即使文字不完全相同，也可進行回覆。\n"
#                 "- 回答僅限於 FAQ 所涵蓋的內容，禁止引入額外常識。\n"
#                 "- 若確實無資料可參考，請回：「目前無法提供準確答案」。\n"
#                 "\n"
#                 "Step 2：若 FAQ 可回應，請確認該問題是否屬於餐飲業常見工作或行政工作處理範疇。\n"
#                 "- 若都不是，請回：「這不是我能處理的範疇哦～」。\n"
#                 "\n"
#                 "⚠️ 禁止使用任何非 FAQ 的知識。即使你知道正確答案，只要 FAQ 沒寫，也不能說。\n"
#                 "❌ 不得加入結語，不得說額外關心「歡迎再次提問」、「有其他問題請詢問」「希望可以幫你解決問題」等句子。"
#             )
#         },
#         {
#             "role": "user",
#             "content": f"使用者問：「{query}」\n以下是他有權限查閱的 FAQ：\n{context}"
#         }
#     ]

#     print("\n📤 [DEBUG] 傳送給 GPT 的 Prompt：")
#     print(messages[0]["content"])
#     print(messages[1]["content"])

#     try:
#         completion = await client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             max_tokens=300,
#             temperature=0.1
#         )
#         reply = completion.choices[0].message.content.strip()
#     except Exception as e:
#         print("❌ GPT 呼叫失敗：", str(e))
#         return "❌ 回答時發生錯誤，請稍後再試。"

#     print("\n🧾 [DEBUG] GPT 回覆內容：")
#     print(reply)
#     print("--------------------\n")

#     return reply


# if __name__ == "__main__":
#     import asyncio

#     async def test():
#         query = input("請輸入你要查詢的問題：\n> ")
#         user_id = input("請輸入模擬的使用者 ID：\n> ")
#         answer = await answer_query_secure(query, user_id)
#         print("\n💬 最終回覆內容：")
#         print(answer)

#     asyncio.run(test())

