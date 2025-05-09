import openai
import json
from dotenv import load_dotenv
import os

def load_api_key():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

# def embed_faq_list(faq_list: list) -> list:
# #取出每一個dict，並將分類改為中文，取值用第一個方法可以增加容錯率，第二個方法如果沒有會報錯
#     embedded = []
#     for item in faq_list:
#         input_text = f"分類: {item.get('category', '')} 問題: {item['question']} 回答: {item['answer']}"
#         response = openai.embeddings.create(
#             input=input_text,
#             model="text-embedding-3-small"
#         )
#         item["embedding"] = response.data[0].embedding
#         # item["embedding"]新增embedding欄位，data[0]跟回傳值有關因為一次只處理一筆資料所以是data[0]
#         embedded.append(item)
#     return embedded

def embed_faq_list_batch(faq_list: list, batch_size=20) -> list:
    embedded = []
    
    # 依照 batch_size 切批次
    for i in range(len(faq_list), batch_size):
        batch = faq_list[i:i + batch_size]

        # 將每一筆 FAQ 組合成輸入字串
        # 列表生成式 for 寫在後面 [ expression for item in iterable ]
        # input_texts = []
        # for faq in batch:
        # text = f"分類: {faq.get('category', '')} 問題: {faq['question']} 回答: {faq['answer']}"
        # input_texts.append(text)

        input_texts = [
            f"分類: {faq.get('category', '')} 問題: {faq['question']} 回答: {faq['answer']}"
            for faq in batch
        ]

        # 一次送一批給 OpenAI 做嵌入
        response = openai.embeddings.create(
            input=input_texts,
            model="text-embedding-3-small"
        )

        # 將結果逐筆加入對應 FAQ
        # batch 是你送出去的 FAQ（例如 20 筆）
        # response.data 是 OpenAI 回傳的嵌入結果（同樣 20 筆）
        # zip(...) 會「一筆 FAQ 對應一筆結果」，像這樣配對：

        for faq, result in zip(batch, response.data):
            faq["embedding"] = result.embedding
            embedded.append(faq)

    return embedded

def embed_faq():
    load_api_key()
    with open("fdata/1.JSON", "r", encoding="utf-8") as f:
        faq_list = json.load(f)

    embedded_faqs = embed_faq_list_batch(faq_list)

    with open("embedded_faq.json", "w", encoding="utf-8") as f:
        json.dump(embedded_faqs, f, ensure_ascii=False, indent=2)

    print("✅ 成功將 FAQ 嵌入向量並儲存")


if __name__ == "__main__":
    load_api_key()
    with open("data/1.JSON", "r", encoding="utf-8") as f:
        faq_list = json.load(f)

    preview_data = embed_faq_list(faq_list[:4])

    with open("embedded_faq_preview.json", "w", encoding="utf-8") as f:
        json.dump(preview_data, f, ensure_ascii=False, indent=2)

    print("✅ 僅前 4 筆 FAQ 嵌入完成，已儲存為 embedded_faq_preview.json")

