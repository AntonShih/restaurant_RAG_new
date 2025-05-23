import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from core.embedding import embed_faq_list_batch
from RAG.core.formatting import format_for_pinecone
from RAG.core.pinecone_checker import get_existing_vector_info
from pinecone import Pinecone

def load_environment():
    load_dotenv()
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
    full_path = os.path.abspath(path)
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

def upload_to_vector_db(index, faqs, namespace, batch_size=100):
    print("🔍 檢查向量資料庫...")
    existing_ids, existing_questions = get_existing_vector_info(index, namespace)

    vectors = format_for_pinecone(faqs)
    new_vectors = []

    for v in vectors:
        if v["metadata"]["question"] not in existing_questions:
            new_vectors.append(v)

    print(f"📦 過濾後剩下 {len(new_vectors)}/{len(vectors)} 筆向量要上傳")

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

if __name__ == "__main__":
    index, namespace = load_environment()

    # 1. 載入本地 FAQ json
    faqs = process_faq_file()

    if not faqs:
        print("❌ 無 FAQ 資料可處理")
        sys.exit(1)

    # 2. 查詢向量資料庫中已存在的 question
    existing_ids, existing_questions = get_existing_vector_info(index, namespace)

    # 3. 過濾重複問題
    new_faqs = [f for f in faqs if f["question"] not in existing_questions]
    print(f"🆕 共發現 {len(new_faqs)} 筆新問題需嵌入")

    if not new_faqs:
        print("⚠️ 所有 FAQ 已存在，無需嵌入")
        sys.exit(0)

    # 4. 執行嵌入
    print("🧠 正在生成向量嵌入...")
    embedded = embed_faq_list_batch(new_faqs)
    embedded = [f for f in embedded if "embedding" in f]

    # 5. 上傳到向量資料庫
    success = upload_to_vector_db(index, embedded, namespace)
    if not success:
        print("❌ FAQ 向量上傳失敗")

