# 測試用來篩選使用可可以看到什麼資訊

from config.openai import init_openai
from config.pinecone import get_namespace,init_pinecone
from adapters.pinecone_adapter import get_pinecone_index
from RAG.query.query_engine_safe import answer_query_secure

def run_manual_query_test(index, namespace):

    query = input("請輸入你要查詢的問題：\n> ")
    user_id = input("請輸入模擬的使用者 ID：\n> ")

    answer = answer_query_secure(query, user_id, index, namespace)

    print("\n💬 最終回覆內容：")
    print(answer)

if __name__ == "__main__":
    # 測試poetry run python -m tools.RAG_tools.manual_query_tes
    
    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()
    
    run_manual_query_test(index, namespace)