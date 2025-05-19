# 🧠 RAG 問答系統｜餐飲業 FAQ 智能助手

本專案是一套以 **RAG（Retrieval-Augmented Generation）架構** 為核心的智慧問答系統，專為餐飲業 FAQ 管理、員工訓練與營運支援而設計，結合 OpenAI 向量嵌入、Pinecone 向量資料庫與權限控管邏輯，並已整合 LINE Bot 使用情境。

---

## 🗂️ 專案架構

```
RAG/
├── core/                      # 核心邏輯模組
│   ├── embedding.py          # 將問題轉換為 OpenAI 向量
│   ├── formatting.py         # 將資料格式化為 Pinecone 可接受格式
│   ├── compare.py            # 相似 FAQ 向量比對查詢
│   └── pinecone_checker.py   # 檢查現有向量，避免重複上傳
│
├── query/                    # 高階查詢邏輯
│   └── query_engine_safe.py # 加入身份驗證的安全查詢
│
├── line_bot/                 # LINE Bot 使用者管理
│   ├── models.py             # 使用者資料模型、權限對應
│   ├── mongodb_client.py     # MongoDB 連線管理
│   └── webhook_handler.py    # LINE webhook 處理器
│
├── tests/                    # 測試腳本（使用 pytest）
├── data/                     # FAQ JSON 資料來源
│   └── sop.json
├── upload_faq.py             # FAQ 上傳工具（嵌入 + 上傳）
├── query_test.py             # CLI 測試介面
├── app.py                    # FastAPI 入口（LINE Webhook）
└── README.md
```

---

## ⚙️ 安裝與設定

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定 `.env` 環境變數

```env
# Pinecone 向量資料庫
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=your-index-name
PINECONE_NAMESPACE=restaurant

# OpenAI
OPENAI_API_KEY=your-openai-key

# LINE Bot
LINE_CHANNEL_ACCESS_TOKEN=xxx
LINE_CHANNEL_SECRET=xxx

# MongoDB
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=linebot_db

# 角色密碼（認證用）
PASSWORD_MANAGER=xxx
PASSWORD_NORMAL=xxx
...
```

---

## 🚀 使用流程

### 🧠 上傳 FAQ 到向量資料庫

```bash
python upload_faq.py
```

- 自動載入 FAQ JSON
- 進行去重
- 嵌入向量（OpenAI）
- 上傳到 Pinecone

---

### 🔍 啟動 CLI 查詢介面（測試用）

```bash
python query_test.py
```

---

### 🔐 安全查詢（LINE Bot 入口）

```bash
python query_engine_safe.py
```

- 查詢 top-3 相似問題
- 根據使用者職等過濾
- 回傳 GPT 回覆（限制只能根據 FAQ 回答）

---

## 💬 LINE Bot 整合功能

- 支援 RichMenu 點擊「認證角色」
- 輸入密碼後，紀錄 `user_id` 與 `access_level`
- 使用者查詢時，自動呼叫 `answer_query_secure()`
- 不符合權限者回傳警告語句

---

## 🧪 單元測試

使用 `pytest`：

```bash
pytest RAG/tests
```

測試範圍涵蓋：
- 嵌入格式正確性
- 向量格式轉換
- 查詢相似度結果
- 權限過濾邏輯（mock 測試）

---

## 🧠 FAQ JSON 格式

```json
{
  "question": "每日幾點要倒垃圾？",
  "answer": "每日 22:30 前",
  "category": "打烊與閉店流程",
  "access_level": 1
}
```

---

## ✨ 擴充建議

| 功能 | 說明 |
|------|------|
| 🔐 身分驗證後回傳不同內容 | 根據 access_level 回傳不同 FAQ、不同回覆語氣 |
| 📦 支援文件上傳自動嵌入 | 例如 SOP Word/PDF 檔 |
| 🧾 查詢記錄分析 | 蒐集常見問題供優化 FAQ |
| 🌐 整合 Web 前台介面 | 做成內部知識系統或新人教學入口 |

---

## 👨‍💻 作者

本專案由 **閔文** 設計開發，應用於實體餐飲營運場景。  
如需定製、部署協助、串接自家 SOP 系統，歡迎聯絡！

---

### 🔗 授權與貢獻

MIT License。歡迎 Fork、使用、或作為內部訓練系統基礎。  
如有貢獻需求請提交 Pull Request 或聯繫開發者 🙌
