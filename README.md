# 🧠 RAG 問答系統｜餐飲業 FAQ 智能助手

本專案是一套以 **RAG（Retrieval-Augmented Generation）架構** 為核心的智慧問答系統，專為餐飲業 FAQ 管理、員工訓練與營運支援而設計，結合 OpenAI 向量嵌入、Pinecone 向量資料庫與權限控管邏輯，達成企業客製化，並已整合 LINE Bot 使用情境。

---
## ✨ 特色亮點

### 🤖 LINE 聊天即問即答  
無需安裝額外 App，用戶可直接透過 LINE 對話進行即時查詢，降低使用門檻、提升便利性。

### 🔐 身份驗證與權限控管  
導入多層身份驗證機制，不同職位可查閱不同內容，確保內部知識安全、避免資訊外洩。

### 🧠 嚴謹可信的 AI 回應邏輯  
透過 FAQ 向量語意比對，GPT 僅針對使用者有權取得的資料進行內容組合與生成，不得自行擴寫，確保回應可溯源、可驗證。

### ☁️ 雲端自動部署：GitHub Actions + GCP Cloud Run  
專案支援 Docker 化建置，並透過 GitHub Actions 自動部署至 GCP Cloud Run，快速上線、輕鬆維護。

### ⚙️ CI/CD 自動化工作流程  
建構完整的持續整合與持續部署流程（CI/CD），有效提升開發交付效率與系統穩定性。

---
## 🛠 技術架構（Tech Stack）

 - 後端框架：FastAPI（同步處理，保留 async 擴充彈性）

 - 訊息串接：LINE Messaging API（line-bot-sdk v3）

 - AI 向量檢索：OpenAI Embedding + Pinecone（RAG 檢索式生成）

 - 身份驗證與權限控管：MongoDB（使用者角色 + 存取分級）

 - 資料上傳與清洗：支援 FAQ JSON 批次匯入、自動去重

 - 部署與維運：Docker + GitHub Actions + GCP Cloud Run（CI/CD 自動部署）

---
## 🧪 測試（規劃中）
 - Pytest + Mock：初步建立測試流程，驗證資料流與外部服務整合

 - Coverage：預計導入覆蓋率追蹤，提升系統品質穩定性

## 📦 專案結構（模組職責導向）

```bash
restaurant-rag/             # 專案根目錄
├── .github/                # GitHub Actions 自動部署與 CI/CD 設定
├── adapters/               # 封裝第三方服務（OpenAI、Pinecone、MongoDB）
├── config/                 # 所有初始化設定（API 金鑰、連線）
├── core/                   # 核心邏輯
│   ├── auth/               # 簡易密碼比對
│   ├── compare.py          # 向量查詢比對
│   ├── embedding.py        # FAQ 嵌入處理
│   └── query_logic.py      # RAG 查詢主流程（嵌入 → 比對 → 篩選 → GPT）
├── data/                   # FAQ 原始 JSON 檔案
├── line_bot/               # LINE Bot webhook 與互動處理邏輯
│   ├── db/                 # MongoDB user 資料存取與身分驗證
│   ├── handlers/           # webhook message/postback 處理流程
│   └── templates/          # Flex Bubble 訊息格式生成
├── models/                 # Pinecone資料格式標準化處理
├── services/               # 商業邏輯服務層（例如 secure query 流程）
├── tools/                  # 實用工具
│   ├── line_bot_tools/     # rich menu建置
│   └── RAG_tools/          # FAQ 上傳工具
├── README.md               # 專案說明文件
├── line_bot_main.py        # FastAPI 主應用入口，接收 webhook 並路由事件
├── Dockerfile              # 本地/測試版本部署用
├── deploy.Dockerfile       # 對應 Cloud Run 正式部署用
├── .env.example            # 附上格式範例、用於部署環境參考
├── requirements.txt        # 部屬需要
└── pyproject.toml          # Poetry 依賴管理
```
---

## ⚙️ 快速安裝與設定

### 1️⃣ 安裝依賴

```bash
poetry install
```

### 2️⃣ 設定環境變數 `.env`

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
```

---

## 🚀 使用流程

### 上傳 FAQ 並建構向量庫

```bash
python upload_faq.py
```
* 自動載入資料、去重、產生嵌入、上傳 Pinecone

### 整合至 LINE Bot 流程

* 使用者透過 LINE 傳送「認證：職位」進行身份確認
* 成功後可查詢問題，例如「炸鍋油多久換？」
* 系統根據權限 → 對應 FAQ → 比對語意 → GPT 回答
* 不符合權限者將回傳警示訊息
---

## 🗂 FAQ 格式範例

```json
{
  "question": "每日幾點要倒垃圾？",
  "answer": "每日 22:30 前",
  "category": "打烊與閉店流程",
  "access_level": 1
}
```

---

## ☁️ Cloud Run 部署教學

### 1. 建立映像檔

```bash
docker build -t asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/your-repo/line-rag-bot .
docker push asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/your-repo/line-rag-bot
```

### 2. 部署至 GCP

* 建立 Cloud Run 服務並指定映像檔
* 設定環境變數與 webhook callback URL
* 部署完成後即可透過 LINE 使用

---

## 🧩 擴充建議（未來 Roadmap）

| 功能項目         | 說明                                                                 |
|------------------|----------------------------------------------------------------------|
| ✅ Redis 快取     | 1. 加速重複查詢，避免頻繁嵌入與向量查找<br>2. 取代本地記憶體存取驗證          |
| ✅ 完善 CI/CD 測試流程 | 增加自動化測試與部署驗證邏輯                                                 |
| 🎨 Flex Bubble 美化 | 將回答格式設計得更結構化、視覺引導性更佳                                         |
| 🧑‍💻 外部認證頁面   | 新增 Web 認證介面，支援密碼輸入與身份確認                                         |
| 🧑‍💻 Fastapi   | 新增 Web 認證介面，支援密碼輸入與身份確認                                         |

---

## 👨‍💻 作者

本專案由 **閔文** 設計開發，應用於實體餐飲營運場景。  
如需定製、部署協助、串接自家 SOP 系統，歡迎聯絡！

---

### 🔗 授權與貢獻

MIT License。歡迎 Fork、使用、或作為內部訓練系統基礎。  
如有貢獻需求請提交 Pull Request 或聯繫開發者 🙌

📮 聯絡方式：[anton.shih7@gmail.com]

---

## 🔓 授權

MIT License

歡迎自由使用、fork、修改，或與我聯絡共同開發適用於其他產業場景的知識查詢解決方案。
