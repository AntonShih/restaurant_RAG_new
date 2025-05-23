import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_faq_list_batch(faq_list):
    result = []
    for item in faq_list:
        response = openai.embeddings.create(
            input=item["question"],
            model="text-embedding-3-small"
        )
        item["embedding"] = response.data[0].embedding
        result.append(item)
    return result


def run_preview(
    input_path: str = "data/1.JSON",
    output_path: str = "embedded_faq_preview.json",
    preview_count: int | None = 4
):
    """將指定 FAQ json 檔前幾筆資料嵌入並輸出成 JSON"""
    if not os.path.exists(input_path):
        print(f"找不到檔案：{input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        faq_list = json.load(f)

    preview_data = embed_faq_list_batch(faq_list[:preview_count])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(preview_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已完成嵌入前 {preview_count} 筆，儲存為 {output_path}")


if __name__ == "__main__":
    run_preview()
