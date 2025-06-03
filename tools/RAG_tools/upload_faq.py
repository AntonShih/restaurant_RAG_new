# 資料上傳vector DB前的準備
import json
import os
from core.embedding import embed_faq_list_batch
from models.formatting import format_for_pinecone
from tools.RAG_tools.pinecone_checker import get_existing_vector_info
from config.openai import init_openai
from config.pinecone import get_namespace,init_pinecone
from adapters.pinecone_adapter import get_pinecone_index

def process_faq_file(path="data/sop.json"):
    """
    輸入相對路徑在向量化前先去重，去除資料裡面相同問題
    看似多此一舉但在第一次上傳時很重要
    """
    full_path = os.path.abspath(path) #改為絕對路徑
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            raw_faqs = json.load(f)
    except Exception as e:
        print(f"❌ 無法讀取檔案 {full_path}: {e}")
        return []

    seen = set() #唯一值
    result = []
    for faq in raw_faqs:
        q = faq.get("question")
        if q and q not in seen:
            seen.add(q)
            result.append(faq)

    print(f"📊 共讀取 {len(raw_faqs)} 筆，去重後剩 {len(result)} 筆 FAQ")
    return result

def upload_faq_from_json(path,index,namespace,batch_size=100):
    """
    主流程：拿去重後的FQA載入 FAQ 檔案、過濾重複、嵌入、格式化、上傳。
    """
    # Step 1: 載入本地 FAQ json + 去重
    faqs = process_faq_file(path)

    # Step 2: 查詢向量資料庫中已存在的問題
    _, existing_questions = get_existing_vector_info(index, namespace)

    # Step 3: 過濾重複
    new_faqs = [f for f in faqs if f["question"] not in existing_questions]
    print(f"🆕 共發現 {len(new_faqs)} 筆新問題需嵌入")

    if not new_faqs:
        print("⚠️ 所有 FAQ 已存在，無需嵌入")
        return False

    # Step 4: 執行嵌入
    print("🧠 正在生成向量嵌入...")
    embedded = embed_faq_list_batch(new_faqs)
    embedded = [f for f in embedded if "embedding" in f]

    # Step 5: 格式化 + 上傳
    vectors = format_for_pinecone(embedded)
    print(f"📦 準備上傳 {len(vectors)} 筆向量")

    try:
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch, namespace=namespace)
        print("✅ FAQ 向量上傳完成")
        return True
    except Exception as e:
        print(f"❌ 向量上傳失敗：{e}")
        return False


if __name__ == "__main__":
    # 測試 python -m tools.RAG_tools.upload_faq
    # 檢查 FAQ 去重狀態（單純看資料）
    # faqs = process_faq_file("data/sop.json")
    # print(faqs[:2])  # 印出前兩筆看看內容

    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()

     # 執行上傳流程（會自帶處理 + 上傳）
    upload_faq_from_json("data/sop.json",index,namespace)

