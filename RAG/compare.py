import openai
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import json

# 載入環境變數與初始化
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
namespace = os.getenv("PINECONE_NAMESPACE")
# namespace 不是「標籤分類」，而是「資料分區」的概念。
# 你可以把它想成：資料庫中的「獨立資料表」，不是資料列中的「欄位」或「標籤」。

def get_embedding(text):
    """
    呼叫 OpenAI API 將輸入文字轉換成向量
    return回來的資料結構
    {"object": "list",
    "data": [{
        "embedding": [0.0123, 0.0042, ..., -0.0019],
        "index": 0,
        "object": "embedding"}],
    "model": "text-embedding-3-small",
    "object": "list",
    "usage": {
    "prompt_tokens": 9,
    "total_tokens": 9}}
    """
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# 檢查openai格式 物件轉json ensure_ascii 保留中文
def print_embedding_response(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))

# 檢查pinecone

def debug_pinecone_response(response):
    print("回傳型別：", type(response))
    print("完整資料內容：\n")
    print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))

   

def search_similar_faqs(query, top_k=3):
    """查詢最相似 FAQ 向量"""
    query_vector = get_embedding(query)
    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    # print(type(result))  # 輸出：<class 'dict'>
    # print(dir(result))  # 看看有哪些屬性與方法

    return result["matches"]


if __name__ == "__main__":
    user_input = input("請輸入你的問題：\n> ")
    results = search_similar_faqs(user_input)
    
    # # print_embedding_response(user_input)
    # query_vector = get_embedding(user_input)
    # full_response = index.query(
    # vector=query_vector,
    # top_k=3,
    # include_metadata=True,
    # namespace=namespace
    # )

    # # 印出完整 Pinecone 回傳資料
    # debug_pinecone_response(full_response)

    print("\n🔍 最相近的 FAQ：\n")
    for i, r in enumerate(results, 1):
        meta = r["metadata"]
        print(f"{i}. [{meta['category']}] {meta['question']}")
        print(f"   答：{meta['answer']}")
        print(f"   相似度：{round(r['score'], 4)}\n")