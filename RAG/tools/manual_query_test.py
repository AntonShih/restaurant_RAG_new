# 測試用來篩選使用可可以看到什麼資訊

from config.environment import init_openai,get_pinecone_index,get_namespace,init_pinecone
from RAG.query.query_engine_safe import answer_query_secure

def run_manual_query_test():
    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()

    query = input("請輸入你要查詢的問題：\n> ")
    user_id = input("請輸入模擬的使用者 ID：\n> ")

    answer = answer_query_secure(query, user_id, index, namespace)

    print("\n💬 最終回覆內容：")
    print(answer)

if __name__ == "__main__":
    # 測試poetry run python -m RAG.tools.manual_query_test
    
    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()
    
    run_manual_query_test()