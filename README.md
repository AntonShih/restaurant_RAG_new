# 🧠 RAG 問答系統｜餐飲業 FAQ 智能助手

本專案是一套以 **RAG（Retrieval-Augmented Generation）架構** 為核心的智慧問答系統，專為餐飲業 FAQ 管理、員工訓練與營運支援而設計，結合 OpenAI 向量嵌入、Pinecone 向量資料庫與權限控管邏輯，達成企業客製化，並已整合 LINE Bot 使用情境。

---
## ✨ 特色亮點

🤖 LINE 聊天即問即答：無須安裝額外 App，直接透過 LINE 對話查詢

🔐 身份驗證 + 權限控管：不同職位可查閱不同內容，守住知識邊界

🧠 AI 回答嚴謹可靠：基於 FAQ 向量語意比對，GPT 僅回應資料中已有知識

🧾 SOP / FAQ 自由擴充：支援 JSON 上傳，未來可對接 Word、PDF 文件

☁️ Cloud Run 一鍵部署：支援 Docker 化建置與 GCP 雲端部署

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

## 📌 本專案採「職責導向模組設計」

第三方服務封裝統一於 adapters/

LINE webhook 與回覆訊息封裝於 line_bot/

測試與開發工具統一放在 tools/

CI/CD 自動化配置集中於 .github/

如此設計讓維護與擴充變得簡潔有序，並方便後續引入 Web 前台、權限角色分層與記錄分析等功能模組。

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


## ✨ 擴充建議


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
