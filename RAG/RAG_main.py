import os
import json
import sys
import time
from dotenv import load_dotenv

# 從其他模塊導入函數
from embedding import embed_faq_list_batch, load_api_key
from upload import format_for_pinecone
from compare import get_embedding, search_similar_faqs
from pinecone import Pinecone

def load_environment():
    """載入環境變數並初始化API連接"""
    load_dotenv()
    
    # 初始化OpenAI (使用已存在的函數)
    load_api_key()
    
    # 初始化Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME")
    namespace = os.getenv("PINECONE_NAMESPACE", "default")
    
    # 確認索引是否存在
    try:
        index = pc.Index(index_name)
        print(f"✅ 成功連接到Pinecone索引: {index_name}")
        return pc, index, namespace
    except Exception as e:
        print(f"❌ 連接Pinecone索引失敗: {str(e)}")
        sys.exit(1)

def process_faq_files(directory="data"):
    """處理指定目錄中的所有JSON檔案，檢查並移除重複的FAQ項目"""
    all_faqs = []
    seen_questions = set()  # 用於追蹤已處理的問題
    duplicate_count = 0
    
    try:
        # 獲取目錄中的所有JSON檔案
        json_files = [f for f in os.listdir(directory) if f.endswith('.json') or f.endswith('.JSON')]
        
        if not json_files:
            print(f"⚠️ 在{directory}目錄中找不到JSON檔案")
            return []
        
        # 讀取並合併所有JSON檔案
        for file in json_files:
            file_path = os.path.join(directory, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    faqs = json.load(f)
                    print(f"📁 從{file}讀取了{len(faqs)}筆FAQ資料")
                    
                    # 檢查並添加非重複項
                    file_duplicates = 0
                    for faq in faqs:
                        # 檢查問題是否已存在
                        if faq['question'] in seen_questions:
                            file_duplicates += 1
                            duplicate_count += 1
                            continue
                        
                        # 添加非重複項並更新追蹤集
                        all_faqs.append(faq)
                        seen_questions.add(faq['question'])
                    
                    if file_duplicates > 0:
                        print(f"   ⚠️ 跳過{file_duplicates}筆重複問題")
                        
            except Exception as e:
                print(f"⚠️ 無法處理檔案{file}: {str(e)}")
        
        if duplicate_count > 0:
            print(f"⚠️ 總共跳過{duplicate_count}筆重複問題")
            
        print(f"📊 總共讀取了{len(all_faqs)}筆不重複FAQ資料")
        return all_faqs
    except Exception as e:
        print(f"❌ 處理FAQ檔案時發生錯誤: {str(e)}")
        return []

def upload_to_vector_db(index, faqs, namespace):
    """將FAQ向量上傳到Pinecone，檢查並跳過重複資料"""
    try:
        # 檢查現有向量ID
        try:
            # 獲取現有向量的資料統計
            stats = index.describe_index_stats()
            # 檢查指定namespace的向量數量
            existing_count = stats.get('namespaces', {}).get(namespace, {}).get('vector_count', 0)
            print(f"ℹ️ 向量資料庫中已有{existing_count}筆向量")
            
            # 如果資料庫中已有向量，檢查重複
            existing_ids = set()
            existing_questions = set()
            
            if existing_count > 0:
                # 獲取所有已存在的向量ID和問題 (分批查詢)
                query_limit = 10000  # Pinecone的查詢限制
                for i in range(0, existing_count, query_limit):
                    # 這裡使用一個通用向量進行低閾值查詢，主要是為了獲取向量ID
                    # 實際應用中可能需要更複雜的邏輯來獲取所有向量ID
                    temp_vector = [0.0] * 1536  # OpenAI embedding的維度
                    results = index.query(
                        vector=temp_vector,
                        top_k=min(query_limit, existing_count-i),
                        include_metadata=True,
                        namespace=namespace
                    )
                    
                    # 收集ID和問題文本
                    for match in results.get('matches', []):
                        existing_ids.add(match.get('id', ''))
                        if match.get('metadata') and 'question' in match.get('metadata', {}):
                            existing_questions.add(match['metadata']['question'])
                
                print(f"ℹ️ 已獲取{len(existing_ids)}個現有向量ID和{len(existing_questions)}個問題")
        except Exception as e:
            print(f"⚠️ 無法獲取現有向量資訊，將假設沒有重複: {str(e)}")
            existing_ids = set()
            existing_questions = set()
            
        # 將FAQ格式化為Pinecone可接受的格式
        pinecone_vectors = format_for_pinecone(faqs)
        
        # 過濾掉重複的資料
        filtered_vectors = []
        for vector in pinecone_vectors:
            # 檢查ID和問題是否已存在
            if vector['id'] in existing_ids:
                continue
                
            # 檢查問題文本是否重複
            if vector['metadata']['question'] in existing_questions:
                print(f"⚠️ 跳過重複問題: {vector['metadata']['question'][:50]}...")
                continue
                
            filtered_vectors.append(vector)
            existing_ids.add(vector['id'])  # 更新已存在ID集合
            existing_questions.add(vector['metadata']['question'])  # 更新已存在問題集合
        
        print(f"ℹ️ 過濾後剩餘{len(filtered_vectors)}/{len(pinecone_vectors)}筆向量需要上傳")
        
        # 如果沒有需要上傳的資料，直接返回
        if not filtered_vectors:
            print("✅ 沒有新資料需要上傳")
            return True
        
        # 分批上傳到Pinecone (每批100筆)
        batch_size = 100
        for i in range(0, len(filtered_vectors), batch_size):
            batch = filtered_vectors[i:i+batch_size]
            index.upsert(vectors=batch, namespace=namespace)
            print(f"⬆️ 已上傳{min(i+batch_size, len(filtered_vectors))}/{len(filtered_vectors)}筆向量")
            # 避免超過API請求限制
            time.sleep(1)
        
        print(f"✅ 成功上傳所有{len(filtered_vectors)}筆新FAQ向量到Pinecone")
        return True
    except Exception as e:
        print(f"❌ 上傳向量到Pinecone時發生錯誤: {str(e)}")
        return False

def interactive_mode(index, namespace):
    """交互式模式讓用戶提問"""
    print("\n🤖 餐飲業FAQ助手已啟動！輸入'exit'結束對話\n")
    
    while True:
        user_input = input("\n請輸入您的問題：\n> ")
        
        if user_input.lower() in ['exit', 'quit', '離開', '退出']:
            print("👋 感謝使用，再見！")
            break
        
        print("🔍 搜尋中...\n")
        # 直接使用compare.py中的search_similar_faqs函數
        results = search_similar_faqs(user_input)
        
        if not results:
            print("❓ 找不到相關的FAQ，請嘗試用不同方式提問。")
            continue
        
        print("📝 最相近的FAQ：\n")
        for i, r in enumerate(results, 1):
            meta = r["metadata"]
            print(f"{i}. [{meta.get('category', '一般')}] {meta.get('question')}")
            print(f"   答：{meta.get('answer')}")
            print(f"   相似度：{round(r['score'], 4)}\n")

def main():
    """主函數，整合所有步驟"""
    print("🚀 餐飲業FAQ RAG系統啟動中...")
    
    # 載入環境變數和初始化連接
    _, index, namespace = load_environment()
    
    # 檢查是否要重新處理和上傳FAQ
    should_process = input("是否重新處理FAQ資料並上傳到向量資料庫？(y/n，預設為n): ").lower() == 'y'
    
    if should_process:
        # 處理FAQ檔案
        print("\n📂 準備處理FAQ檔案...")
        all_faqs = process_faq_files()
        
        if not all_faqs:
            print("❌ 沒有FAQ資料可處理，程序終止")
            return
        
        # 生成嵌入向量 (使用embedding.py中的函數)
        print("\n🧠 正在生成向量嵌入...")
        embedded_faqs = embed_faq_list_batch(all_faqs)

        # ✅ 確保每筆 FAQ 都有成功嵌入向量才上傳
        embedded_faqs = [f for f in embedded_faqs if "embedding" in f]
        
        # 上傳到向量資料庫
        print("\n⬆️ 正在上傳向量到Pinecone...")
        upload_success = upload_to_vector_db(index, embedded_faqs, namespace)
        
        if not upload_success:
            print("❌ 上傳失敗，程序終止")
            return
    
    # 進入交互式模式
    interactive_mode(index, namespace)

if __name__ == "__main__":
    main()