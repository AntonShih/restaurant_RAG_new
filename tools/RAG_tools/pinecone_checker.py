def get_existing_vector_info(index, namespace):
    """
    🔧 工具函式：取得指定 namespace 中已存在的向量 ID 與 question 集合，
    ✅ 屬於 tools，因為它是開發階段、資料管理用的輔助邏輯，不屬於主流程。
    
    回傳：
    - existing_ids: set[str]，所有已存在的向量 ID
    - existing_questions: set[str]，所有已存在的 question（從 metadata 提取）

    使用場景：
    - 判斷上傳 FAQ 時是否重複
    - 清查目前 Pinecone 中的資料內容
    """
    existing_ids, existing_questions = set(), set()
    try:
        # 取得目前 index 的統計資料
        stats = index.describe_index_stats()
        
        # 抓出指定 namespace 中的向量數量
        count = stats.get("namespaces", {}).get(namespace, {}).get("vector_count", 0)
        if count == 0:
            return existing_ids, existing_questions

        # 預測目前的向量 ID 格式為 faq_1 ~ faq_N
        fetch_ids = [f"faq_{i+1}" for i in range(count)]
        fetched = index.fetch(ids=fetch_ids, namespace=namespace)

        # 將 fetch 結果中的 ID 與問題加入集合
        for vector_id, record in fetched.vectors.items():
            existing_ids.add(vector_id)
            if record.metadata and "question" in record.metadata:
                existing_questions.add(record.metadata["question"])

    except Exception as e:
        print(f"❌ 無法取得現有向量資訊: {e}")

    return existing_ids, existing_questions
