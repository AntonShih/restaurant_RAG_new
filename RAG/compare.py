import openai
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# 載入環境變數與初始化
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
namespace = os.getenv("PINECONE_NAMESPACE", "default")
# namespace 不是「標籤分類」，而是「資料分區」的概念。
# 你可以把它想成：資料庫中的「獨立資料表」，不是資料列中的「欄位」或「標籤」。

def get_embedding(text):
    """呼叫 OpenAI API 將輸入文字轉換成向量"""
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def search_similar_faqs(query, top_k=3):
    """查詢最相似 FAQ 向量"""
    query_vector = get_embedding(query)
    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    return result["matches"]


if __name__ == "__main__":
    user_input = input("請輸入你的問題：\n> ")
    results = search_similar_faqs(user_input)

    print("\n🔍 最相近的 FAQ：\n")
    for i, r in enumerate(results, 1):
        meta = r["metadata"]
        print(f"{i}. [{meta['category']}] {meta['question']}")
        print(f"   答：{meta['answer']}")
        print(f"   相似度：{round(r['score'], 4)}\n")
