# 開發使用用來測search_similar_faqs功能是否正常 ，找前三相似的
from RAG.core.compare import search_similar_faqs
from config.environment import init_openai, get_pinecone_index, get_namespace, init_pinecone

def interactive_mode(index, namespace):
    print("\n🤖 餐飲業 FAQ 助手已啟動，輸入 'exit' 離開\n")
    while True:
        q = input("請輸入問題：\n> ").strip()
        if q.lower() in ["exit", "quit", "bye", "離開"]:
            print("👋 感謝使用，再見！")
            break

        print("\n🔍 搜尋中...")
        results = search_similar_faqs(query=q, index=index, namespace=namespace)

        if not results:
            print("❓ 找不到相關資料，請改用不同方式詢問。\n")
            continue

        print("📝 最相近 FAQ：\n")
        for i, r in enumerate(results, 1):
            meta = r["metadata"]
            print(f"{i}. [{meta.get('category', '未分類')}] {meta.get('question')}\n   答：{meta.get('answer')}\n   相似度：{round(r['score'], 4)}\n")

if __name__ == "__main__":
    # 測試 poetry run python -m RAG.tools.query_loop

        # 初始化
    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()

    # 啟動查詢互動
    interactive_mode(index, namespace)