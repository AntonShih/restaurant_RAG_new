
def get_existing_vector_info(index, namespace):
    """
    取得指定 namespace 中已存在的向量 ID 與 question 集合，
    回傳 (set of ids, set of questions)
    """
    existing_ids, existing_questions = set(), set()
    try:
        stats = index.describe_index_stats()
        count = stats.get("namespaces", {}).get(namespace, {}).get("vector_count", 0)
        if count == 0:
            return existing_ids, existing_questions

        # 根據目前的向量數量猜測 ID 格式為 faq_1 ~ faq_N
        fetch_ids = [f"faq_{i+1}" for i in range(count)]
        fetched = index.fetch(ids=fetch_ids, namespace=namespace)

        for vector_id, record in fetched.vectors.items():
            existing_ids.add(vector_id)
            if record.metadata and "question" in record.metadata:
                existing_questions.add(record.metadata["question"])
    except Exception as e:
        print(f"❌ 無法取得現有向量資訊: {e}")
    return existing_ids, existing_questions
