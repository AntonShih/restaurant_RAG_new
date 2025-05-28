import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from argparse import ArgumentParser
from config.environment import init_openai, get_pinecone_index, get_namespace, init_pinecone
from RAG.tools.upload_faq import upload_faq_from_json
from RAG.tools.query_loop import interactive_mode
from RAG.tools.embedding_preview import run_preview
from RAG.tools.manual_query_test import run_manual_query_test
from RAG.query.query_engine_safe import answer_query_secure
from config.log_config import init_logging
import logging

init_logging(level=logging.DEBUG, to_file=True)


def main():
    parser = ArgumentParser()
    parser.add_argument("--upload", action="store_true", help="是否執行 FAQ 上傳")
    parser.add_argument("--path", type=str, default="data/sop.json", help="FAQ JSON 檔案路徑")
    parser.add_argument("--interactive", action="store_true", help="是否啟用互動查詢模式")
    parser.add_argument("--embedding_preview", action="store_true", help="是否在上傳前查看embedding格式前幾筆是否正確")
    parser.add_argument("--test_query", action="store_true", help="手動測試 FAQ 查詢流程")
    args = parser.parse_args()

    print("🚀 餐飲業 FAQ 系統啟動")
    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()

    if args.embedding_preview:
        print("💬  在上傳前查看embedding格式前幾筆是否正確")
        run_preview(input_path=args.path)

    if args.upload:
        print("⬆️  開始上傳 FAQ 向量資料")
        upload_faq_from_json(args.path,index,namespace)

    if args.interactive:
        print("💬  啟用查詢互動模式")
        interactive_mode(index, namespace)

    if args.test_query:
        print("💬  測試問問題，用設定的帳號及權限看回答是否正確")
        run_manual_query_test()

    if args.test_query:
        print("💬  測試問問題，用設定的帳號及權限看回答是否正確")
        run_manual_query_test()

        # logging 測試：用固定問題與使用者 ID 查詢
        test_query = "今天幾點打烊"
        test_user_id = "U_test123"

        print("\n💬 Logging 測試查詢：", test_query)
        result = answer_query_secure(test_query, test_user_id, index, namespace)
        print("🧠 回覆內容：", result)



if __name__ == "__main__":
    # 測試 poetry run python RAG/dev_runner.py --interactive --upload --embedding_preview --test_query 
    # 可指定路徑喔--path data/faq_law.json
    main()
