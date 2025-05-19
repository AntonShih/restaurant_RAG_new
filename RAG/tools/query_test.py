
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from RAG.core.compare import search_similar_faqs

def load_environment():
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    namespace = os.getenv("PINECONE_NAMESPACE")
    index = Pinecone(api_key=api_key).Index(index_name)
    return index, namespace

if __name__ == "__main__":
    #測試用: python -m RAG.tools.query_test
    index, namespace = load_environment()

    print("\n🤖 FAQ 查詢 CLI 啟動，輸入 exit 離開")
    while True:
        query = input("\n請輸入你的問題：\n> ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        results = search_similar_faqs(query)
        if not results:
            print("❓ 找不到相關資料。")
            continue

        print("\n📝 查詢結果：\n")
        for i, r in enumerate(results, 1):
            meta = r["metadata"]
            print(f"{i}. [{meta.get('category', '未分類')}] {meta.get('question')}")
            print(f"   答：{meta.get('answer')}")
            print(f"   相似度：{round(r['score'], 4)}\n")
