import os
import json
import sys
from dotenv import load_dotenv
from argparse import ArgumentParser

from RAG.core.embedding import embed_faq_list_batch, load_api_key
from RAG.core.formatting import format_for_pinecone
from RAG.core.compare import search_similar_faqs
from pinecone import Pinecone


def load_environment():
    """載入環境變數與初始化 API"""
    load_dotenv()
    load_api_key()

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    namespace = os.getenv("PINECONE_NAMESPACE")

    try:
        index = Pinecone(api_key=api_key).Index(index_name)
        print(f"✅ 成功連接到 Pinecone 索引: {index_name}")
        return index, namespace
    except Exception as e:
        print(f"❌ 連接 Pinecone 失敗: {str(e)}")
        sys.exit(1)


def process_faq_file(path="data/sop.json"):
    """讀取 JSON FAQ 檔案並去重，資料清洗"""
    full_path = os.path.abspath(os.path.join(os.getcwd(), path))

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            raw_faqs = json.load(f)
    except Exception as e:
        print(f"❌ 無法讀取檔案 {full_path}: {e}")
        return []

    seen = set()
    result = []
    for faq in raw_faqs:
        q = faq.get("question")
        if q and q not in seen:
            seen.add(q)
            result.append(faq)

    print(f"📊 共讀取 {len(raw_faqs)} 筆，去重後剩 {len(result)} 筆 FAQ")
    return result


def get_existing_vector_info(index, namespace):
    """使用 fetch API 擷取目前所有向量 ID 與對應問題"""
    existing_ids, existing_questions = set(), set()

    try:
        stats = index.describe_index_stats()
        count = stats.get("namespaces", {}).get(namespace, {}).get("vector_count")
        if count == 0:
            return existing_ids, existing_questions

        fetch_ids = [f"faq_{i+1}" for i in range(count)]
        fetched = index.fetch(ids=fetch_ids, namespace=namespace)

        for vector_id, record in fetched.vectors.items():
            existing_ids.add(vector_id)
            metadata = record.metadata
            if metadata and "question" in metadata:
                existing_questions.add(metadata["question"])

    except Exception as e:
        print(f"❌ 使用 fetch 取得向量資訊失敗：{e}")

    return existing_ids, existing_questions



def upload_to_vector_db(index, faqs, namespace, batch_size=100):
    print("🔍 檢查向量資料庫...")
    existing_ids, existing_questions = get_existing_vector_info(index, namespace)
    vectors = format_for_pinecone(faqs)

    new_vectors = [v for v in vectors if v["id"] not in existing_ids and v["metadata"]["question"] not in existing_questions]
    print(f"📦 過濾後剩 {len(new_vectors)}/{len(vectors)} 筆向量要上傳")

    if not new_vectors:
        print("⚠️ 沒有新資料需要上傳")
        return True

    try:
        for i in range(0, len(new_vectors), batch_size):
            batch = new_vectors[i:i + batch_size]
            index.upsert(vectors=batch, namespace=namespace)
        print("✅ 向量上傳完成")
        return True
    except Exception as e:
        print(f"❌ 上傳失敗：{e}")
        return False


def interactive_mode(index, namespace):
    print("\n🤖 餐飲業 FAQ 助手已啟動，輸入 'exit' 離開\n")
    while True:
        q = input("請輸入問題：\n> ").strip()
        if q.lower() in ["exit", "quit", "bye", "離開"]:
            print("👋 感謝使用，再見！")
            break

        print("\n🔍 搜尋中...")
        results = search_similar_faqs(query=q)

        if not results:
            print("❓ 找不到相關資料，請改用不同方式詢問。\n")
            continue

        print("📝 最相近 FAQ：\n")
        for i, r in enumerate(results, 1):
            meta = r["metadata"]
            print(f"{i}. [{meta.get('category', '未分類')}] {meta.get('question')}\n   答：{meta.get('answer')}\n   相似度：{round(r['score'], 4)}\n")


def main():
    parser = ArgumentParser()
    parser.add_argument("--upload", action="store_true", help="是否重新上傳 FAQ")
    parser.add_argument("--path", type=str, default="data/sop.json", help="FAQ JSON 檔案路徑")
    args = parser.parse_args()

    print("🚀 餐飲業 FAQ RAG 系統啟動中...")
    index, namespace = load_environment()

    if args.upload:
        faqs = process_faq_file(args.path)
        if not faqs:
            print("❌ 無 FAQ 資料，程序中止")
            return

        print("🔍 檢查向量資料庫是否已有相同問題...")
        existing_ids, existing_questions = get_existing_vector_info(index, namespace)

        # 過濾出新問題（避免浪費 OpenAI embedding）
        new_faqs = [f for f in faqs if f["question"] not in existing_questions]
        print(f"🆕 共發現 {len(new_faqs)} 筆新問題（將送入 OpenAI 嵌入）")

        if not new_faqs:
            print("⚠️ 無需嵌入，所有資料皆已存在")
        else:
            print("🧠 正在生成向量嵌入...")
            embedded = embed_faq_list_batch(new_faqs)
            embedded = [f for f in embedded if "embedding" in f]

            if not upload_to_vector_db(index, embedded, namespace):
                print("❌ 上傳失敗")
                return
    else:
        interactive_mode(index, namespace)


if __name__ == "__main__":
    main()
