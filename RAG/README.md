# 🧠 餐飲業 FAQ 問答系統（RAG 架構）

本專案為一套以 RAG（Retrieval-Augmented Generation）架構打造的 FAQ 自助查詢系統，結合 OpenAI 向量嵌入與 Pinecone 向量資料庫，適用於餐飲業日常 SOP、員工訓練與突發狀況處理。

---

## 📂 專案結構

RAG/
├── core/ # 核心模組
│ ├── compare.py # 相似 FAQ 查詢
│ ├── embedding.py # 問題嵌入產生器
│ ├── formatting.py # 向量格式轉換器
│ └── pinecone_checker.py # 現有向量去重判斷
│
├── data/
│ └── sop.json # 原始 FAQ 資料集（JSON 格式）
│
├── query/
│ └── query_engine_safe.py # 連結line bot 權限控管 + GPT 回答
│
├── tests/ # 單元測試模組
│ ├── test_compare.py
│ ├── test_embedding.py
│ ├── test_formatting.py
│ └── test_vector_utils.py
│
├── upload_faq.py # FAQ 向量上傳主腳本
├── query_test.py # CLI 查詢介面測試腳本
└── README.md # 說明文件